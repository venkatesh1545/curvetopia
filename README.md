- [CURVETOPIA: A Journey into the World of Curves](#curvetopia-a-journey-into-the-world-of-curves)
  - [Project Overview](#project-overview)
  - [Objective](#objective)
  - [Problem Description](#problem-description)
  - [Simplifications](#simplifications)
  - [Project Structure](#project-structure)
  - [Key Features](#key-features)
    - [1. Regularize Curves](#1-regularize-curves)
    - [2. Exploring Symmetry in Curves](#2-exploring-symmetry-in-curves)
    - [3. Completing Incomplete Curves](#3-completing-incomplete-curves)
    - [4. Visualization](#4-visualization)
  - [How to Install Dependencies](#how-to-install-dependencies)
    - [For Windows](#for-windows)
    - [For macOS and Linux](#for-macos-and-linux)
  - [How to Run the Application](#how-to-run-the-application)
  - [Contributors](#contributors)

# CURVETOPIA: A Journey into the World of Curves

## Project Overview

Welcome to **Curvetopia**, a project dedicated to identifying, regularizing, and beautifying 2D curves. Our goal is to transform complex curves into elegant shapes through a series of processing tasks. This includes regularizing curves, exploring symmetries, and completing incomplete shapes. The application is built using Flask and leverages various image processing and visualization techniques.

## Objective

The mission of Curvetopia is to:

- Identify and regularize shapes such as lines, circles, ellipses, rectangles, polygons, and star shapes.
- Detect symmetries in curves, particularly reflection symmetries.
- Complete incomplete or fragmented curves, ensuring natural and smooth transitions.

## Problem Description

Given input curves represented as sequences of points (polylines), the project aims to output refined curves as connected cubic Bézier curves. The transformation involves regularization, symmetry detection, and curve completion.

## Simplifications

- Input is provided as polylines (sequences of points) rather than PNG images.
- The project focuses on specific tasks: regularization, symmetry detection, and curve completion.

## Project Structure

```
/curvetopia
│
├── static/
│   ├── css/
│   │   └── styles.css              # Stylesheet for the web application
│   └── uploads/                    # Directory for storing uploaded images
│
├── templates/                      # Directory for HTML templates
│   ├── curve_completion.html       # Template for the curve completion page
│   ├── landing.html                # Template for the landing page
│   ├── process_image.html          # Template for processing the uploaded image
│   ├── results.html                # Template for displaying the results
│   ├── upload_image.html           # Template for the image upload page
│   └── visualize_data.html         # Template for visualizing the data
│   └── visualize_result.html       # Template for visualizing the result
│
├── app.py                          # Main Flask application file
├── curve_completion_handler.py     # Handles curve completion logic
├── process_handler.py              # Manages image processing tasks
├── requirements.txt                # Lists Python dependencies
├── upload_handler.py               # Manages file uploads
├── visualize_handler1.py           # Handles data visualization (part 1)
└── visualize_handler2.py           # Handles data visualization (part 2)

```

## Key Features

### 1. Regularize Curves

Identify and regularize various shapes:

- **Straight Lines**
- **Circles and Ellipses**: Detect curves where all points are equidistant from a center or have two focal points.
- **Rectangles and Rounded Rectangles**: Differentiate between rectangles and those with curved edges.
- **Regular Polygons**: Recognize polygons with equal sides and angles.
- **Star Shapes**: Identify star shapes with radial arms and a central point.

**Supported Formats**: `.jpg`, `.jpeg`, `.png`

**Supported Resolution**: **250x250**

### 2. Exploring Symmetry in Curves

Identify reflection symmetries in closed shapes. This involves checking for lines of symmetry where the shape can be divided into mirrored halves.

**Supported Formats**: `.png`, `.jpg`

### 3. Completing Incomplete Curves

Complete curves that are fragmented or partially occluded. The completion should consider smoothness, regularity, and symmetry.

**Supported Formats**: `.csv`

### 4. Visualization

Visualize curves using different formats and convert them to PNG for further analysis. Visualization helps in interpreting and validating the processed curves.

**Supported Formats**: `.jpg`, `.jpeg`, `.png`, `.csv`

## How to Install Dependencies

### For Windows

1. **Clone the Repository**:

   ```powershell
   git clone https://github.com/Karthik-Saladi5/curvetopia.git
   cd curvetopia
   ```

2. **Set PowerShell Execution Policy** (if needed):
   Ensure that you can run scripts in PowerShell. Open PowerShell as Administrator and run:

   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

3. **Create and Activate a Virtual Environment**:
   Create a virtual environment:

   ```powershell
   python -m venv venv
   ```

   Activate the virtual environment:

   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

4. **Install Python Packages**:
   ```powershell
   pip install -r requirements.txt
   ```

### For macOS and Linux

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/Karthik-Saladi5/curvetopia.git
   cd curvetopia
   ```

2. **Create and Activate a Virtual Environment**:
   Create a virtual environment:

   ```bash
   python3 -m venv venv
   ```

   Activate the virtual environment:

   ```bash
   source venv/bin/activate
   ```

3. **Install Python Packages**:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run the Application

1. **Start the Flask Server**:

   ```bash
   python app.py
   ```

2. **Navigate to** `http://127.0.0.1:5000` **in your web browser** to access the application.

## Contributors

**Developed by** - [**venkatesh1545**](https://github.com/venkatesh1545)

**Deployed by** - [**omteja04**](https://github.com/omteja04)

**Tested by** - [**Karthik-Saladi5**](https://github.com/Karthik-Saladi5)
