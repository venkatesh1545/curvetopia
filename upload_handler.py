from flask import Blueprint, request, render_template, redirect, current_app
import os
import cv2
import numpy as np
from werkzeug.utils import secure_filename

upload_image = Blueprint('upload_image', __name__)

# Function to determine the shape of the object
def detect_shape(contour):
    shape = "unidentified"
    perimeter = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)  # Adjusted approximation factor
    
    num_vertices = len(approx)
    
    if num_vertices == 3:
        shape = "triangle"
    elif num_vertices == 4:
        (x, y, w, h) = cv2.boundingRect(approx)
        ar = w / float(h)
        shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"
    elif num_vertices == 5:
        shape = "pentagon"
    elif num_vertices == 6:
        shape = "hexagon"
    elif num_vertices == 10 and is_star_shape(approx):
        shape = "star"
    elif num_vertices > 6:
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        circularity = (4 * np.pi * area) / (perimeter * perimeter)
        if circularity > 0.85:
            shape = "circle"
        else:
            shape = "ellipse"
    else:
        shape = "unidentified"
    
    return shape

# Function to check if the contour is a star shape
def is_star_shape(approx):
    # This function will check specific properties of the contour to determine if it's a star
    # One basic approach could be to look at the internal angles or the distance between points.
    # This will need fine-tuning based on specific requirements or training data.
    return True  # Placeholder, requires specific logic based on star detection needs

# Function to check if the contour is a straight line
def is_straight_line(contour):
    _, (MA, ma), _ = cv2.fitEllipse(contour)
    return ma < 0.05 * MA  # Improved condition for straight line detection

# Function to process the uploaded image and detect shapes
def process_image(file_path):
    img = cv2.imread(file_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)  # Applying GaussianBlur for better edge detection
    edged = cv2.Canny(blurred, 50, 150)  # Edge detection using Canny
    
    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    shape_counts = {
        "triangle": 0,
        "square": 0,
        "rectangle": 0,
        "pentagon": 0,
        "hexagon": 0,
        "polygon": 0,
        "circle": 0,
        "ellipse": 0,
        "star": 0,
        "straight_line": 0,
        "unidentified": 0
    }
    
    for contour in contours:
        if is_straight_line(contour):
            shape = "straight_line"
        else:
            shape = detect_shape(contour)
        if shape in shape_counts:
            shape_counts[shape] += 1
        else:
            shape_counts["unidentified"] += 1
    
    return shape_counts

# Route to handle image upload
@upload_image.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        
        # Save the uploaded file
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Process the image and detect shapes
        shape_counts = process_image(file_path)
        
        # Render the results
        return render_template('results.html', shapes=shape_counts)
    return render_template('upload_image.html')