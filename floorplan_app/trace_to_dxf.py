# trace_to_dxf.py
import cv2
import pytesseract
import numpy as np
import ezdxf
from ezdxf.enums import TextEntityAlignment
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def preprocess_image(img_gray):
    """Apply preprocessing to improve image quality before tracing"""
    # Apply Gaussian blur to reduce noise
    img_gray = cv2.GaussianBlur(img_gray, (5, 5), 0)
    
    # Apply adaptive threshold to handle varying lighting conditions
    thresh = cv2.adaptiveThreshold(img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                  cv2.THRESH_BINARY_INV, 11, 2)
    
    # Optional: Apply morphology operations to clean up the image
    kernel = np.ones((3, 3), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    
    return thresh

def find_text_regions(img_color):
    """Find and extract text regions from the image"""
    try:
        return pytesseract.image_to_data(img_color, output_type=pytesseract.Output.DICT)
    except Exception as e:
        logger.warning(f"OCR processing failed: {str(e)}")
        return {"text": [], "left": [], "top": [], "width": [], "height": []}

def trace_image_to_dxf_with_text(image_path, output_dxf):
    """Process an image to create a DXF file with traced contours and text"""
    logger.info(f"Processing image: {image_path}")
    
    # Load the image
    try:
        img_gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        img_color = cv2.imread(image_path)
        
        if img_gray is None or img_color is None:
            raise ValueError("Failed to load image.")
            
        # Get image dimensions for logging
        height, width = img_gray.shape
        logger.info(f"Image dimensions: {width}x{height}")
    except Exception as e:
        logger.error(f"Error loading image: {str(e)}")
        raise
    
    # Flip the image (for coordinate system consistency)
    try:
        img_gray = cv2.flip(img_gray, 0)
        img_color = cv2.flip(img_color, 0)
    except Exception as e:
        logger.error(f"Error flipping image: {str(e)}")
        raise
    
    # Apply preprocessing
    try:
        thresh = preprocess_image(img_gray)
    except Exception as e:
        logger.error(f"Error during image preprocessing: {str(e)}")
        # Fall back to basic thresholding if advanced preprocessing fails
        _, thresh = cv2.threshold(img_gray, 200, 255, cv2.THRESH_BINARY_INV)
    
    # Find contours
    try:
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        logger.info(f"Found {len(contours)} contours")
    except Exception as e:
        logger.error(f"Error finding contours: {str(e)}")
        raise
    
    # Create a new DXF document
    try:
        doc = ezdxf.new()
        msp = doc.modelspace()
    except Exception as e:
        logger.error(f"Error creating DXF document: {str(e)}")
        raise
    
    # Process contours and add to DXF
    contour_count = 0
    try:
        for contour in contours:
            points = contour.squeeze()
            if len(points.shape) != 2 or len(points) < 2:
                continue
                
            # Optional: Filter out very small contours
            if cv2.arcLength(contour, True) < 10:
                continue
                
            for i in range(len(points) - 1):
                p1 = tuple(map(int, points[i]))
                p2 = tuple(map(int, points[i + 1]))
                msp.add_line(p1, p2)
                contour_count += 1
        
        logger.info(f"Added {contour_count} line segments to DXF")
    except Exception as e:
        logger.error(f"Error processing contours: {str(e)}")
        # Continue with text extraction even if contour processing fails
    
    # Extract and add text
    text_count = 0
    try:
        data = find_text_regions(img_color)
        for i in range(len(data['text'])):
            text = data['text'][i].strip()
            if text:
                x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                cx, cy = x + w // 2, y + h // 2
                
                # Add text entity
                msp.add_text(text, dxfattribs={'height': 10}).set_placement(
                    (cx, cy), align=TextEntityAlignment.CENTER
                )
                text_count += 1
        
        logger.info(f"Added {text_count} text elements to DXF")
    except Exception as e:
        logger.warning(f"Error processing text: {str(e)}")
        # Continue with saving even if text extraction fails
    
    # Save the DXF file
    try:
        doc.saveas(output_dxf)
        logger.info(f"Successfully saved DXF file: {output_dxf}")
    except Exception as e:
        logger.error(f"Error saving DXF file: {str(e)}")
        raise
        
    return output_dxf
