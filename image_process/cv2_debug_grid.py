import os
import cv2


def detect_and_draw_grid(image_path):
    print(f"Processing: {image_path}...")

    # 1. Load the image
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Image not found.")
        return

    # 2. Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 3. Thresholding (Binarization)
    # We use adaptive thresholding to handle lighting variations.
    # We invert the image so lines become white and background becomes black.
    binary = cv2.adaptiveThreshold(~gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, -2)

    # 4. Isolate Horizontal and Vertical lines using Morphology
    # Create structure elements for extracting lines
    horizontal = binary.copy()
    vertical = binary.copy()

    # Specify size on horizontal axis (width / 30 is a heuristic)
    scale = 20
    horizontal_size = horizontal.shape[1] // scale

    # Create kernel for horizontal lines
    horizontal_structure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontal_size, 1))

    # Apply morphology operations
    horizontal = cv2.erode(horizontal, horizontal_structure)
    horizontal = cv2.dilate(horizontal, horizontal_structure)

    # Create kernel for vertical lines
    vertical_size = vertical.shape[0] // scale
    vertical_structure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, vertical_size))

    # Apply morphology operations
    vertical = cv2.erode(vertical, vertical_structure)
    vertical = cv2.dilate(vertical, vertical_structure)

    # 5. Combine the lines to create the grid mask
    # This creates a purely black and white image of ONLY the grid lines
    grid_mask = horizontal + vertical

    # 6. Find Contours (The cells of the table)
    # This proves we can identify individual boxes
    contours, _ = cv2.findContours(grid_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Create a visual debug image
    debug_image = image.copy()

    # Filter contours by size (remove noise) and draw them
    tables_found = 0
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        # Filter: Only keep shapes that look like tables (wide enough, tall enough)
        if w > 50 and h > 20:
            # Draw a thick green rectangle around detected table structures
            cv2.rectangle(debug_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            tables_found += 1

    # 7. Save the outputs
    cv2.imwrite("../images/debug_1_grid_lines.png", grid_mask)
    cv2.imwrite("../images/debug_2_detected_tables.png", debug_image)

    print(f"Done! Found {tables_found} potential table structures.")
    print("Check 'debug_1_grid_lines.png' to see the extracted black lines.")
    print("Check 'debug_2_detected_tables.png' to see what the computer identified.")


if __name__ == "__main__":
    # Ensure you use the correct filename from your folder
    # Based on your upload, I assume you want to test the faint one
    image_filename = "../images/image3.png"

    if os.path.exists(image_filename):
        detect_and_draw_grid(image_filename)
    else:
        # Fallback to the other image if the first one isn't found
        detect_and_draw_grid("image2.png")