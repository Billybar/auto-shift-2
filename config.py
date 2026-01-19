# config.py

# ==========================================
#         System Configuration
# ==========================================
ENABLE_IMAGE_PARSING = False
IMAGE_FILENAME = "images/image3.png"

# ==========================================
#         Shift Rules & Weights
# ==========================================
SHIFT_MORNING = 0
SHIFT_NOON = 1
SHIFT_NIGHT = 2
SHIFT_REINFORCEMENT = 3

NUM_DAYS = 7
NUM_SHIFTS = 4

# Optimization Weights
WEIGHTS = {
    'TARGET_SHIFTS': 50,
    'MAX_SHIFTS': 200,
    'REST_GAP': 2,
    'CHAIN_3_PENALTY': 60,
    'MAX_NIGHTS': 10,
    'MAX_MORNINGS': 4,
    'MAX_EVENINGS': 2,
    'CONSECUTIVE_NIGHTS': 20,
    'MIN_NIGHTS': 5,
    'MIN_MORNINGS': 4,
    'MIN_EVENINGS': 2
}


WEEKDAY_DEMAND = {
    SHIFT_MORNING:       {'guard': 3, 'controller': 1, 'supervisor': 1},
    SHIFT_NOON:          {'guard': 3, 'controller': 1, 'supervisor': 1},
    SHIFT_NIGHT:         {'guard': 4, 'controller': 1, 'supervisor': 0},
    SHIFT_REINFORCEMENT: {'guard': 3, 'controller': 0, 'supervisor': 1}
}

WEEKEND_DEMAND = {
    SHIFT_MORNING:       {'guard': 4, 'controller': 1, 'supervisor': 0},
    SHIFT_NOON:          {'guard': 4, 'controller': 1, 'supervisor': 0},
    SHIFT_NIGHT:         {'guard': 4, 'controller': 1, 'supervisor': 0},
    SHIFT_REINFORCEMENT: {'guard': 0, 'controller': 0, 'supervisor': 0}
}

