import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side


def create_excel_schedule(solver, shift_vars, employees, num_days, num_shifts, colors):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Schedule"
    ws.sheet_view.rightToLeft = True

    # --- Styles ---
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    sub_header_fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2",
                                  fill_type="solid")  # Light blue for buildings
    center_align = Alignment(horizontal='center', vertical='center', wrap_text=True)
    thin_border = Border(left=Side(style='thin'), right=Side(style='thin'),
                         top=Side(style='thin'), bottom=Side(style='thin'))

    days_names = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי", "שבת"]

    # --- Main Headers ---
    # Col 1: Time, Col 2: Role
    ws.cell(row=1, column=1).value = "זמן"  # Time
    ws.cell(row=1, column=2).value = "תפקיד"  # Role

    for i, day in enumerate(days_names):
        cell = ws.cell(row=1, column=i + 3)
        cell.value = day
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_align

    # -------------------------------------------------------------------------
    # Layout Definition
    # -------------------------------------------------------------------------
    # System Shifts (Config): 0=Morning, 1=Noon, 2=Night, 3=Reinforcement

    layout_weekday = [
        # === Building 15 ===
        {"title": "בניין 15", "is_header": True},

        # Morning Block
        {"time": "בוקר", "role": "קבלה", "shift": 0, "role_needed": "guard"},
        {"time": "", "role": "סייר", "shift": 0, "role_needed": "guard"},
        {"time": "", "role": "אחמ\"ש", "shift": 3, "role_needed": "supervisor"},

        {"is_spacer": True},  # Empty row

        # Noon Block
        {"time": "צהריים", "role": "קבלה", "shift": 1, "role_needed": "guard"},
        {"time": "", "role": "סייר", "shift": 1, "role_needed": "guard"},

        {"is_spacer": True},  # Empty row

        # Night Block
        {"time": "לילה", "role": "קבלה", "shift": 2, "role_needed": "guard"},
        {"time": "", "role": "סייר", "shift": 2, "role_needed": "guard"},

        # === Building 18 ===
        {"title": "בניין 18", "is_header": True},

        # Morning Block (+ Reinforcements)
        {"time": "בוקר", "role": "קבלה", "shift": 0, "role_needed": "guard"},
        {"time": "", "role": "בקרה", "shift": 0, "role_needed": "controller"},
        {"time": "", "role": "אחמ\"ש", "shift": 0, "role_needed": "supervisor"},
        {"time": "", "role": "סייר (7-18)", "shift": 3, "role_needed": "guard"},
        {"time": "", "role": "מאבטח 1 (7-18)", "shift": 3, "role_needed": "guard"},
        {"time": "", "role": "מאבטח 2 (7-18)", "shift": 3, "role_needed": "guard"},

        {"is_spacer": True},  # Empty row

        # Noon Block
        {"time": "צהריים", "role": "קבלה", "shift": 1, "role_needed": "guard"},
        {"time": "", "role": "בקרה", "shift": 1, "role_needed": "controller"},
        {"time": "", "role": "אחמ\"ש", "shift": 1, "role_needed": "supervisor"},

        {"is_spacer": True},  # Empty row

        # Night Block
        {"time": "לילה", "role": "קבלה", "shift": 2, "role_needed": "guard"},
        {"time": "", "role": "בקרה", "shift": 2, "role_needed": "controller"},
        {"time": "", "role": "סייר", "shift": 2, "role_needed": "guard"},
    ]

    full_layout = layout_weekday
    current_row = 2

    # Set to prevent duplicates - initialized once!
    used_assignments = set()

    # Helper function to rank roles: Guard=1, Controller=2, Supervisor=3
    def get_employee_rank(emp_idx):
        r = employees[emp_idx].get('role', 'guard')
        if r == 'supervisor': return 3
        if r == 'controller': return 2
        return 1

    # Iterate over layout
    for row_def in full_layout:

        # 1. Handle Building Headers
        if row_def.get("is_header"):
            # Merge across all columns for the title
            ws.merge_cells(start_row=current_row, start_column=1, end_row=current_row, end_column=2 + 7)
            cell = ws.cell(row=current_row, column=1)
            cell.value = row_def["title"]
            cell.font = Font(bold=True, size=12)
            cell.fill = sub_header_fill
            cell.alignment = center_align
            current_row += 1
            continue

        # 2. Handle Spacer Rows (Empty rows)
        if row_def.get("is_spacer"):
            current_row += 1
            continue

        # 3. Regular Rows
        # Column 1: Time
        time_cell = ws.cell(row=current_row, column=1)
        time_cell.value = row_def["time"]
        time_cell.border = thin_border
        time_cell.alignment = center_align
        if row_def["time"]:  # Make the main time label bold
            time_cell.font = Font(bold=True)

        # Column 2: Role
        role_cell = ws.cell(row=current_row, column=2)
        role_cell.value = row_def["role"]
        role_cell.border = thin_border
        role_cell.alignment = Alignment(horizontal='right', vertical='center')

        shift_idx = row_def["shift"]
        role_needed = row_def["role_needed"]

        # Iterate over days
        for d in range(num_days):
            cell = ws.cell(row=current_row, column=d + 3)
            cell.border = thin_border
            cell.alignment = center_align

            # Weekend Filtering Logic
            is_weekend = (d >= 5)  # 5=Friday, 6=Saturday
            skip_assignment = False

            if is_weekend:
                if shift_idx == 3:  # Skip reinforcement shifts on weekends
                    cell.fill = PatternFill(start_color="E7E6E6", end_color="E7E6E6", fill_type="solid")
                    skip_assignment = True
                if "אחמ\"ש" in row_def["role"]:  # Skip supervisor lines on weekends (optional per your logic)
                    cell.fill = PatternFill(start_color="E7E6E6", end_color="E7E6E6", fill_type="solid")
                    skip_assignment = True

            if not skip_assignment:
                assigned_emp = None

                # 1. Collect ALL candidates assigned by solver to this shift
                candidates = []
                for e_idx, emp in enumerate(employees):
                    if solver.Value(shift_vars[(e_idx, d, shift_idx)]):
                        candidates.append(e_idx)

                # 2. Priority Sorting (Critical Fix from previous step)
                # Sort candidates based on role scarcity to prevent "cannibalization"
                if role_needed == 'guard':
                    # Use lower ranks (Guards) first
                    candidates.sort(key=get_employee_rank)
                elif role_needed == 'controller':
                    # Use Controllers (rank 2) first, then Supervisors (rank 3)
                    candidates.sort(key=lambda x: (0 if get_employee_rank(x) == 2 else 1))
                elif role_needed == 'supervisor':
                    # Only supervisors can do this, no special sort needed mostly
                    pass

                # 3. Assign the first valid candidate
                for cand_idx in candidates:
                    if (d, cand_idx) in used_assignments:
                        continue

                    emp_role = employees[cand_idx].get('role', 'guard')
                    is_match = False

                    if role_needed == 'guard':
                        is_match = True
                    elif role_needed == 'controller':
                        if emp_role in ['controller', 'supervisor']:
                            is_match = True
                    elif role_needed == 'supervisor':
                        if emp_role == 'supervisor':
                            is_match = True

                    if is_match:
                        assigned_emp = cand_idx
                        used_assignments.add((d, cand_idx))
                        break

                # Write to Excel
                if assigned_emp is not None:
                    name = employees[assigned_emp]['name']
                    color = colors[assigned_emp] if assigned_emp < len(colors) else "FFFFFF"

                    cell.value = name
                    cell.fill = PatternFill(start_color=color, end_color=color, fill_type="solid")

        current_row += 1

    output_filename = "shift_schedule_output/shift_schedule_colored.xlsx"
    wb.save(output_filename)
    print(f"Excel file created successfully with New Layout: {output_filename}")