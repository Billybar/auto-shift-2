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