# optimizer.py
from ortools.sat.python import cp_model
import config


# ============================================================================
# 1. Model Initialization & Variables
# ============================================================================
def _init_model_and_variables(employees, num_days, num_shifts):
    """
    Initializes the CP Model and creates the boolean variables grid.
    Returns: model, shift_vars (dict)
    """
    model = cp_model.CpModel()
    shift_vars = {}

    for e in range(len(employees)):
        for d in range(num_days):
            for s in range(num_shifts):
                shift_vars[(e, d, s)] = model.NewBoolVar(f'shift_{e}_{d}_{s}')

    return model, shift_vars


# ============================================================================
# 2. Hard Constraints: Role Demands
# ============================================================================
def _add_role_demand_constraints(model, shift_vars, employees, num_days, num_shifts):
    """
    Enforces that every shift has the required number of Guards, Controllers, and Supervisors.
    """
    weekend_days = [5, 6]

    # Helper: Group employees by role capabilities
    supervisors_idx = [i for i, emp in enumerate(employees) if emp.get('role') == 'supervisor']
    controllers_idx = [i for i, emp in enumerate(employees) if emp.get('role') == 'controller']

    # Combined group: Everyone capable of Controller duties (Controllers + Supervisors)
    capable_controller_idx = supervisors_idx + controllers_idx

    for d in range(num_days):
        daily_config = config.WEEKEND_DEMAND if d in weekend_days else config.WEEKDAY_DEMAND

        for s in range(num_shifts):
            # Retrieve specific shift requirements
            reqs = daily_config.get(s, {'guard': 0, 'controller': 0, 'supervisor': 0})
            req_guard = reqs.get('guard', 0)
            req_controller = reqs.get('controller', 0)
            req_supervisor = reqs.get('supervisor', 0)

            total_needed = req_guard + req_controller + req_supervisor

            # A. Total Headcount Constraint
            model.Add(sum(shift_vars[(e, d, s)] for e in range(len(employees))) == total_needed)

            # B. Supervisor Constraint (Strict)
            if req_supervisor > 0:
                model.Add(sum(shift_vars[(e, d, s)] for e in supervisors_idx) >= req_supervisor)

            # C. Skilled Workers Constraint (Controller + Supervisor coverage)
            needed_skilled = req_controller + req_supervisor
            if needed_skilled > 0:
                model.Add(sum(shift_vars[(e, d, s)] for e in capable_controller_idx) >= needed_skilled)


# ============================================================================
# 3. Hard Constraints: Shift Rules (Overlap & Spacing)
# ============================================================================
def _add_shift_rules_constraints(model, shift_vars, num_employees, num_days, num_shifts):
    """
    Enforces logical shift rules: No back-to-back shifts, no overlapping shifts.
    """
    # A. Prevent back-to-back shifts (Global check)
    total_slots = num_days * num_shifts
    for e in range(num_employees):
        for t in range(total_slots - 1):
            day, shift = t // num_shifts, t % num_shifts
            next_day, next_shift = (t + 1) // num_shifts, (t + 1) % num_shifts

            model.Add(shift_vars[(e, day, shift)] + shift_vars[(e, next_day, next_shift)] <= 1)

    # B. Reinforcement Shift Overlaps (Specific to this business logic)
    # Reinforcement (3) overlaps with Morning (0) and Noon (1)
    for e in range(num_employees):
        for d in range(num_days):
            # Conflict: Reinforcement vs Morning
            model.Add(shift_vars[(e, d, config.SHIFT_REINFORCEMENT)] +
                      shift_vars[(e, d, config.SHIFT_MORNING)] <= 1)
            # Conflict: Reinforcement vs Noon
            model.Add(shift_vars[(e, d, config.SHIFT_REINFORCEMENT)] +
                      shift_vars[(e, d, config.SHIFT_NOON)] <= 1)


