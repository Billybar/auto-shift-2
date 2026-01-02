import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter


# הגדרת מיפוי תפקידים מהבקשה שלך לתפקידים במערכת
# Reception/Patrol/Security Guard -> נניח שכולם דורשים 'guard' (או כל עובד שיכול לבצע שמירה)
# Control -> 'controller'
# Supervisor -> 'supervisor'

def create_excel_schedule(solver, shift_vars, employees, num_days, num_shifts, colors):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Schedule"
    ws.sheet_view.rightToLeft = True

    # עיצובים
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    sub_header_fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")  # תכלת לבניינים
    center_align = Alignment(horizontal='center', vertical='center', wrap_text=True)
    thin_border = Border(left=Side(style='thin'), right=Side(style='thin'),
                         top=Side(style='thin'), bottom=Side(style='thin'))

    days_names = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי", "שבת"]

    # כותרות ראשיות
    ws.cell(row=1, column=1).value = "עמדה / בניין"
    ws.cell(row=1, column=2).value = "תפקיד במשמרת"

    for i, day in enumerate(days_names):
        cell = ws.cell(row=1, column=i + 3)
        cell.value = day
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_align

    # -------------------------------------------------------------------------
    # הגדרת המבנה (Layout) של הטבלה
    # -------------------------------------------------------------------------
    # משמרות: 0=בוקר, 1=צהריים, 2=לילה, 3=תגבור

    # מבנה אמצע שבוע (א-ה)
    layout_weekday = [
        # --- בניין 15 ---
        {"title": "בניין 15", "is_header": True},
        {"label": "קבלה (בוקר)", "shift": 0, "role_needed": "guard"},
        {"label": "קבלה (צהריים)", "shift": 1, "role_needed": "guard"},
        {"label": "קבלה (לילה)", "shift": 2, "role_needed": "guard"},
        {"label": "סייר (בוקר)", "shift": 0, "role_needed": "guard"},
        {"label": "סייר (צהריים)", "shift": 1, "role_needed": "guard"},
        {"label": "סייר (לילה)", "shift": 2, "role_needed": "guard"},
        {"label": "אחמ\"ש (תגבור 07-17)", "shift": 3, "role_needed": "supervisor"},

        # --- בניין 18 ---
        {"title": "בניין 18", "is_header": True},
        {"label": "קבלה (בוקר)", "shift": 0, "role_needed": "guard"},
        {"label": "קבלה (צהריים)", "shift": 1, "role_needed": "guard"},
        {"label": "קבלה (לילה)", "shift": 2, "role_needed": "guard"},

        {"label": "בקרה (בוקר)", "shift": 0, "role_needed": "controller"},
        {"label": "בקרה (צהריים)", "shift": 1, "role_needed": "controller"},
        {"label": "בקרה (לילה)", "shift": 2, "role_needed": "controller"},

        {"label": "אחמ\"ש (בוקר)", "shift": 0, "role_needed": "supervisor"},
        {"label": "אחמ\"ש (ערב/צהריים)", "shift": 1, "role_needed": "supervisor"},  # הנחתי שערב הכוונה למשמרת השנייה

        {"label": "מאבטח 1 (תגבור 08-18)", "shift": 3, "role_needed": "guard"},
        {"label": "מאבטח 2 (תגבור 08-18)", "shift": 3, "role_needed": "guard"},
        {"label": "סייר (תגבור 08-18)", "shift": 3, "role_needed": "guard"},
    ]

    # מבנה סוף שבוע (ו-ש)
    layout_weekend = [
        # --- בניין 15 ---
        {"title": "בניין 15 (סופ\"ש)", "is_header": True},
        {"label": "קבלה (בוקר)", "shift": 0, "role_needed": "guard"},
        {"label": "קבלה (צהריים)", "shift": 1, "role_needed": "guard"},
        {"label": "קבלה (לילה)", "shift": 2, "role_needed": "guard"},
        {"label": "סייר (בוקר)", "shift": 0, "role_needed": "guard"},
        {"label": "סייר (צהריים)", "shift": 1, "role_needed": "guard"},
        {"label": "סייר (לילה)", "shift": 2, "role_needed": "guard"},

        # --- בניין 18 ---
        {"title": "בניין 18 (סופ\"ש)", "is_header": True},
        {"label": "קבלה (בוקר)", "shift": 0, "role_needed": "guard"},
        {"label": "קבלה (צהריים)", "shift": 1, "role_needed": "guard"},
        {"label": "קבלה (לילה)", "shift": 2, "role_needed": "guard"},

        {"label": "סייר (בוקר)", "shift": 0, "role_needed": "guard"},
        {"label": "סייר (צהריים)", "shift": 1, "role_needed": "guard"},
        {"label": "סייר (לילה)", "shift": 2, "role_needed": "guard"},

        {"label": "בקרה (בוקר)", "shift": 0, "role_needed": "controller"},
        {"label": "בקרה (צהריים)", "shift": 1, "role_needed": "controller"},
        {"label": "בקרה (לילה)", "shift": 2, "role_needed": "controller"},
    ]

    # מיזוג הרשימות כדי לייצר אינדקס שורות אחיד באקסל
    # מכיוון שהמבנה משתנה בין אמצע שבוע לסופ"ש, נצטרך לצייר את כל השורות
    # ובמקום שבו השורה לא רלוונטית ליום מסוים, נשאיר ריק או נסמן.
    # גישה פשוטה יותר: רשימת השורות היא המקסימלית (של אמצע שבוע),
    # ובסופ"ש נתעלם משורות התגבור שלא קיימות.

    # לצורך הפשטות והנראות, נשתמש ב-Layout של אמצע השבוע כשלד הראשי,
    # ובימים ו-ש נדלג על השיבוץ בשורות שאינן קיימות בסופ"ש.

    full_layout = layout_weekday

    current_row = 2

    # מעבר על כל שורה בהגדרה (Layout)
    for row_def in full_layout:

        # 1. כותרות (בניין 15 / בניין 18)
        if row_def.get("is_header"):
            ws.merge_cells(start_row=current_row, start_column=1, end_row=current_row, end_column=2 + 7)
            cell = ws.cell(row=current_row, column=1)
            cell.value = row_def["title"]
            cell.font = Font(bold=True, size=12)
            cell.fill = sub_header_fill
            cell.alignment = center_align
            current_row += 1
            continue

        # 2. שורות רגילות
        # עמודה 1+2: תיאור העמדה
        ws.merge_cells(start_row=current_row, start_column=1, end_row=current_row, end_column=2)
        desc_cell = ws.cell(row=current_row, column=1)
        desc_cell.value = row_def["label"]
        desc_cell.border = thin_border
        desc_cell.alignment = Alignment(horizontal='right', vertical='center')

        # משתני עזר לשיבוץ
        shift_idx = row_def["shift"]
        role_needed = row_def["role_needed"]

        # מעבר על כל יום בשבוע
        for d in range(num_days):
            cell = ws.cell(row=current_row, column=d + 3)
            cell.border = thin_border
            cell.alignment = center_align

            # בדיקה: האם השורה הזו רלוונטית ליום הזה?
            is_weekend = (d >= 5)  # 5=שישי, 6=שבת

            # אם זה סופ"ש, אבל השורה היא "תגבור" או "אחמש בוקר/ערב" שלא קיים בסופ"ש לפי ההגדרה שלך
            # נצטרך לסנן. לפי התיאור שלך, בסופ"ש יש רק: קבלה, סייר, בקרה (כולם 24/7).
            # כלומר שורות תגבור ושורות אחמ"ש - לא פעילות בסופ"ש.

            skip_assignment = False
            if is_weekend:
                if "תגבור" in row_def["label"] or "אחמ\"ש" in row_def["label"]:
                    cell.fill = PatternFill(start_color="E7E6E6", end_color="E7E6E6", fill_type="solid")  # אפור
                    skip_assignment = True

            if not skip_assignment:
                # מציאת עובד מתאים מהפתרון (Solver)
                # אנו מחפשים עובד ששובץ למשמרת (shift_idx) ביום (d)
                # ויש לו את התפקיד המתאים (role_needed)
                # וגם - שעוד לא השתמשנו בו בשורה קודמת באותו יום!

                assigned_emp = None

                # נאסוף את כל העובדים המשובצים למשמרת זו ביום הזה
                candidates = []
                for e_idx, emp in enumerate(employees):
                    if solver.Value(shift_vars[(e_idx, d, shift_idx)]):
                        # בדיקה האם העובד כבר "בוזבז" בשורות קודמות של אותו יום
                        # לצורך זה נצטרך לשמור state חיצוני או להשתמש ב-Set זמני לכל יום
                        # הגישה הכי טובה: לחשב את זה מראש או לסמן.
                        # כאן נשתמש בסימון זמני באובייקט העובד (לא אידיאלי) או ברשימה מקומית.
                        candidates.append(e_idx)

                # כעת צריך לבחור אחד מהמועמדים שמתאים לתפקיד
                # ושלא שובץ כבר באותו יום בשורות *אחרות* בטבלה הזו.
                # כדי לעשות זאת, נשמור סט של (day, employee_index) שכבר כתבנו לאקסל.

                if not hasattr(create_excel_schedule, "used_assignments"):
                    create_excel_schedule.used_assignments = set()

                # איפוס הסט בתחילת ריצה (טריק מלוכלך בגלל הפונקציה, עדיף להעביר משתנה)
                if row_def == full_layout[1] and d == 0:
                    create_excel_schedule.used_assignments = set()

                for cand_idx in candidates:
                    # האם כבר שובץ בשורה אחרת היום?
                    if (d, cand_idx) in create_excel_schedule.used_assignments:
                        continue

                    # בדיקת התאמת תפקיד
                    emp_role = employees[cand_idx].get('role', 'guard')  # ברירת מחדל שומר

                    is_match = False
                    if role_needed == 'guard':
                        # לשמירה יכול להיכנס כל אחד (אלא אם יש לך חוקים אחרים)
                        is_match = True
                    elif role_needed == 'controller':
                        # לבקרה יכול להיכנס בקר או אחמ"ש
                        if emp_role in ['controller', 'supervisor']:
                            is_match = True
                    elif role_needed == 'supervisor':
                        # לאחמ"ש יכול להיכנס רק אחמ"ש
                        if emp_role == 'supervisor':
                            is_match = True

                    if is_match:
                        assigned_emp = cand_idx
                        create_excel_schedule.used_assignments.add((d, cand_idx))
                        break

                # כתיבה לתא
                if assigned_emp is not None:
                    name = employees[assigned_emp]['name']
                    color = colors[assigned_emp] if assigned_emp < len(colors) else "FFFFFF"

                    cell.value = name
                    cell.fill = PatternFill(start_color=color, end_color=color, fill_type="solid")
                else:
                    # אם לא נמצא עובד (אולי חוסר בכוח אדם או שהאופטימיזר לא שיבץ מספיק)
                    pass

        current_row += 1

    # הוספת מקרא או סיכום אם רוצים (אופציונלי)

    # שמירה
    output_filename = "shift_schedule_output/shift_schedule_colored.xlsx"
    wb.save(output_filename)
    print(f"Excel file created successfully with Building layout: {output_filename}")


# איפוס ה-State הסטטי למקרה של ריצות חוזרות
create_excel_schedule.used_assignments = set()