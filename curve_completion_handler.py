import os
import csv
import numpy as np
from flask import Blueprint, render_template, request, redirect, current_app, flash, send_file
from werkzeug.utils import secure_filename
from scipy.interpolate import interp1d
from sklearn.linear_model import LinearRegression

curve_completion = Blueprint('curve_completion', __name__)

# Example function for connected curve completion

# Function to remove duplicate x values by averaging corresponding y values
def remove_duplicates(x, y):
    unique_x, indices = np.unique(x, return_inverse=True)
    avg_y = np.zeros_like(unique_x)
    
    for i, idx in enumerate(indices):
        avg_y[idx] += y[i]
    
    counts = np.bincount(indices)
    avg_y /= counts
    
    return unique_x, avg_y

# Example function for connected curve completion with duplication handling
def complete_connected_curve(points):
    x, y = points[:, 2], points[:, 3]
    
    # Remove duplicates from x and average corresponding y values
    x, y = remove_duplicates(x, y)
    
    f = interp1d(x, y, kind='cubic', fill_value="extrapolate")
    new_x = np.linspace(min(x), max(x), num=100, endpoint=True)
    new_y = f(new_x)
    
    return np.column_stack((new_x, new_y))


# Example function for disconnected curve completion
def complete_disconnected_curve(points):
    x, y = points[:, 2], points[:, 3]
    model = LinearRegression()
    model.fit(x.reshape(-1, 1), y)
    new_x = np.linspace(min(x), max(x), num=100, endpoint=True)
    new_y = model.predict(new_x.reshape(-1, 1))
    return np.column_stack((new_x, new_y))

@curve_completion.route('/', methods=['GET', 'POST'])
def complete_curve():
    if request.method == 'POST':
        occlusion_type = request.form['occlusion_type']
        file = request.files['file']

        if not file or not file.filename.endswith('.csv'):
            flash('Please upload a valid CSV file.', 'danger')
            return redirect(request.url)

        # Save the uploaded file
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Read the CSV file and process the points
        points = []
        with open(file_path, 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                # Debug: Print row content
                print("Row content:", row)
                
                # If row contains only one string, split it
                if len(row) == 1:
                    row = row[0].split(',')
                
                # Convert to float
                points.append([float(val) for val in row])

        points = np.array(points)

        # Debug: Print points shape and content
        print("Points array shape:", points.shape)
        print("Points array content:", points)

        # Perform curve completion based on occlusion type
        if occlusion_type == 'connected':
            completed_points = complete_connected_curve(points)
        elif occlusion_type == 'disconnected':
            completed_points = complete_disconnected_curve(points)
        else:
            flash('Invalid occlusion type selected.', 'danger')
            return redirect(request.url)

        # Save the completed points to a new CSV file
        output_filename = os.path.join(current_app.config['UPLOAD_FOLDER'], f'completed_{filename}')
        with open(output_filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            for point in completed_points:
                writer.writerow([0.00E+00, 0.00E+00, point[0], point[1]])

        flash('Curve completion successful!', 'success')
        return send_file(output_filename, as_attachment=True)

    return render_template('curve_completion.html')