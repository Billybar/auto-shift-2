import cv2
import numpy as np


class ScheduleImageParser:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = cv2.imread(image_path)
        if self.image is None:
            raise ValueError(f"Could not load image from {image_path}")

    def parse_tables(self, employee_ids):
        """
        Main function: Detects tables and extracts constraints.
        """
        table_boxes = self._detect_table_boxes()

        # Sort tables from top to bottom
        table_boxes.sort(key=lambda b: b[1])

        all_constraints = []
        print(f"DEBUG: Found {len(table_boxes)} tables.")

        for i, box in enumerate(table_boxes):
            if i >= len(employee_ids):
                break

            emp_id = employee_ids[i]
            x, y, w, h = box

            # Extract constraints from this specific table
            table_constraints = self._scan_grid_geometry(x, y, w, h, emp_id)
            all_constraints.extend(table_constraints)

        return all_constraints

    def _detect_table_boxes(self):
        """
        Identifies tables by 'smearing' the image horizontally.
        This connects the header letters (א ב ג) into a single block,
        ensuring we get the FULL width even if grid lines are faint.
        """
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        # 1. Threshold (Black text becomes White)
        binary = cv2.adaptiveThreshold(~gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, -2)

        # 2. Horizontal Dilation
        # We use a very wide kernel to force detected text to merge horizontally
        kernel_width = int(self.image.shape[1] / 15)  # Dynamic width
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_width, 3))
        dilated = cv2.dilate(binary, kernel, iterations=3)

        # 3. Find Contours
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        valid_boxes = []
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            # Filter: Must be wide enough to be a table
            if w > self.image.shape[1] * 0.3 and h > 20:
                valid_boxes.append((x, y, w, h))

        return valid_boxes

    def _scan_grid_geometry(self, x, y, w, h, emp_id):
        constraints = []

        # Geometry:
        # Header is approx top 22%
        header_height = int(h * 0.22)
        shift_height = (h - header_height) / 3.0

        # Width: Use 90% of the box width (assuming right margin has text)
        grid_width_limit = w * 0.90
        col_width = grid_width_limit / 7.0

        # Prepare Red Mask
        hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        mask1 = cv2.inRange(hsv, np.array([0, 70, 50]), np.array([10, 255, 255]))
        mask2 = cv2.inRange(hsv, np.array([170, 70, 50]), np.array([180, 255, 255]))
        red_mask = mask1 + mask2

        # Iterate Grid
        for day_idx in range(7):
            for shift_idx in range(3):
                # Coordinates (Right-to-Left calculation for Hebrew days)
                cell_right_edge = x + grid_width_limit - (day_idx * col_width)
                cell_left_edge = cell_right_edge - col_width

                cell_top = y + header_height + (shift_idx * shift_height)

                cx = int(cell_left_edge)
                cy = int(cell_top)
                cw = int(col_width)
                ch = int(shift_height)

                # Check center of cell to avoid border noise
                padding_x = int(cw * 0.3)
                padding_y = int(ch * 0.3)

                if cw > 0 and ch > 0:
                    roi = red_mask[cy + padding_y: cy + ch - padding_y, cx + padding_x: cx + cw - padding_x]
                    if cv2.countNonZero(roi) > 5:  # Threshold of red pixels
                        constraints.append((emp_id, day_idx, shift_idx))

        return constraints