# ==========================================
#         Data: Employees
# ==========================================
EMPLOYEES = [
    # Supervisor
    {'id': 0, 'name': 'אביב קוברין', 'target_shifts': 4, 'max_shifts': 4, 'role': 'supervisor', 'history_streak': 0, 'max_mornings': 5, 'min_mornings': 0, 'max_evenings': 5, 'min_evenings': 0, 'max_nights': 5, 'min_nights': 0},
    # Supervisor
    {'id': 1, 'name': 'אברהם טגניה', 'target_shifts': 5, 'max_shifts': 6, 'role': 'supervisor', 'history_streak': 0, 'max_mornings': 5, 'min_mornings': 0, 'max_evenings': 5, 'min_evenings': 0, 'max_nights': 5, 'min_nights': 0},
    # Guard
    {'id': 2, 'name': 'אוריאל כהן', 'target_shifts': 4, 'max_shifts': 4, 'role': 'guard', 'history_streak': 0, 'max_mornings': 5, 'min_mornings': 0, 'max_evenings': 5, 'min_evenings': 0, 'max_nights': 5, 'min_nights': 0},
    # Supervisor
    {'id': 3, 'name': 'איתי בכר', 'target_shifts': 5, 'max_shifts': 6, 'role': 'supervisor', 'history_streak': 0, 'max_mornings': 5, 'min_mornings': 0, 'max_evenings': 5, 'min_evenings': 0, 'max_nights': 5, 'min_nights': 0},

    # Guard
    {'id': 4, 'name': 'אלון אבשלומוב', 'target_shifts': 3, 'max_shifts': 4, 'role': 'guard', 'history_streak': 0, 'max_mornings': 5, 'min_mornings': 0, 'max_evenings': 5, 'min_evenings': 0, 'max_nights': 5, 'min_nights': 0},

    # Guard
    {'id': 5, 'name': 'אליאב דגו', 'target_shifts': 5, 'max_shifts': 6, 'role': 'guard', 'history_streak': 0, 'max_mornings': 5, 'min_mornings': 0, 'max_evenings': 5, 'min_evenings': 0, 'max_nights': 5, 'min_nights': 0},

    # Guard (New)
    {'id': 6, 'name': 'אנגלינה אגפונוב', 'target_shifts': 5, 'max_shifts': 6, 'role': 'guard', 'history_streak': 0, 'max_mornings': 5, 'min_mornings': 0, 'max_evenings': 5, 'min_evenings': 0, 'max_nights': 5, 'min_nights': 0},

    # Guard (New)
    {'id': 7, 'name': 'אסתר מנגיסטו', 'target_shifts': 5, 'max_shifts': 6, 'role': 'guard', 'history_streak': 0, 'max_mornings': 5, 'min_mornings': 0, 'max_evenings': 5, 'min_evenings': 0, 'max_nights': 5, 'min_nights': 0},

    # Guard (New)
    {'id': 8, 'name': 'אשגרה קסה', 'target_shifts': 5, 'max_shifts': 6, 'role': 'guard', 'history_streak': 0, 'max_mornings': 5, 'min_mornings': 0, 'max_evenings': 5, 'min_evenings': 0, 'max_nights': 5, 'min_nights': 0},

    # Guard
    {'id': 9, 'name': 'בן שפטר', 'target_shifts': 5, 'max_shifts': 6, 'role': 'guard', 'history_streak': 0, 'max_mornings': 5, 'min_mornings': 0, 'max_evenings': 5, 'min_evenings': 0, 'max_nights': 5, 'min_nights': 0},

    # Guard
    {'id': 10, 'name': 'בן שרעבי', 'target_shifts': 5, 'max_shifts': 6, 'role': 'guard', 'history_streak': 0, 'max_mornings': 5, 'min_mornings': 0, 'max_evenings': 5, 'min_evenings': 0, 'max_nights': 5, 'min_nights': 0},

    # Guard
    {'id': 11, 'name': 'בר פרויליך', 'target_shifts': 3, 'max_shifts': 3, 'role': 'guard', 'history_streak': 0, 'max_mornings': 5, 'min_mornings': 0, 'max_evenings': 5, 'min_evenings': 0, 'max_nights': 5, 'min_nights': 0},

    # Controller
    {'id': 12, 'name': 'דוד ניסנוב', 'target_shifts': 4, 'max_shifts': 4, 'role': 'controller', 'history_streak': 0, 'max_mornings': 5, 'min_mornings': 0, 'max_evenings': 5, 'min_evenings': 0, 'max_nights': 5, 'min_nights': 0},

    # Supervisor
    {'id': 13, 'name': 'דן מיכאל צ\'לרו', 'target_shifts': 5, 'max_shifts': 6, 'role': 'supervisor', 'history_streak': 0, 'max_mornings': 5, 'min_mornings': 0, 'max_evenings': 5, 'min_evenings': 0, 'max_nights': 5, 'min_nights': 0},

    # Controller (New)
    {'id': 14, 'name': 'יבגני קנייב', 'target_shifts': 5, 'max_shifts': 6, 'role': 'controller', 'history_streak': 0, 'max_mornings': 5, 'min_mornings': 0, 'max_evenings': 5, 'min_evenings': 0, 'max_nights': 5, 'min_nights': 0},

    # Guard
    {'id': 15, 'name': 'יובל קורן', 'target_shifts': 3, 'max_shifts': 3, 'role': 'guard', 'history_streak': 0, 'max_mornings': 5, 'min_mornings': 0, 'max_evenings': 5, 'min_evenings': 0, 'max_nights': 5, 'min_nights': 0},

    # Guard
    {'id': 16, 'name': 'יניר דחוח', 'target_shifts': 3, 'max_shifts': 4, 'role': 'guard', 'history_streak': 0, 'max_mornings': 5, 'min_mornings': 0, 'max_evenings': 5, 'min_evenings': 0, 'max_nights': 5, 'min_nights': 0},

    # Guard
    {'id': 17, 'name': 'לי פז', 'target_shifts': 3, 'max_shifts': 3, 'role': 'guard', 'history_streak': 0, 'max_mornings': 5, 'min_mornings': 0, 'max_evenings': 5, 'min_evenings': 0, 'max_nights': 5, 'min_nights': 0},

    # Controller
    {'id': 18, 'name': 'ליאור לוי', 'target_shifts': 5, 'max_shifts': 6, 'role': 'controller', 'history_streak': 0, 'max_mornings': 5, 'min_mornings': 0, 'max_evenings': 5, 'min_evenings': 0, 'max_nights': 5, 'min_nights': 0},

    # Supervisor
    {'id': 19, 'name': 'מיטל סבטן', 'target_shifts': 3, 'max_shifts': 4, 'role': 'supervisor', 'history_streak': 0, 'max_mornings': 5, 'min_mornings': 0, 'max_evenings': 5, 'min_evenings': 0, 'max_nights': 5, 'min_nights': 0},

    # Supervisor
    {'id': 20, 'name': 'מיכאל מורוזוב', 'target_shifts': 3, 'max_shifts': 4, 'role': 'supervisor', 'history_streak': 0, 'max_mornings': 5, 'min_mornings': 0, 'max_evenings': 5, 'min_evenings': 0, 'max_nights': 5, 'min_nights': 0},

    # Guard (Renamed)
    {'id': 21, 'name': 'מקס שמרטייב', 'target_shifts': 5, 'max_shifts': 6, 'role': 'guard', 'history_streak': 0, 'max_mornings': 5, 'min_mornings': 0, 'max_evenings': 5, 'min_evenings': 0, 'max_nights': 5, 'min_nights': 0},

    # Supervisor
    {'id': 22, 'name': 'מקסים ירחו', 'target_shifts': 5, 'max_shifts': 6, 'role': 'supervisor', 'history_streak': 0, 'max_mornings': 5, 'min_mornings': 0, 'max_evenings': 5, 'min_evenings': 0, 'max_nights': 5, 'min_nights': 0},

    # Supervisor (New)
    {'id': 23, 'name': 'מקסים פוגורלץ', 'target_shifts': 5, 'max_shifts': 6, 'role': 'supervisor', 'history_streak': 0, 'max_mornings': 5, 'min_mornings': 0, 'max_evenings': 5, 'min_evenings': 0, 'max_nights': 5, 'min_nights': 0},

    # Controller (New)
    {'id': 24, 'name': 'מקסים קרויטורו', 'target_shifts': 5, 'max_shifts': 6, 'role': 'controller', 'history_streak': 0, 'max_mornings': 5, 'min_mornings': 0, 'max_evenings': 5, 'min_evenings': 0, 'max_nights': 5, 'min_nights': 0},

    # Controller
    {'id': 25, 'name': 'נהוראי קדוש', 'target_shifts': 5, 'max_shifts': 6, 'role': 'controller', 'history_streak': 0, 'max_mornings': 5, 'min_mornings': 0, 'max_evenings': 5, 'min_evenings': 0, 'max_nights': 5, 'min_nights': 0},

    # Guard
    {'id': 26, 'name': 'ניר תורגמן', 'target_shifts': 4, 'max_shifts': 4, 'role': 'guard', 'history_streak': 0, 'max_mornings': 5, 'min_mornings': 0, 'max_evenings': 5, 'min_evenings': 0, 'max_nights': 5, 'min_nights': 0},

    # Guard
    {'id': 27, 'name': 'סיוון בר סיני', 'target_shifts': 5, 'max_shifts': 6, 'role': 'guard', 'history_streak': 0, 'max_mornings': 5, 'min_mornings': 0, 'max_evenings': 5, 'min_evenings': 0, 'max_nights': 5, 'min_nights': 0},

    # Controller
    {'id': 28, 'name': 'עדי אוליאל', 'target_shifts': 3, 'max_shifts': 3, 'role': 'controller', 'history_streak': 0, 'max_mornings': 5, 'min_mornings': 0, 'max_evenings': 5, 'min_evenings': 0, 'max_nights': 5, 'min_nights': 0},

    # Guard
    {'id': 29, 'name': 'עומר בוזגלו', 'target_shifts': 5, 'max_shifts': 6, 'role': 'guard', 'history_streak': 0, 'max_mornings': 5, 'min_mornings': 0, 'max_evenings': 5, 'min_evenings': 0, 'max_nights': 5, 'min_nights': 0},

    # Controller (New)
    {'id': 30, 'name': 'קרן אור בלמוט', 'target_shifts': 3, 'max_shifts': 4, 'role': 'controller', 'history_streak': 0, 'max_mornings': 5, 'min_mornings': 0, 'max_evenings': 5, 'min_evenings': 0, 'max_nights': 5, 'min_nights': 0},

    # Supervisor
    {'id': 31, 'name': 'רון פורמן', 'target_shifts': 5, 'max_shifts': 6, 'role': 'supervisor', 'history_streak': 0, 'max_mornings': 5, 'min_mornings': 0, 'max_evenings': 5, 'min_evenings': 0, 'max_nights': 5, 'min_nights': 0},

    # Guard (New)
    {'id': 32, 'name': 'רחלי וורקו', 'target_shifts': 5, 'max_shifts': 6, 'role': 'guard', 'history_streak': 0, 'max_mornings': 5, 'min_mornings': 0, 'max_evenings': 5, 'min_evenings': 0, 'max_nights': 5, 'min_nights': 0},

    # Controller
    {'id': 33, 'name': 'שגיב בן משה', 'target_shifts': 3, 'max_shifts': 4, 'role': 'controller', 'history_streak': 0, 'max_mornings': 5, 'min_mornings': 0, 'max_evenings': 5, 'min_evenings': 0, 'max_nights': 5, 'min_nights': 0},

    # Guard
    {'id': 34, 'name': 'שגיב חליוה', 'target_shifts': 3, 'max_shifts': 4, 'role': 'guard', 'history_streak': 0, 'max_mornings': 5, 'min_mornings': 0, 'max_evenings': 5, 'min_evenings': 0, 'max_nights': 5, 'min_nights': 0},

    # Supervisor
    {'id': 35, 'name': 'שלמה יסיאס', 'target_shifts': 5, 'max_shifts': 6, 'role': 'supervisor', 'history_streak': 0, 'max_mornings': 5, 'min_mornings': 0, 'max_evenings': 5, 'min_evenings': 0, 'max_nights': 5, 'min_nights': 0},

    # Guard
    {'id': 36, 'name': 'שקד איתן', 'target_shifts': 5, 'max_shifts': 6, 'role': 'guard', 'history_streak': 0, 'max_mornings': 5, 'min_mornings': 0, 'max_evenings': 5, 'min_evenings': 0, 'max_nights': 5, 'min_nights': 0},
]

