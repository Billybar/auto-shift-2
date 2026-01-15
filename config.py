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
    'MAX_SHIFTS': 60,
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
    # Supervisors
    # role_priority: Default is 5. Higher value = Stricter adherence to role ratio.
    {'name': 'אביב קוברין', 'target_shifts': 4, 'max_shifts': 4, 'role': 'supervisor', 'role_priority': 20, 'history_streak': 0, 'max_mornings': 0, 'min_mornings': 0, 'max_evenings': 0, 'min_evenings': 0, 'max_nights': 2, 'min_nights': 0},
    {'name': 'אברהם טגניה', 'target_shifts': 5, 'max_shifts': 6, 'role': 'supervisor', 'role_priority': 5, 'history_streak': 0, 'max_mornings': 0, 'min_mornings': 0, 'max_evenings': 0, 'min_evenings': 0, 'max_nights': 2, 'min_nights': 0},
    {'name': 'איתי בכר', 'target_shifts': 5, 'max_shifts': 6, 'role': 'supervisor', 'role_priority': 5, 'history_streak': 0, 'max_mornings': 0, 'min_mornings': 0, 'max_evenings': 0, 'min_evenings': 0, 'max_nights': 2, 'min_nights': 0},
    {'name': 'דן מיכאל צלרו', 'target_shifts': 5, 'max_shifts': 6, 'role': 'supervisor', 'role_priority': 5, 'history_streak': 0, 'max_mornings': 0, 'min_mornings': 0, 'max_evenings': 0, 'min_evenings': 0, 'max_nights': 2, 'min_nights': 0},
    {'name': 'יהודה ענאקי', 'target_shifts': 3, 'max_shifts': 4, 'role': 'supervisor', 'role_priority': 5, 'history_streak': 0, 'max_mornings': 0, 'min_mornings': 0, 'max_evenings': 0, 'min_evenings': 0, 'max_nights': 2, 'min_nights': 0},
    {'name': 'מיטל סבטן', 'target_shifts': 3, 'max_shifts': 3, 'role': 'supervisor', 'role_priority': 5, 'history_streak': 0, 'max_mornings': 0, 'min_mornings': 0, 'max_evenings': 0, 'min_evenings': 0, 'max_nights': 2, 'min_nights': 0},
    {'name': 'מיכאל מורוזוב', 'target_shifts': 3, 'max_shifts': 4, 'role': 'supervisor', 'role_priority': 5, 'history_streak': 0, 'max_mornings': 0, 'min_mornings': 0, 'max_evenings': 0, 'min_evenings': 0, 'max_nights': 2, 'min_nights': 0},
    {'name': 'מקסים ירחו', 'target_shifts': 5, 'max_shifts': 6, 'role': 'supervisor', 'role_priority': 5, 'history_streak': 0, 'max_mornings': 0, 'min_mornings': 0, 'max_evenings': 0, 'min_evenings': 0, 'max_nights': 2, 'min_nights': 0},
    {'name': 'רון פורמן', 'target_shifts': 5, 'max_shifts': 6, 'role': 'supervisor', 'role_priority': 5, 'history_streak': 0, 'max_mornings': 0, 'min_mornings': 0, 'max_evenings': 0, 'min_evenings': 0, 'max_nights': 2, 'min_nights': 0},
    {'name': 'שלמה יסיאס', 'target_shifts': 3, 'max_shifts': 3, 'role': 'supervisor', 'role_priority': 5, 'history_streak': 0, 'max_mornings': 0, 'min_mornings': 0, 'max_evenings': 0, 'min_evenings': 0, 'max_nights': 2, 'min_nights': 0},

    # Controllers
    {'name': 'דוד ניסנוב', 'target_shifts': 4, 'max_shifts': 4, 'role': 'controller', 'history_streak': 0, 'max_mornings': 0, 'min_mornings': 0, 'max_evenings': 0, 'min_evenings': 0, 'max_nights': 2, 'min_nights': 0},
    {'name': 'עדי אוליאל', 'target_shifts': 3, 'max_shifts': 3, 'role': 'controller', 'history_streak': 0, 'max_mornings': 0, 'min_mornings': 0, 'max_evenings': 0, 'min_evenings': 0, 'max_nights': 2, 'min_nights': 0},
    {'name': 'שגיב בן משה', 'target_shifts': 3, 'max_shifts': 4, 'role': 'controller', 'history_streak': 0, 'max_mornings': 0, 'min_mornings': 0, 'max_evenings': 0, 'min_evenings': 0, 'max_nights': 2, 'min_nights': 0},

    # Guards (Existing & New)
    {'name': 'אדגו פנטייה', 'target_shifts': 5, 'max_shifts': 6, 'role': 'guard', 'history_streak': 0, 'max_mornings': 0, 'min_mornings': 0, 'max_evenings': 0, 'min_evenings': 0, 'max_nights': 2, 'min_nights': 0},
    {'name': 'אופיר מנחם', 'target_shifts': 3, 'max_shifts': 3, 'role': 'guard', 'history_streak': 0, 'max_mornings': 0, 'min_mornings': 0, 'max_evenings': 0, 'min_evenings': 0, 'max_nights': 2, 'min_nights': 0},
    {'name': 'אוריאל כהן', 'target_shifts': 3, 'max_shifts': 4, 'role': 'guard', 'history_streak': 0, 'max_mornings': 0, 'min_mornings': 0, 'max_evenings': 0, 'min_evenings': 0, 'max_nights': 2, 'min_nights': 0},
    {'name': 'אלון אבשלומו', 'target_shifts': 3, 'max_shifts': 4, 'role': 'guard', 'history_streak': 0, 'max_mornings': 0, 'min_mornings': 0, 'max_evenings': 0, 'min_evenings': 0, 'max_nights': 2, 'min_nights': 0},
    {'name': 'אליאב דגו', 'target_shifts': 5, 'max_shifts': 6, 'role': 'guard', 'history_streak': 0, 'max_mornings': 0, 'min_mornings': 0, 'max_evenings': 0, 'min_evenings': 0, 'max_nights': 2, 'min_nights': 0},
    {'name': 'ארתור ארנוביץ', 'target_shifts': 4, 'max_shifts': 4, 'role': 'guard', 'history_streak': 0, 'max_mornings': 0, 'min_mornings': 0, 'max_evenings': 0, 'min_evenings': 0, 'max_nights': 2, 'min_nights': 0},
    {'name': 'בן שפטר', 'target_shifts': 5, 'max_shifts': 6, 'role': 'guard', 'history_streak': 0, 'max_mornings': 0, 'min_mornings': 0, 'max_evenings': 0, 'min_evenings': 0, 'max_nights': 2, 'min_nights': 0},
    {'name': 'בן שרעבי', 'target_shifts': 5, 'max_shifts': 6, 'role': 'guard', 'history_streak': 0, 'max_mornings': 0, 'min_mornings': 0, 'max_evenings': 0, 'min_evenings': 0, 'max_nights': 2, 'min_nights': 0},
    {'name': 'בר גובשייבץ', 'target_shifts': 5, 'max_shifts': 6, 'role': 'guard', 'history_streak': 0, 'max_mornings': 0, 'min_mornings': 0, 'max_evenings': 0, 'min_evenings': 0, 'max_nights': 2, 'min_nights': 0},
    {'name': 'בר פרויליך', 'target_shifts': 3, 'max_shifts': 3, 'role': 'guard', 'history_streak': 0, 'max_mornings': 0, 'min_mornings': 0, 'max_evenings': 0, 'min_evenings': 0, 'max_nights': 2, 'min_nights': 0},
    {'name': 'יובל קורן', 'target_shifts': 3, 'max_shifts': 3, 'role': 'guard', 'history_streak': 0, 'max_mornings': 0, 'min_mornings': 0, 'max_evenings': 0, 'min_evenings': 0, 'max_nights': 2, 'min_nights': 0},
    {'name': 'יניר דוחו', 'target_shifts': 3, 'max_shifts': 4, 'role': 'guard', 'history_streak': 0, 'max_mornings': 0, 'min_mornings': 0, 'max_evenings': 0, 'min_evenings': 0, 'max_nights': 2, 'min_nights': 0},
    {'name': 'יעל אזיזוב', 'target_shifts': 5, 'max_shifts': 6, 'role': 'guard', 'history_streak': 0, 'max_mornings': 0, 'min_mornings': 0, 'max_evenings': 0, 'min_evenings': 0, 'max_nights': 2, 'min_nights': 0},
    {'name': 'לי פז', 'target_shifts': 3, 'max_shifts': 4, 'role': 'guard', 'history_streak': 0, 'max_mornings': 0, 'min_mornings': 0, 'max_evenings': 0, 'min_evenings': 0, 'max_nights': 2, 'min_nights': 0},
    {'name': 'ליאור לוי', 'target_shifts': 3, 'max_shifts': 4, 'role': 'guard', 'history_streak': 0, 'max_mornings': 0, 'min_mornings': 0, 'max_evenings': 0, 'min_evenings': 0, 'max_nights': 2, 'min_nights': 0},
    {'name': 'מקסים שמרטייב', 'target_shifts': 5, 'max_shifts': 6, 'role': 'guard', 'history_streak': 0, 'max_mornings': 0, 'min_mornings': 0, 'max_evenings': 0, 'min_evenings': 0, 'max_nights': 2, 'min_nights': 0},
    {'name': 'נהוראי קדוש', 'target_shifts': 5, 'max_shifts': 6, 'role': 'guard', 'history_streak': 0, 'max_mornings': 0, 'min_mornings': 0, 'max_evenings': 0, 'min_evenings': 0, 'max_nights': 2, 'min_nights': 0},
    {'name': 'ניר תורגמן', 'target_shifts': 4, 'max_shifts': 4, 'role': 'guard', 'history_streak': 0, 'max_mornings': 0, 'min_mornings': 0, 'max_evenings': 0, 'min_evenings': 0, 'max_nights': 2, 'min_nights': 0},
    {'name': 'סיוון בר סיני', 'target_shifts': 5, 'max_shifts': 6, 'role': 'guard', 'history_streak': 0, 'max_mornings': 0, 'min_mornings': 0, 'max_evenings': 0, 'min_evenings': 0, 'max_nights': 2, 'min_nights': 0},
    {'name': 'עומר בוזגלו', 'target_shifts': 3, 'max_shifts': 4, 'role': 'guard', 'history_streak': 0, 'max_mornings': 0, 'min_mornings': 0, 'max_evenings': 0, 'min_evenings': 0, 'max_nights': 2, 'min_nights': 0},
    {'name': 'עמית מנור', 'target_shifts': 5, 'max_shifts': 6, 'role': 'guard', 'history_streak': 0, 'max_mornings': 0, 'min_mornings': 0, 'max_evenings': 0, 'min_evenings': 0, 'max_nights': 2, 'min_nights': 0},
    {'name': 'שגיב חליווה', 'target_shifts': 5, 'max_shifts': 6, 'role': 'guard', 'history_streak': 0, 'max_mornings': 0, 'min_mornings': 0, 'max_evenings': 0, 'min_evenings': 0, 'max_nights': 2, 'min_nights': 0},
    {'name': 'שקד איתן', 'target_shifts': 5, 'max_shifts': 6, 'role': 'guard', 'history_streak': 0, 'max_mornings': 0, 'min_mornings': 0, 'max_evenings': 0, 'min_evenings': 0, 'max_nights': 2, 'min_nights': 0},
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
WORKED_LAST_SAT_NOON = [0, 4]  # Example: Ira and Gadi
WORKED_LAST_SAT_NIGHT = [1, 5]  # Example: Asaf, Dolev

