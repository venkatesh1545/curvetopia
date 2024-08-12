import cv2
import numpy as np
from flask import Blueprint, request, render_template, redirect, url_for, current_app
import os

process_image = Blueprint('process_image', __name__)

@process_image.route('/', methods=['GET', 'POST'])
def upload_and_process():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        
        # Save the uploaded file
        filename = file.filename
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Process the image
        img = cv2.imread(file_path)
        edges = cv2.Canny(img, 100, 700)
        
        # Detect symmetry and draw lines on the image
        symmetry_img, symmetries = detect_and_process_shapes(img, edges)
        
        # Save the processed image with symmetry lines
        processed_img_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'processed_' + filename)
        cv2.imwrite(processed_img_path, symmetry_img)
        
        # Return the result
        return render_template('process_image.html', filename=filename, symmetries=symmetries, processed_filename='processed_' + filename)
    
    return render_template('process_image.html')

def detect_and_process_shapes(img, edges):
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    symmetries = []
    output_img = img.copy()

    for contour in contours:
        # Create a mask for the current shape
        mask = np.zeros_like(edges)
        cv2.drawContours(mask, [contour], -1, 255, -1)
        
        # Extract the bounding box for the current shape
        x, y, w, h = cv2.boundingRect(contour)
        shape_img = img[y:y+h, x:x+w]
        shape_mask = mask[y:y+h, x:x+w]
        
        # Separate the shape from the background
        isolated_shape = cv2.bitwise_and(shape_img, shape_img, mask=shape_mask)
        
        # Check symmetry for the isolated shape
        horizontal_symmetry_count, vertical_symmetry_count = check_symmetry(isolated_shape, shape_mask)
        
        # Draw symmetry lines on the output image
        if horizontal_symmetry_count > 0:
            cv2.line(output_img, (x, y + h // 2), (x + w, y + h // 2), (0, 255, 0), 2)
        if vertical_symmetry_count > 0:
            cv2.line(output_img, (x + w // 2, y), (x + w // 2, y + h), (255, 0, 0), 2)
        
        # Append the results
        symmetries.append({
            'contour_index': len(symmetries) + 1,
            'horizontal_symmetry': horizontal_symmetry_count,
            'vertical_symmetry': vertical_symmetry_count
        })

    return output_img, symmetries

def check_symmetry(shape_img, shape_mask):
    # Convert the isolated shape to grayscale
    shape_gray = cv2.cvtColor(shape_img, cv2.COLOR_BGR2GRAY)
    
    # Get the bounding box dimensions
    h, w = shape_gray.shape
    
    # Initialize symmetry counts
    horizontal_symmetry_count = 0
    vertical_symmetry_count = 0
    
    # Horizontal symmetry check
    top_half = shape_gray[:h//2, :]
    bottom_half = shape_gray[h//2:, :]
    mirrored_bottom_half = np.flip(bottom_half, axis=0)
    
    if np.array_equal(top_half, mirrored_bottom_half):
        horizontal_symmetry_count += 1
    
    # Vertical symmetry check
    left_half = shape_gray[:, :w//2]
    right_half = shape_gray[:, w//2:]
    mirrored_right_half = np.flip(right_half, axis=1)
    
    if np.array_equal(left_half, mirrored_right_half):
        vertical_symmetry_count += 1
    
    return horizontal_symmetry_count, vertical_symmetry_count