EMPLOYEE_COLORS = [
    # Adjusted for 36 Employees
    'FF9999', '99FF99', '9999FF', 'FFFF99', 'FFCC99', 'FF99FF', '99FFFF', 'CCCCCC', '87CEFA', 'E6B8B7',
    'D8BFD8', 'FFD700', 'ADFF2F', 'FFA07A', '20B2AA', '778899', 'B0C4DE', 'FFFACD', 'E0FFFF', 'F4A460',
    '9370DB', '3CB371', '7B68EE', '00FA9A', '48D1CC', 'C71585', 'FFE4E1', 'FFE4B5', 'FFDEAD', '98FB98',
    'AFEEEE', 'DB7093', 'FFEFD5', 'FFDAB9', 'DDA0DD', 'B0E0E6'
]

# ==========================================
#         Constraints & Context
# ==========================================

# Previous Week Context
WORKED_LAST_SAT_NOON = [0, 4]  # Example:
WORKED_LAST_SAT_NIGHT = [1, 5]  # Example:

# Manual Assignments (Force Shift)
MANUAL_ASSIGNMENTS = [
]

# Manual Unavailability Requests
# Format: (Employee ID, Day 0-6, Shift 0-3)
MANUAL_REQUESTS = [
    # ID 0 - אביב קוברין (All Week Unavailable)
    (0, 0, 0), (0, 0, 1), (0, 0, 2), (0, 0, 3),  # Sunday (18/1)
    (0, 1, 0), (0, 1, 1), (0, 1, 2), (0, 1, 3),  # Monday (19/1)
    (0, 2, 0), (0, 2, 1), (0, 2, 2), (0, 2, 3),  # Tuesday (20/1)
    (0, 3, 0), (0, 3, 1), (0, 3, 2), (0, 3, 3),  # Wednesday (21/1)
    (0, 4, 0), (0, 4, 1), (0, 4, 2), (0, 4, 3),  # Thursday (22/1)
    (0, 5, 0), (0, 5, 1), (0, 5, 2), (0, 5, 3),  # Friday (23/1)
    (0, 6, 0), (0, 6, 1), (0, 6, 2), (0, 6, 3),  # Saturday (24/1)

    # ID 1
    (1, 4, 2),  # Thursday (22/1) - Night unavailable
    (1, 5, 0), (1, 5, 3), (1, 5, 1), (1, 5, 2),  # Friday (23/1) - All shifts unavailable
    (1, 6, 3), (1, 6, 1), (1, 6, 2),  # Saturday (24/1) - Long Morning, Evening & Night unavailable

    # ID 2 - אוריאל כהן
    (2, 0, 0), (2, 0, 3), (2, 0, 2),  # Sunday (18/1)
    (2, 1, 0), (2, 1, 2),  # Monday (19/1)
    (2, 2, 0), (2, 2, 3), (2, 2, 2),  # Tuesday (20/1)
    (2, 3, 0), (2, 3, 3), (2, 3, 2),  # Wednesday (21/1)
    (2, 4, 2),  # Thursday (22/1)

    # ID 3 - איתי בכר
    (3, 0, 0), (3, 0, 3), (3, 0, 1), (3, 0, 2),  # Sunday (18/1)
    (3, 1, 2),  # Monday (19/1)
    (3, 2, 0), (3, 2, 3), (3, 2, 1), (3, 2, 2),  # Tuesday (20/1)
    (3, 3, 2),  # Wednesday (21/1)
    (3, 4, 2),  # Thursday (22/1)
    (3, 5, 3), (3, 5, 1),  # Friday (23/1)
    (3, 6, 2),  # Saturday (24/1)

    # ID 4 - אלון אבשלומוב
    (4, 0, 0), (4, 0, 3), (4, 0, 1),  # Sunday (18/1)
    (4, 1, 0), (4, 1, 3), (4, 1, 1),  # Monday (19/1)
    (4, 2, 0), (4, 2, 3), (4, 2, 1),  # Tuesday (20/1)
    (4, 3, 0), (4, 3, 3),  # Wednesday (21/1)
    (4, 5, 3), (4, 5, 1),  # Friday (23/1)

# ID 5 - אליאב דגו
    (5,0,0), (5,0,3), (5,0,1),
    (5, 1, 0), (5, 1, 3), (5, 1, 1), # Monday (19/1)
    (5, 2, 0), (5, 2, 3), (5, 2, 1), # Tuesday (20/1)
    (5, 3, 0), (5, 3, 3), (5, 3, 1), # Wednesday (21/1)
    (5, 4, 0), (5, 4, 3), (5, 4, 1), # Thursday (22/1)
    (5, 5, 0), (5, 5, 3), (5, 5, 1), # Friday (23/1)
    (5, 6, 0), (5, 6, 3), (5, 6, 1), # Saturday (24/1)

# ID 6 - אנגלינה אגפונוב
    (6, 0, 3), # Sunday (18/1)
    (6, 1, 3), # Monday (19/1)
    (6, 3, 3), # Wednesday (21/1)
    (6, 4, 1), # Thursday (22/1)
    (6, 5, 0), (6, 5, 3), (6, 5, 2), # Friday (23/1)
    (6, 6, 2), # Saturday (24/1)

# ID 7 - אסתר מנגיסטו
    (7, 1, 3), (7, 1, 1), (7, 1, 2), # Monday (19/1)
    (7, 2, 0), (7, 2, 3), (7, 2, 1), (7, 2, 2), # Tuesday (20/1)
    (7, 3, 3), (7, 3, 1), # Wednesday (21/1)

# ID 8 - אשגרה קסה
    (8, 0, 2), # Sunday (18/1)
    (8, 1, 0), (8, 1, 3), (8, 1, 2), # Monday (19/1)
    (8, 2, 0), (8, 2, 3), # Tuesday (20/1)
    (8, 3, 0), (8, 3, 3), (8, 3, 1), (8, 3, 2), # Wednesday (21/1)
    (8, 5, 2), # Friday (23/1)
    (8, 6, 0), (8, 6, 3), (8, 6, 1), (8, 6, 2), # Saturday (24/1)

# ID 9 - בן שפטר
    (9, 0, 0), (9, 0, 3), (9, 0, 1), # Sunday (18/1)
    (9, 1, 0), (9, 1, 3), # Monday (19/1)
    (9, 2, 0), (9, 2, 3), (9, 2, 1), # Tuesday (20/1)
    (9, 3, 1), (9, 3, 2), # Wednesday (21/1)
    (9, 4, 0), (9, 4, 3), (9, 4, 2), # Thursday (22/1)
    (9, 5, 0), (9, 5, 3), (9, 5, 1), (9, 5, 2), # Friday (23/1)
    (9, 6, 0), (9, 6, 3), (9, 6, 2), # Saturday (24/1)

    # ID 11 - בר פרויליך
    (11, 0, 0), (11, 0, 3), (11, 0, 1), (11, 0, 2), # Sunday (18/1)
    (11, 2, 0), (11, 2, 3), (11, 2, 1), # Tuesday (20/1)
    (11, 3, 3), # Wednesday (21/1)
    (11, 4, 1), # Thursday (22/1)
    (11, 5, 0), (11, 5, 3), (11, 5, 1), # Friday (23/1)
    (11, 6, 3), # Saturday (24/1)

    # ID 13 - דן מיכאל צ'לרו
    (13, 0, 0), (13, 0, 3), # Sunday (18/1)
    (13, 3, 3), (13, 3, 1), # Wednesday (21/1)
    (13, 5, 0), (13, 5, 3), # Friday (23/1)

    # ID 12 - דוד ניסנוב
    (12, 0, 0), (12, 0, 3), (12, 0, 1), (12, 0, 2), # Sunday (18/1)
    (12, 2, 3), # Tuesday (20/1)
    (12, 3, 3), (12, 3, 1), (12, 3, 2), # Wednesday (21/1)
    (12, 4, 0), (12, 4, 3), (12, 4, 1), (12, 4, 2), # Thursday (22/1)
    (12, 5, 0), (12, 5, 3), # Friday (23/1)
    (12, 6, 3), (12, 6, 2), # Saturday (24/1)

    # ID 10 - בן שרעבי
    (10, 0, 0), (10, 0, 3), (10, 0, 1), # Sunday (18/1)
    (10, 2, 0), (10, 2, 3), # Tuesday (20/1)
    (10, 3, 0), (10, 3, 3), (10, 3, 1), # Wednesday (21/1)

# ID 14 - יבגני קנייב
    (14, 0, 0), (14, 0, 3), (14, 0, 2), # Sunday (18/1)
    (14, 1, 0), (14, 1, 3),             # Monday (19/1)
    (14, 2, 1), (14, 2, 2),             # Tuesday (20/1)
    (14, 3, 3), (14, 3, 1), (14, 3, 2), # Wednesday (21/1)
    (14, 4, 0), (14, 4, 3), (14, 4, 1), # Thursday (22/1)
    (14, 5, 0), (14, 5, 2),             # Friday (23/1)
    (14, 6, 2),                         # Saturday (24/1)

    # ID 17 - לי פז
    (17, 0, 0), (17, 0, 3), (17, 0, 1), # Sunday (18/1)
    (17, 1, 2),                         # Monday (19/1)
    (17, 2, 0), (17, 2, 3), (17, 2, 1), (17, 2, 2), # Tuesday (20/1)
    (17, 3, 0), (17, 3, 3), (17, 3, 1), (17, 3, 2), # Wednesday (21/1)
    (17, 4, 2),                         # Thursday (22/1)
    (17, 5, 3), (17, 5, 1), (17, 5, 2), # Friday (23/1)
    (17, 6, 0), (17, 6, 3), (17, 6, 1), (17, 6, 2), # Saturday (24/1)

    # ID 18 - ליאור לוי
    (18, 0, 0), (18, 0, 3), (18, 0, 2), # Sunday (18/1)
    (18, 1, 2),                         # Monday (19/1)
    (18, 2, 1), (18, 2, 2),             # Tuesday (20/1)
    (18, 4, 0), (18, 4, 3), (18, 4, 1), (18, 4, 2), # Thursday (22/1)
    (18, 5, 0), (18, 5, 3), (18, 5, 1), (18, 5, 2), # Friday (23/1)

    # ID 16 - יניר דחוח
    (16, 0, 0), (16, 0, 3),             # Sunday (18/1)
    (16, 2, 0), (16, 2, 3),             # Tuesday (20/1)
    (16, 3, 0), (16, 3, 3), (16, 3, 2), # Wednesday (21/1)
    (16, 4, 0), (16, 4, 3), (16, 4, 1), (16, 4, 2), # Thursday (22/1)
    (16, 5, 0), (16, 5, 3), (16, 5, 1), (16, 5, 2), # Friday (23/1)
    (16, 6, 0), (16, 6, 3),             # Saturday (24/1)

    # ID 15 - יובל קורן
    (15, 0, 0), (15, 0, 3), (15, 0, 1), (15, 0, 2), # Sunday (18/1)
    (15, 1, 0), (15, 1, 3), (15, 1, 1), # Monday (19/1)
    (15, 2, 2),                         # Tuesday (20/1)
    (15, 3, 0), (15, 3, 3), (15, 3, 1), (15, 3, 2), # Wednesday (21/1)
    (15, 4, 0), (15, 4, 3), (15, 4, 1), # Thursday (22/1)
    (15, 6, 2),                         # Saturday (24/1)

# ID 19 - מיטל סבטן
    (19, 0, 0), (19, 0, 3), (19, 0, 1), (19, 0, 2), # Sunday (18/1)
    (19, 1, 0), (19, 1, 3),                         # Monday (19/1)
    (19, 2, 2),                                     # Tuesday (20/1)
    (19, 3, 0), (19, 3, 3), (19, 3, 1), (19, 3, 2), # Wednesday (21/1)
    (19, 4, 2),                                     # Thursday (22/1)
    (19, 5, 0), (19, 5, 3), (19, 5, 1), (19, 5, 2), # Friday (23/1)
    (19, 6, 2),                                     # Saturday (24/1)

    # ID 23 - מקסים פוגורלץ
    (23, 0, 0), (23, 0, 3), (23, 0, 1), (23, 0, 2), # Sunday (18/1)
    (23, 1, 0), (23, 1, 3), (23, 1, 1), (23, 1, 2), # Monday (19/1)
    (23, 2, 0), (23, 2, 3), (23, 2, 1), (23, 2, 2), # Tuesday (20/1)
    (23, 3, 0), (23, 3, 3), (23, 3, 1), (23, 3, 2), # Wednesday (21/1)
    (23, 4, 0), (23, 4, 3), (23, 4, 1), (23, 4, 2), # Thursday (22/1)
    # Friday & Saturday are fully available (Green)

    # ID 20 - מיכאל מורוזוב
    (20, 0, 0),                                     # Sunday (18/1)
    (20, 1, 0), (20, 1, 3), (20, 1, 1), (20, 1, 2), # Monday (19/1)
    (20, 2, 2),                                     # Tuesday (20/1)
    (20, 3, 0), (20, 3, 3), (20, 3, 1), (20, 3, 2), # Wednesday (21/1)
    (20, 4, 0), (20, 4, 3),                         # Thursday (22/1)
    (20, 5, 2),                                     # Friday (23/1)
    (20, 6, 2),                                     # Saturday (24/1)

    # ID 21 - מקס שמרטייב
    (21, 1, 0), (21, 1, 3), (21, 1, 1), (21, 1, 2), # Monday (19/1)
    (21, 3, 0), (21, 3, 3), (21, 3, 1), (21, 3, 2), # Wednesday (21/1)

# ID 25 - נהוראי קדוש
    (25, 0, 3), (25, 0, 1),             # Sunday (18/1)
    (25, 2, 3), (25, 2, 1),             # Tuesday (20/1)
    (25, 4, 3), (25, 4, 1),             # Thursday (22/1)
    (25, 5, 3), (25, 5, 1), (25, 5, 2), # Friday (23/1)
    (25, 6, 0), (25, 6, 3), (25, 6, 1), (25, 6, 2), # Saturday (24/1)

    # ID 29 - עומר בוזגלו
    (29, 0, 0), (29, 0, 3), (29, 0, 1), # Sunday (18/1)
    (29, 1, 3),                         # Monday (19/1)
    (29, 2, 3),                         # Tuesday (20/1)
    (29, 3, 3),                         # Wednesday (21/1)
    (29, 4, 3),                         # Thursday (22/1)
    (29, 5, 1),                         # Friday (23/1)

    # ID 30 - קרן אור בלמוט
    (30, 0, 0), (30, 0, 3), (30, 0, 1), # Sunday (18/1)
    (30, 1, 0), (30, 1, 3), (30, 1, 1), # Monday (19/1)
    (30, 2, 3), (30, 2, 1), (30, 2, 2), # Tuesday (20/1)
    (30, 3, 0), (30, 3, 3), (30, 3, 1), (30, 3, 2), # Wednesday (21/1)
    (30, 4, 3),                         # Thursday (22/1)
    (30, 6, 1), (30, 6, 2),             # Saturday (24/1)

    # ID 26 - ניר תורגמן
    (26, 0, 0), (26, 0, 3), (26, 0, 1), (26, 0, 2), # Sunday (18/1)
    (26, 1, 0), (26, 1, 3),             # Monday (19/1)
    (26, 2, 0), (26, 2, 3),             # Tuesday (20/1)
    (26, 3, 0), (26, 3, 3),             # Wednesday (21/1)
    (26, 5, 0), (26, 5, 3),             # Friday (23/1)
    (26, 6, 3),                         # Saturday (24/1)

    # ID 27 - סיוון בר סיני
    (27, 0, 3),                         # Sunday (18/1)
    (27, 2, 0), (27, 2, 3), (27, 2, 1), (27, 2, 2), # Tuesday (20/1)
    (27, 3, 0), (27, 3, 3), (27, 3, 1), (27, 3, 2), # Wednesday (21/1)
    (27, 4, 3), (27, 4, 2),             # Thursday (22/1)
    (27, 5, 0), (27, 5, 3), (27, 5, 1), (27, 5, 2), # Friday (23/1)
    (27, 6, 1), (27, 6, 2),             # Saturday (24/1)

    # ID 28 - עדי אוליאל
    (28, 0, 3), (28, 0, 2),             # Sunday (18/1)
    (28, 1, 0), (28, 1, 3), (28, 1, 1), (28, 1, 2), # Monday (19/1)
    (28, 2, 0), (28, 2, 3), (28, 2, 1), (28, 2, 2), # Tuesday (20/1)
    (28, 3, 0), (28, 3, 3), (28, 3, 1), (28, 3, 2), # Wednesday (21/1)
    (28, 6, 2),                         # Saturday (24/1)

    # ID 36 - שקד איתן (כל השבוע חסום)
    (36, 0, 0), (36, 0, 3), (36, 0, 1), (36, 0, 2),  # Sunday (18/1)
    (36, 1, 0), (36, 1, 3), (36, 1, 1), (36, 1, 2),  # Monday (19/1)
    (36, 2, 0), (36, 2, 3), (36, 2, 1), (36, 2, 2),  # Tuesday (20/1)
    (36, 3, 0), (36, 3, 3), (36, 3, 1), (36, 3, 2),  # Wednesday (21/1)
    (36, 4, 0), (36, 4, 3), (36, 4, 1), (36, 4, 2),  # Thursday (22/1)
    (36, 5, 0), (36, 5, 3), (36, 5, 1), (36, 5, 2),  # Friday (23/1)
    (36, 6, 0), (36, 6, 3), (36, 6, 1), (36, 6, 2),  # Saturday (24/1)

    # ID 32 - רחלי וורקו
    (32, 1, 3), (32, 1, 1),  # Monday (19/1)
    (32, 2, 0), (32, 2, 3), (32, 2, 1),  # Tuesday (20/1)
    (32, 3, 2),  # Wednesday (21/1)
    (32, 4, 0), (32, 4, 3), (32, 4, 1),  # Thursday (22/1)

    # ID 33 - שגיב בן משה
    (33, 0, 1), (33, 0, 2),  # Sunday (18/1)
    (33, 1, 1), (33, 1, 2),  # Monday (19/1)
    (33, 3, 1), (33, 3, 2),  # Wednesday (21/1)
    (33, 4, 1), (33, 4, 2),  # Thursday (22/1)
    (33, 6, 2),  # Saturday (24/1)

    # ID 35 - שלמה יסיאס
    (35, 0, 0), (35, 0, 3),  # Sunday (18/1)
    (35, 1, 0), (35, 1, 3),  # Monday (19/1)
    (35, 2, 3),  # Tuesday (20/1)
    (35, 4, 0), (35, 4, 3),  # Thursday (22/1)
    (35, 5, 3),  # Friday (23/1)
    (35, 6, 0), (35, 6, 3), (35, 6, 1), (35, 6, 2),  # Saturday (24/1)

    # ID 31 - רון פורמן
    (31, 0, 1),  # Sunday (18/1)
    (31, 1, 0), (31, 1, 3),  # Monday (19/1)
    (31, 2, 0), (31, 2, 3),  # Tuesday (20/1)
    (31, 3, 0), (31, 3, 3),  # Wednesday (21/1)
    (31, 5, 1),  # Friday (23/1)

    # ID 34 - שגיב חליוה
    (34, 0, 0), (34, 0, 3), (34, 0, 1), (34, 0, 2),  # Sunday (18/1)
    (34, 1, 0), (34, 1, 3), (34, 1, 1), (34, 1, 2),  # Monday (19/1)
    (34, 2, 0), (34, 2, 3), (34, 2, 1), (34, 2, 2),  # Tuesday (20/1)
    (34, 4, 0), (34, 4, 3), (34, 4, 1), (34, 4, 2),  # Thursday (22/1)
    (34, 5, 3), (34, 5, 2),  # Friday (23/1)
    (34, 6, 3), (34, 6, 2),  # Saturday (24/1)
]