# ============================================================================
# 4. Hard Constraints: Availability & Assignments
# ============================================================================
def _add_availability_constraints(model, shift_vars, employees, unavailable_requests,
                                  manual_assignments, worked_last_sat_noon, worked_last_sat_night):
    """
    Handles specific user requests, forced assignments, and history from previous week.
    """
    num_employees = len(employees)
    num_days = config.NUM_DAYS
    num_shifts = config.NUM_SHIFTS

    # A. Unavailable Requests (Manual + Image)
    for req in unavailable_requests:
        e, d, s = req
        if 0 <= e < num_employees and 0 <= d < num_days and 0 <= s < num_shifts:
            model.Add(shift_vars[(e, d, s)] == 0)

    # B. Previous Week Context (Rest Rules)
    for emp_id in worked_last_sat_night:
        if 0 <= emp_id < num_employees:
            # Cannot work Sunday Morning if worked Saturday Night
            model.Add(shift_vars[(emp_id, 0, 0)] == 0)

    # C. Manual Assignments (Force Shift)
    for assign in manual_assignments:
        e, d, s = assign
        if 0 <= e < num_employees and 0 <= d < num_days and 0 <= s < num_shifts:
            # Safety Check
            if (e, d, s) in unavailable_requests:
                name = employees[e]['name']
                raise ValueError(f"CRITICAL CONFLICT: {name} forced to (D:{d}, S:{s}) but marked unavailable.")

            model.Add(shift_vars[(e, d, s)] == 1)


def _add_labor_law_constraints(model, shift_vars, employees, num_days, num_shifts):
    """
    Enforces max consecutive work days (7-day streak prevention).
    """
    for e in range(len(employees)):
        work_days_vars = []
        for d in range(num_days):
            is_working = model.NewBoolVar(f'working_day_{e}_{d}')
            # Link shift_vars to is_working
            model.Add(sum(shift_vars[(e, d, s)] for s in range(num_shifts)) > 0).OnlyEnforceIf(is_working)
            model.Add(sum(shift_vars[(e, d, s)] for s in range(num_shifts)) == 0).OnlyEnforceIf(is_working.Not())
            work_days_vars.append(is_working)

        streak = employees[e].get('history_streak', 0)

        # If they already have a streak, limit the beginning of the week
        if streak > 0:
            limit = 7 - streak
            if limit <= num_days and limit > 0:
                model.Add(sum(work_days_vars[0:limit]) < limit)

        # Standard check within the current week
        if streak == 0:
            model.Add(sum(work_days_vars) < 7)


