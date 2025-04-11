import cv2
import pytesseract
import numpy as np
import ezdxf
from ezdxf.enums import TextEntityAlignment

def trace_image_to_dxf_with_text(image_path, output_dxf):
    # Load image
    img_gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    img_color = cv2.imread(image_path)

    if img_gray is None or img_color is None:
        raise ValueError("Failed to load image.")

    # Flip the image both vertically and horizontally
    img_gray = cv2.flip(img_gray, 0)
    img_color = cv2.flip(img_color, 0)

    # Thresholding
    _, thresh = cv2.threshold(img_gray, 200, 255, cv2.THRESH_BINARY_INV)

    # Contour detection
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Create DXF
    doc = ezdxf.new()
    msp = doc.modelspace()

    # Draw contours
    for contour in contours:
        points = contour.squeeze()
        if len(points.shape) != 2 or len(points) < 2:
            continue
        for i in range(len(points) - 1):
            p1 = tuple(map(int, points[i]))
            p2 = tuple(map(int, points[i + 1]))
            msp.add_line(p1, p2)

    # OCR and text placement
    data = pytesseract.image_to_data(img_color, output_type=pytesseract.Output.DICT)
    for i in range(len(data['text'])):
        text = data['text'][i].strip()
        if text:
            x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
            cx, cy = x + w // 2, y + h // 2
            msp.add_text(text, dxfattribs={'height': 10}).set_placement(
                (cx, cy), align=TextEntityAlignment.CENTER
            )

    # Save file
    doc.saveas(output_dxf)
    print(f"✅ DXF saved as '{output_dxf}'")

# Example usage
trace_image_to_dxf_with_text(
    "/Users/suryadeepsinhjadeja/Desktop/PHOTO-2025-04-11-14-30-43.jpg",
    "output_with_text.dxf"
)
