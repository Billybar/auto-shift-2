import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side


def create_excel_schedule(solver, shift_vars, employees, num_days, num_shifts, colors):
    wb = openpyxl.Workbook()

    # --- Sheet 1: Schedule ---
    ws = wb.active
    ws.title = "Schedule"
    ws.sheet_view.rightToLeft = True

    # --- Styles ---
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    sub_header_fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
    center_align = Alignment(horizontal='center', vertical='center', wrap_text=True)
    thin_border = Border(left=Side(style='thin'), right=Side(style='thin'),
                         top=Side(style='thin'), bottom=Side(style='thin'))

    # Conditional formatting colors
    alert_red_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
    alert_green_fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
    alert_orange_fill = PatternFill(start_color="FCE4D6", end_color="FCE4D6", fill_type="solid")

    days_names = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי", "שבת"]

    # --- Main Headers ---
    ws.cell(row=1, column=1).value = "זמן"
    ws.cell(row=1, column=2).value = "תפקיד"

    for i, day in enumerate(days_names):
        cell = ws.cell(row=1, column=i + 3)
        cell.value = day
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_align

    # -------------------------------------------------------------------------
    # Layout Definition
    # -------------------------------------------------------------------------
    layout_weekday = [
        # === Building 15 ===
        {"title": "בניין 15", "is_header": True},
        {"time": "בוקר", "role": "קבלה", "shift": 0, "role_needed": "guard"},
        {"time": "", "role": "סייר", "shift": 0, "role_needed": "guard"},
        {"time": "", "role": "אחמ\"ש", "shift": 3, "role_needed": "supervisor"},
        {"is_spacer": True},
        {"time": "צהריים", "role": "קבלה", "shift": 1, "role_needed": "guard"},
        {"time": "", "role": "סייר", "shift": 1, "role_needed": "guard"},
        {"is_spacer": True},
        {"time": "לילה", "role": "קבלה", "shift": 2, "role_needed": "guard"},
        {"time": "", "role": "סייר", "shift": 2, "role_needed": "guard"},

        # === Building 18 ===
        {"title": "בניין 18", "is_header": True},
        {"time": "בוקר", "role": "קבלה", "shift": 0, "role_needed": "guard"},
        {"time": "", "role": "בקרה", "shift": 0, "role_needed": "controller"},
        {"time": "", "role": "אחמ\"ש", "shift": 0, "role_needed": "supervisor"},
        {"time": "", "role": "סייר (7-18)", "shift": 3, "role_needed": "guard"},
        {"time": "", "role": "מאבטח 1 (7-18)", "shift": 3, "role_needed": "guard"},
        {"time": "", "role": "מאבטח 2 (7-18)", "shift": 3, "role_needed": "guard"},
        {"is_spacer": True},
        {"time": "צהריים", "role": "קבלה", "shift": 1, "role_needed": "guard"},
        {"time": "", "role": "בקרה", "shift": 1, "role_needed": "controller"},
        {"time": "", "role": "אחמ\"ש", "shift": 1, "role_needed": "supervisor"},
        {"is_spacer": True},
        {"time": "לילה", "role": "קבלה", "shift": 2, "role_needed": "guard"},
        {"time": "", "role": "בקרה", "shift": 2, "role_needed": "controller"},
        {"time": "", "role": "סייר", "shift": 2, "role_needed": "guard"},
    ]

    current_row = 2
    used_assignments = set()

    # --- Data Structures for Statistics ---
    shift_counts = {i: {0: 0, 1: 0, 2: 0, 3: 0} for i in range(len(employees))}

    # Pre-calculate counts
    for e_idx in range(len(employees)):
        for d in range(num_days):
            for s in range(num_shifts):
                if solver.Value(shift_vars[(e_idx, d, s)]):
                    shift_counts[e_idx][s] += 1

    role_fill_counts = {i: {'supervisor': 0, 'controller': 0, 'guard': 0} for i in range(len(employees))}

    def get_employee_rank(emp_idx):
        r = employees[emp_idx].get('role', 'guard')
        if r == 'supervisor': return 3
        if r == 'controller': return 2
        return 1

    # --- Generate Schedule Table ---
    for row_def in layout_weekday:
        if row_def.get("is_header"):
            ws.merge_cells(start_row=current_row, start_column=1, end_row=current_row, end_column=9)
            cell = ws.cell(row=current_row, column=1)
            cell.value = row_def["title"]
            cell.font = Font(bold=True, size=12)
            cell.fill = sub_header_fill
            cell.alignment = center_align
            current_row += 1
            continue

        if row_def.get("is_spacer"):
            current_row += 1
            continue

        time_cell = ws.cell(row=current_row, column=1)
        time_cell.value = row_def["time"]
        time_cell.border = thin_border
        time_cell.alignment = center_align
        if row_def["time"]: time_cell.font = Font(bold=True)

        role_cell = ws.cell(row=current_row, column=2)
        role_cell.value = row_def["role"]
        role_cell.border = thin_border
        role_cell.alignment = Alignment(horizontal='right', vertical='center')

        shift_idx = row_def["shift"]
        role_needed = row_def["role_needed"]

        for d in range(num_days):
            cell = ws.cell(row=current_row, column=d + 3)
            cell.border = thin_border
            cell.alignment = center_align
            is_weekend = (d >= 5)

            skip = False
            if is_weekend and (shift_idx == 3 or "אחמ\"ש" in row_def["role"]):
                cell.fill = PatternFill(start_color="E7E6E6", end_color="E7E6E6", fill_type="solid")
                skip = True

            if not skip:
                candidates = []
                for e_idx, emp in enumerate(employees):
                    if solver.Value(shift_vars[(e_idx, d, shift_idx)]):
                        candidates.append(e_idx)

                if role_needed == 'guard':
                    candidates.sort(key=get_employee_rank)
                elif role_needed == 'controller':
                    candidates.sort(key=lambda x: (0 if get_employee_rank(x) == 2 else 1))

                assigned_emp = None
                for cand_idx in candidates:
                    if (d, cand_idx) in used_assignments: continue

                    emp_role = employees[cand_idx].get('role', 'guard')
                    is_match = False
                    if role_needed == 'guard':
                        is_match = True
                    elif role_needed == 'controller' and emp_role in ['controller', 'supervisor']:
                        is_match = True
                    elif role_needed == 'supervisor' and emp_role == 'supervisor':
                        is_match = True

                    if is_match:
                        assigned_emp = cand_idx
                        used_assignments.add((d, cand_idx))
                        role_fill_counts[assigned_emp][role_needed] += 1
                        break

                if assigned_emp is not None:
                    name = employees[assigned_emp]['name']
                    color = colors[assigned_emp] if assigned_emp < len(colors) else "FFFFFF"
                    cell.value = name
                    cell.fill = PatternFill(start_color=color, end_color=color, fill_type="solid")
        current_row += 1

    # =========================================================================
    # Sheet 2: Statistics
    # =========================================================================
    ws_stats = wb.create_sheet("סטטיסטיקות")
    ws_stats.sheet_view.rightToLeft = True
    stats_header_fill = PatternFill(start_color="70AD47", end_color="70AD47", fill_type="solid")

    # --- Table 1: Shift Type Summary ---
    row_cursor = 2
    ws_stats.cell(row=row_cursor, column=1).value = "סיכום משמרות לעובד"
    ws_stats.cell(row=row_cursor, column=1).font = Font(bold=True, size=14)
    row_cursor += 1

    headers = ["שם העובד", "בוקר", "צהריים", "לילה", "תגבור", 'סה"כ', 'יעד']
    for col_idx, h in enumerate(headers, 1):
        c = ws_stats.cell(row=row_cursor, column=col_idx)
        c.value = h
        c.font = header_font
        c.fill = stats_header_fill
        c.alignment = center_align
        c.border = thin_border
    row_cursor += 1

    for e_idx, emp in enumerate(employees):
        counts = shift_counts[e_idx]
        total = counts[0] + counts[1] + counts[2] + counts[3]
        target = emp.get('target_shifts', 0)
        night_shifts = counts[2]

        row_data = [emp['name'], counts[0], counts[1], counts[2], counts[3], total, target]
        row_fill = None
        if total > target: row_fill = alert_green_fill
        if total < target: row_fill = alert_red_fill
        if night_shifts > 2: row_fill = alert_orange_fill

        for col_idx, val in enumerate(row_data, 1):
            c = ws_stats.cell(row=row_cursor, column=col_idx)
            c.value = val
            c.border = thin_border
            c.alignment = center_align
            if row_fill: c.fill = row_fill
        row_cursor += 1

    # --- Summary Row Calculation (MOVED HERE) ---
    # This must happen immediately after Table 1 is finished
    total_morning = sum(shift_counts[e][0] for e in range(len(employees)))
    total_noon = sum(shift_counts[e][1] for e in range(len(employees)))
    total_night = sum(shift_counts[e][2] for e in range(len(employees)))
    total_reinforcement = sum(shift_counts[e][3] for e in range(len(employees)))
    total_actual = total_morning + total_noon + total_night + total_reinforcement
    total_target = sum(emp.get('target_shifts', 0) for emp in employees)

    summary_data = ["TOTAL", total_morning, total_noon, total_night, total_reinforcement, total_actual, total_target]

    for col_idx, val in enumerate(summary_data, 1):
        c = ws_stats.cell(row=row_cursor, column=col_idx)
        c.value = val
        c.font = Font(bold=True)
        c.fill = PatternFill(start_color="DDDDDD", end_color="DDDDDD", fill_type="solid")
        c.border = thin_border
        c.alignment = center_align

    row_cursor += 1  # Move cursor past the Total row
    row_cursor += 2  # Spacer between tables

    # --- Table 2: Supervisor Shift Summary ---
    ws_stats.cell(row=row_cursor, column=1).value = 'סיכום משמרות אחמ"ש'
    ws_stats.cell(row=row_cursor, column=1).font = Font(bold=True, size=14)
    row_cursor += 1

    ws_stats.cell(row=row_cursor, column=1).value = "שם האחמ\"ש"
    ws_stats.cell(row=row_cursor, column=2).value = 'סה"כ משמרות בתפקיד אחמ"ש'
    for c_i in [1, 2]:
        c = ws_stats.cell(row=row_cursor, column=c_i)
        c.font = header_font
        c.fill = PatternFill(start_color="ED7D31", end_color="ED7D31", fill_type="solid")
        c.border = thin_border
    row_cursor += 1

    for e_idx, emp in enumerate(employees):
        if emp.get('role') == 'supervisor':
            shifts_as_sup = role_fill_counts[e_idx]['supervisor']

            c1 = ws_stats.cell(row=row_cursor, column=1)
            c1.value = emp['name']
            c1.border = thin_border

            c2 = ws_stats.cell(row=row_cursor, column=2)
            c2.value = shifts_as_sup
            c2.border = thin_border
            c2.alignment = center_align
            row_cursor += 1

    row_cursor += 2  # Spacer

    # --- Table 3: Controller Shift Summary ---
    ws_stats.cell(row=row_cursor, column=1).value = 'סיכום משמרות בקרה'
    ws_stats.cell(row=row_cursor, column=1).font = Font(bold=True, size=14)
    row_cursor += 1

    ws_stats.cell(row=row_cursor, column=1).value = "שם הבקר"
    ws_stats.cell(row=row_cursor, column=2).value = 'סה"כ משמרות בתפקיד בקר'
    for c_i in [1, 2]:
        c = ws_stats.cell(row=row_cursor, column=c_i)
        c.font = header_font
        c.fill = PatternFill(start_color="5B9BD5", end_color="5B9BD5", fill_type="solid")
        c.border = thin_border
    row_cursor += 1

    for e_idx, emp in enumerate(employees):
        if emp.get('role') in ['controller', 'supervisor']:
            if emp.get('role') == 'controller':
                shifts_as_con = role_fill_counts[e_idx]['controller']

                c1 = ws_stats.cell(row=row_cursor, column=1)
                c1.value = emp['name']
                c1.border = thin_border

                c2 = ws_stats.cell(row=row_cursor, column=2)
                c2.value = shifts_as_con
                c2.border = thin_border
                c2.alignment = center_align
                row_cursor += 1

    # --- Save ---
    output_filename = "shift_schedule_output/shift_schedule_colored.xlsx"
    wb.save(output_filename)
    print(f"Excel file created successfully with Statistics: {output_filename}")