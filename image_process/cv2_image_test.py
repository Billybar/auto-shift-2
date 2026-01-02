import cv2
import numpy as np


def solve_schedule_precision(image_path):
    # 1. טעינת תמונה
    img = cv2.imread(image_path)
    if img is None:
        print("Error: Image not found.")
        return

    # שכפול לטובת ציור התוצאה הסופית
    debug_img = img.copy()

    # --- שלב א: זיהוי אגרסיבי של העיגולים האדומים ---
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # הרחבתי משמעותית את טווח האדום כדי לא לפספס כלום
    lower_red1 = np.array([0, 70, 50])
    upper_red1 = np.array([15, 255, 255])
    lower_red2 = np.array([160, 70, 50])
    upper_red2 = np.array([180, 255, 255])

    mask = cv2.inRange(hsv, lower_red1, upper_red1) + cv2.inRange(hsv, lower_red2, upper_red2)

    # ניקוי רעשים וחיבור חלקים קרובים
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # מציאת קונטורים של הנקודות
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    dots = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 50: continue  # סינון רעש קטן מאוד

        x, y, w, h = cv2.boundingRect(cnt)
        center_x = x + w // 2
        center_y = y + h // 2
        dots.append((center_x, center_y))

        # ציור הנקודה שזוהתה על תמונת הדיבאג (ירוק)
        cv2.circle(debug_img, (center_x, center_y), 6, (0, 255, 0), -1)

    print(f"Debug: Found {len(dots)} red dots constraints.")

    # --- שלב ב: זיהוי קווים על תמונה 'נקייה' ---
    # אנחנו 'מוחקים' את האדום מהתמונה המקורית כדי שלא יפריע לזיהוי הקווים
    clean_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # כל מה שאדום במסכה -> הופך ללבן (כאילו ריק)
    clean_gray[mask > 0] = 255

    # בינאריזציה (שחור לבן)
    _, thresh = cv2.threshold(clean_gray, 200, 255, cv2.THRESH_BINARY_INV)

    # היסטוגרמה אנכית (סכום פיקסלים שחורים בכל עמודה)
    vertical_proj = np.sum(thresh, axis=0)

    # זיהוי פיקים (איפה שיש קו אנכי)
    height = img.shape[0]
    # סף רגישות: קו נחשב קו אם הוא לפחות 15% מגובה התמונה
    line_indices = np.where(vertical_proj > height * 255 * 0.15)[0]

    # איחוד קווים קרובים (כי קו עבה הוא כמה פיקסלים)
    vertical_lines = []
    if len(line_indices) > 0:
        group = [line_indices[0]]
        for i in range(1, len(line_indices)):
            if line_indices[i] - line_indices[i - 1] < 10:  # אם קרוב, זה אותו קו
                group.append(line_indices[i])
            else:
                vertical_lines.append(int(np.mean(group)))
                group = [line_indices[i]]
        vertical_lines.append(int(np.mean(group)))

    # הוספת גבולות תמונה אם חסרים
    width = img.shape[1]
    if not vertical_lines or vertical_lines[0] > 30: vertical_lines.insert(0, 0)
    if vertical_lines[-1] < width - 30: vertical_lines.append(width)

    vertical_lines.sort()

    # ציור הקווים שזוהו (כחול)
    for x in vertical_lines:
        cv2.line(debug_img, (x, 0), (x, height), (255, 0, 0), 2)

    # --- שלב ג: מיפוי לוגי ---
    # חלוקה לגובה (עובדים) - הנחה שזה אחיד כי זה טבלה מובנית
    row_height = height / 4

    # חלוקה לרוחב (ימים) - המרווחים בין הקווים שמצאנו
    # עברית מימין לשמאל: המרווח הראשון מימין הוא יום א'
    intervals = []
    for i in range(len(vertical_lines) - 1):
        intervals.append((vertical_lines[i], vertical_lines[i + 1]))

    # הופכים כדי להתחיל מימין
    intervals_reversed = intervals[::-1]

    # שמות הימים (לפי הסדר מימין לשמאל)
    # האינדקס 0 הוא העמודה הימנית ביותר
    header_map = ['א', 'ב', 'ג', 'ד', 'ה', 'ו', 'ש', 'Labels']

    final_schedule = {}

    for dx, dy in dots:
        # 1. מי העובד?
        emp_idx = int(dy // row_height)
        emp_id = emp_idx + 1

        # 2. איזו משמרת? (מיקום יחסי בתוך השורה של העובד)
        rel_y = (dy % row_height) / row_height

        # כיוונון עדין לגבולות המשמרות
        if rel_y < 0.38:
            shift = "בוקר"
        elif rel_y < 0.68:
            shift = "צהריים"
        else:
            shift = "ערב"

        # 3. איזה יום? (לפי קווים אנכיים)
        day_name = "?"
        for i, (start_x, end_x) in enumerate(intervals_reversed):
            if start_x <= dx <= end_x:
                if i < len(header_map):
                    day_name = header_map[i]
                else:
                    day_name = "Side-Text"
                break

        if emp_id not in final_schedule: final_schedule[emp_id] = []
        final_schedule[emp_id].append((day_name, shift))

    # שמירת תמונת הוכחה
    cv2.imwrite('../images/final_debug.jpg', debug_img)
    print("Saved 'final_debug.jpg'. Open it to verify lines and dots.")

    # הדפסה מסודרת
    for eid in sorted(final_schedule.keys()):
        # מיון פנימי לפי סדר ימים הגיוני
        constraints = final_schedule[eid]
        # פונקציית עזר למיון ימים
        day_order = {'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5, 'ו': 6, 'ש': 7, '?': 8}
        shift_order = {'בוקר': 1, 'צהריים': 2, 'ערב': 3}

        constraints.sort(key=lambda x: (day_order.get(x[0], 9), shift_order.get(x[1], 9)))

        print(f"עובד {eid}: {constraints}")


solve_schedule_precision('../images/image3.png')