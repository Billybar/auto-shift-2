import random

# System Configuration
NUM_EMPLOYEES = 36  # Total number of employees
NUM_DAYS = 7
NUM_SHIFTS = 4  # Includes reinforcement shift

# Number of constraints per employee
CONSTRAINTS_PER_EMPLOYEE = 7

all_requests = []

for emp_id in range(NUM_EMPLOYEES):
    # Use a set to ensure unique constraints for this specific employee
    employee_constraints = set()

    while len(employee_constraints) < CONSTRAINTS_PER_EMPLOYEE:
        day = random.randint(0, NUM_DAYS - 1)
        shift = random.randint(0, NUM_SHIFTS - 1)
        employee_constraints.add((day, shift))

    # Add this employee's constraints to the main list
    for day, shift in employee_constraints:
        all_requests.append((emp_id, day, shift))

# Sort the list by Employee ID, then Day, then Shift for readability
all_requests.sort()

# Output the result
print(f"# Generated {len(all_requests)} Constraints ({CONSTRAINTS_PER_EMPLOYEE} per employee)")
print("MANUAL_REQUESTS = [")
for req in all_requests:
    print(f"    {req},")
print("]")