# ============================================================================
# 5. Soft Constraints (Objective Function)
# ============================================================================
def _build_objective_function(model, shift_vars, employees, num_days, num_shifts, worked_last_sat_noon,
                              worked_last_sat_night):
    """
    Constructs the objective function to minimize penalties (Balance, Fairness, Rest).
    """
    w = config.WEIGHTS
    objective_terms = []

    for e in range(len(employees)):
        # Gather shift lists for easy summing
        all_shifts = []
        morning_shifts = []
        evening_shifts = []
        night_shifts = []

        for d in range(num_days):
            morning_shifts.append(shift_vars[(e, d, 0)])
            evening_shifts.append(shift_vars[(e, d, 1)])
            night_shifts.append(shift_vars[(e, d, 2)])

            for s in range(num_shifts):
                all_shifts.append(shift_vars[(e, d, s)])

        # --- A. Min/Max Constraints (Soft) ---
        # Nights
        excess_nights = model.NewIntVar(0, 7, f'exc_night_{e}')
        shortage_nights = model.NewIntVar(0, 7, f'short_night_{e}')
        model.Add(sum(night_shifts) <= employees[e]['max_nights'] + excess_nights)
        model.Add(sum(night_shifts) + shortage_nights >= employees[e]['min_nights'])
        objective_terms.append(excess_nights * w['MAX_NIGHTS'])
        objective_terms.append(shortage_nights * w['MIN_NIGHTS'])

        # Mornings
        excess_morns = model.NewIntVar(0, 7, f'exc_morn_{e}')
        shortage_morns = model.NewIntVar(0, 7, f'short_morn_{e}')
        model.Add(sum(morning_shifts) <= employees[e]['max_mornings'] + excess_morns)
        model.Add(sum(morning_shifts) + shortage_morns >= employees[e]['min_mornings'])
        objective_terms.append(excess_morns * w['MAX_MORNINGS'])
        objective_terms.append(shortage_morns * w['MIN_MORNINGS'])

        # Evenings
        excess_evenings = model.NewIntVar(0, 7, f'exc_eve_{e}')
        shortage_evenings = model.NewIntVar(0, 7, f'short_eve_{e}')
        model.Add(sum(evening_shifts) <= employees[e]['max_evenings'] + excess_evenings)
        model.Add(sum(evening_shifts) + shortage_evenings >= employees[e]['min_evenings'])
        objective_terms.append(excess_evenings * w['MAX_EVENINGS'])

        # --- B. Consecutive Nights ---
        for d in range(num_days - 2):
            is_3_nights = model.NewBoolVar(f'3nights_{e}_{d}')
            # (Night D) AND (Night D+1) AND (Night D+2)
            model.AddBoolAnd([
                shift_vars[(e, d, 2)],
                shift_vars[(e, d + 1, 2)],
                shift_vars[(e, d + 2, 2)]
            ]).OnlyEnforceIf(is_3_nights)

            # Logic inversion for clean optimization
            model.AddBoolOr([
                shift_vars[(e, d, 2)].Not(),
                shift_vars[(e, d + 1, 2)].Not(),
                shift_vars[(e, d + 2, 2)].Not()
            ]).OnlyEnforceIf(is_3_nights.Not())

            objective_terms.append(is_3_nights * w['CONSECUTIVE_NIGHTS'])

        # --- C. Rest Gaps (Quick Turnarounds) ---
        # Avoid pattern: Work Shift X -> Skip 1 -> Work Shift Y (Too tight)
        total_slots = num_days * num_shifts
        for t in range(total_slots - 2):
            day, shift = t // num_shifts, t % num_shifts
            t2 = t + 2
            day2, shift2 = t2 // num_shifts, t2 % num_shifts

            bad_gap = model.NewBoolVar(f'bad_gap_{e}_{t}')
            model.AddBoolAnd([shift_vars[(e, day, shift)], shift_vars[(e, day2, shift2)]]).OnlyEnforceIf(bad_gap)
            model.AddBoolOr([shift_vars[(e, day, shift)].Not(), shift_vars[(e, day2, shift2)].Not()]).OnlyEnforceIf(
                bad_gap.Not())
            objective_terms.append(bad_gap * w['REST_GAP'])

        # Previous week gap penalties
        if e in worked_last_sat_noon:
            objective_terms.append(shift_vars[(e, 0, 0)] * w['REST_GAP'])
        if e in worked_last_sat_night:
            objective_terms.append(shift_vars[(e, 0, 1)] * w['REST_GAP'])

        # --- D. Target Shifts (Balance) ---
        total_worked = sum(all_shifts)
        target = employees[e]['target_shifts']

        # 1. Quadratic Penalty for deviation (Smoother distribution)
        delta = model.NewIntVar(0, 21, f'delta_target_{e}')
        model.Add(total_worked - target <= delta)
        model.Add(target - total_worked <= delta)

        delta_sq = model.NewIntVar(0, 400, f'delta_sq_{e}')
        model.AddMultiplicationEquality(delta_sq, [delta, delta])
        objective_terms.append(delta_sq * w['TARGET_SHIFTS'])

        # 2. Soft Cap Penalty (Anti-Hogging)
        if 'MAX_SHIFTS' in w:
            excess_shifts = model.NewIntVar(0, 7, f'excess_shifts_{e}')
            model.Add(excess_shifts >= total_worked - target)
            objective_terms.append(excess_shifts * w['MAX_SHIFTS'])

        # 3. Hard Limit (Absolute Max)
        model.Add(total_worked <= employees[e]['max_shifts'])

    model.Minimize(sum(objective_terms))


# ============================================================================
# 6. Main Orchestrator
# ============================================================================
def build_and_solve_model(employees, unavailable_requests, manual_assignments,
                          worked_last_sat_noon, worked_last_sat_night):
    # 1. Init
    model, shift_vars = _init_model_and_variables(employees, config.NUM_DAYS, config.NUM_SHIFTS)

    # 2. Hard Constraints
    _add_role_demand_constraints(model, shift_vars, employees, config.NUM_DAYS, config.NUM_SHIFTS)
    _add_shift_rules_constraints(model, shift_vars, len(employees), config.NUM_DAYS, config.NUM_SHIFTS)
    _add_availability_constraints(model, shift_vars, employees, unavailable_requests,
                                  manual_assignments, worked_last_sat_noon, worked_last_sat_night)
    _add_labor_law_constraints(model, shift_vars, employees, config.NUM_DAYS, config.NUM_SHIFTS)

    # 3. Objective (Soft Constraints)
    _build_objective_function(model, shift_vars, employees, config.NUM_DAYS, config.NUM_SHIFTS,
                              worked_last_sat_noon, worked_last_sat_night)

    # 4. Solve
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    return solver, status, shift_vars