# Manual Assignments (Force Shift)
MANUAL_ASSIGNMENTS = [
]

# Manual Unavailability Requests
# Format: (Employee ID, Day 0-6, Shift 0-2)
MANUAL_REQUESTS = [
    (0, 1, 0), (0, 1, 1), (0, 1, 3), (0, 2, 2), (0, 2, 3), (0, 6, 0), (0, 6, 1),
    (1, 0, 2), (1, 1, 0), (1, 1, 3), (1, 3, 1), (1, 5, 0), (1, 5, 1), (1, 6, 0),
    (2, 0, 0), (2, 1, 1), (2, 1, 2), (2, 2, 1), (2, 3, 2), (2, 4, 0), (2, 6, 0),
    (3, 0, 1), (3, 0, 2), (3, 1, 1), (3, 2, 2), (3, 3, 1), (3, 4, 1), (3, 5, 2),
    (4, 0, 2), (4, 3, 3), (4, 4, 1), (4, 4, 3), (4, 6, 0), (4, 6, 2), (4, 6, 3),
    (5, 0, 0), (5, 2, 0), (5, 4, 0), (5, 4, 3), (5, 5, 1), (5, 5, 2), (5, 5, 3),
    (6, 0, 0), (6, 1, 0), (6, 1, 1), (6, 2, 3), (6, 3, 0), (6, 3, 3), (6, 4, 3),
    (7, 0, 2), (7, 1, 0), (7, 3, 3), (7, 4, 0), (7, 4, 2), (7, 6, 0), (7, 6, 1),
    (8, 0, 2), (8, 1, 3), (8, 2, 3), (8, 3, 0), (8, 3, 1), (8, 3, 3), (8, 4, 0),
    (9, 1, 2), (9, 3, 0), (9, 3, 2), (9, 3, 3), (9, 4, 0), (9, 4, 2), (9, 4, 3),
    (10, 1, 1), (10, 2, 1), (10, 3, 0), (10, 3, 2), (10, 3, 3), (10, 4, 2), (10, 6, 2),
    (11, 0, 3), (11, 1, 0), (11, 1, 2), (11, 2, 1), (11, 3, 2), (11, 4, 2), (11, 5, 3),
    (12, 2, 2), (12, 3, 2), (12, 3, 3), (12, 4, 0), (12, 6, 0), (12, 6, 1), (12, 6, 3),
    (13, 0, 3), (13, 1, 3), (13, 2, 1), (13, 2, 2), (13, 3, 2), (13, 5, 2), (13, 6, 2),
    (14, 0, 1), (14, 1, 0), (14, 1, 3), (14, 2, 2), (14, 6, 0), (14, 6, 2), (14, 6, 3),
    (15, 0, 2), (15, 2, 0), (15, 2, 2), (15, 4, 2), (15, 5, 0), (15, 5, 3), (15, 6, 1),
    (16, 0, 0), (16, 1, 1), (16, 2, 1), (16, 3, 0), (16, 5, 1), (16, 6, 0), (16, 6, 3),
    (17, 2, 0), (17, 2, 3), (17, 4, 1), (17, 4, 2), (17, 4, 3), (17, 6, 1), (17, 6, 2),
    (18, 2, 1), (18, 2, 2), (18, 2, 3), (18, 3, 1), (18, 3, 2), (18, 5, 1), (18, 5, 2),
    (19, 2, 2), (19, 3, 2), (19, 4, 0), (19, 4, 1), (19, 4, 3), (19, 5, 1), (19, 6, 2),
    (20, 0, 1), (20, 2, 3), (20, 3, 1), (20, 3, 2), (20, 3, 3), (20, 5, 1), (20, 6, 3),
    (21, 0, 1), (21, 1, 0), (21, 2, 0), (21, 2, 1), (21, 4, 3), (21, 5, 0), (21, 5, 3),
    (22, 0, 0), (22, 1, 2), (22, 1, 3), (22, 3, 3), (22, 4, 1), (22, 5, 1), (22, 6, 0),
    (23, 0, 1), (23, 1, 3), (23, 2, 1), (23, 3, 2), (23, 5, 2), (23, 6, 0), (23, 6, 1),
    (24, 2, 3), (24, 3, 2), (24, 3, 3), (24, 4, 3), (24, 5, 0), (24, 5, 2), (24, 6, 0),
    (25, 1, 2), (25, 3, 3), (25, 4, 3), (25, 5, 0), (25, 5, 2), (25, 5, 3), (25, 6, 0),
    (26, 0, 0), (26, 0, 1), (26, 1, 1), (26, 1, 3), (26, 4, 1), (26, 5, 3), (26, 6, 3),
    (27, 1, 1), (27, 1, 2), (27, 2, 3), (27, 3, 2), (27, 3, 3), (27, 5, 3), (27, 6, 0),
    (28, 0, 1), (28, 1, 1), (28, 2, 1), (28, 2, 2), (28, 5, 1), (28, 5, 3), (28, 6, 3),
    (29, 0, 3), (29, 1, 1), (29, 1, 3), (29, 5, 0), (29, 5, 1), (29, 6, 1), (29, 6, 2),
    (30, 0, 0), (30, 1, 2), (30, 1, 3), (30, 2, 0), (30, 2, 1), (30, 3, 3), (30, 5, 1),
    (31, 0, 0), (31, 0, 1), (31, 1, 0), (31, 1, 3), (31, 5, 0), (31, 5, 2), (31, 6, 1),
    (32, 0, 1), (32, 1, 1), (32, 1, 3), (32, 2, 3), (32, 5, 1), (32, 5, 2), (32, 6, 3),
    (33, 0, 0), (33, 0, 3), (33, 2, 0), (33, 2, 1), (33, 3, 0), (33, 5, 1), (33, 5, 2),
    (34, 0, 1), (34, 0, 2), (34, 2, 0), (34, 2, 1), (34, 2, 3), (34, 3, 1), (34, 6, 1),
    (35, 0, 1), (35, 0, 2), (35, 0, 3), (35, 1, 3), (35, 3, 0), (35, 4, 1), (35, 4, 3),
]