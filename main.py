# main.py
import os
from ortools.sat.python import cp_model

# Import modules
import config
import optimizer
import excel_writer

def main():
    # --------------------------------------------------------
    # Image Parsing Logic
    # --------------------------------------------------------
    image_constraints = []

    if config.ENABLE_IMAGE_PARSING:
        print(f"--- Image Mode Enabled: Parsing {config.IMAGE_FILENAME} ---")
        if os.path.exists(config.IMAGE_FILENAME):
            try:
                # Import only if needed
                from image_process.cv2_image_parser import ScheduleImageParser

                # Define employee order in image (Top -> Down)
                img_employee_order = list(range(len(config.EMPLOYEES))) # 0 to N

                parser = ScheduleImageParser(config.IMAGE_FILENAME)
                image_constraints = parser.parse_tables(img_employee_order)
                print(f"V Success: Extracted {len(image_constraints)} constraints from image.")
            except ImportError:
                print("X Error: cv2_image_parser.py is missing or invalid.")
            except AttributeError:
                print("X Error: 'parse_tables' function not found.")
            except Exception as e:
                print(f"X General Error parsing image: {e}")
        else:
            print(f"X Error: File {config.IMAGE_FILENAME} not found.")
    else:
        print("--- Image Mode Disabled: Using manual list only ---")

    # Combine Lists
    unavailable_requests = config.MANUAL_REQUESTS + image_constraints

    # --------------------------------------------------------
    # Run Optimization
    # --------------------------------------------------------
    solver, status, shift_vars = optimizer.build_and_solve_model(
        employees=config.EMPLOYEES,
        unavailable_requests=unavailable_requests,
        manual_assignments=config.MANUAL_ASSIGNMENTS,
        worked_last_sat_noon=config.WORKED_LAST_SAT_NOON,
        worked_last_sat_night=config.WORKED_LAST_SAT_NIGHT
    )

    # --------------------------------------------------------
    # Output Results
    # --------------------------------------------------------
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(f"\n✅ Solution Found! Cost (Penalty): {solver.ObjectiveValue()}")

        # --------------------------------------------------------
        # DEBUG: RAW SOLVER VALIDATION
        # --------------------------------------------------------
        # print("\n" + "=" * 50)
        # print("🔍 Real-time Check: Raw Data from Solver")
        # print("=" * 50)
        #
        # for e_idx, emp in enumerate(config.EMPLOYEES):
        #     assigned_count = 0
        #     shifts_details = []
        #
        #     for d in range(config.NUM_DAYS):
        #         for s in range(config.NUM_SHIFTS):
        #             if solver.Value(shift_vars[(e_idx, d, s)]):
        #                 assigned_count += 1
        #                 # Convert indices to readable names
        #                 shift_name = ["Morning", "Noon", "Night", "Reinforcement"][s]
        #                 day_name = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"][d]
        #                 shifts_details.append(f"{day_name}-{shift_name}")
        #
        #     target = emp['target_shifts']
        #
        #     # Print status icon based on target vs actual
        #     gap = target - assigned_count
        #     status_icon = "✅" if gap <= 0 else "❌"
        #     if gap > 0: status_icon = "⚠️"  # Shift shortage
        #
        #     # Print the row
        #     print(
        #         f"{status_icon} {emp['name']:<15} | Target: {target} | Actual: {assigned_count} | Details: {', '.join(shifts_details)}")
        #
        # print("=" * 50 + "\n")

        # --------------------------------------------------------
        # Generate Excel Report
        # --------------------------------------------------------
        excel_writer.create_excel_schedule(
            solver,
            shift_vars,
            config.EMPLOYEES,
            config.NUM_DAYS,
            config.NUM_SHIFTS,
            config.EMPLOYEE_COLORS
        )
    else:
        print("\n❌ No feasible solution found. Try relaxing constraints.")

if __name__ == "__main__":
    main()