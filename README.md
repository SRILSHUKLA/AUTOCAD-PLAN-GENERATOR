# DraftEase 🏗️
![image](https://github.com/user-attachments/assets/44b2aa51-38da-48ad-8b8a-8aeb9a9d45d4)


## Overview

**DraftEase** is a web-based tool that converts architectural floor plan images into editable CAD files (DXF format). Instead of relying on AI, DraftEase uses a custom algorithmic approach to trace architectural elements such as walls and rooms from clear floor plan images, making the output reliable and lightweight.

## Features

- **Image-to-CAD Conversion**: Upload floor plan images and convert them to DXF format
- **Algorithmic Tracing Engine**: Detects structure outlines using traditional computer vision techniques
- **Fast and Lightweight**: No heavy AI models, runs efficiently even on basic setups
- **Editable CAD Output**: Generated DXF files are compatible with all major CAD software
- **Intuitive UI**: Drag-and-drop upload and instant download of output files

## Technologies Used

- Python (Flask)
- HTML5, CSS3, JavaScript
- OpenCV and PIL for image processing
- DXF writing using `ezdxf` or custom tracing logic

## How It Works

1. **Upload**: Select a clean floor plan image (PNG, JPG)
2. **Trace**: The backend processes the image and traces architectural outlines
3. **Convert**: The traced shapes are converted into DXF file elements
4. **Download**: Instantly download the DXF for editing in AutoCAD or similar software

## Installation

To run DraftEase locally:

```bash
git clone https://github.com/SRILSHUKLA/AUTOCAD-PLAN-GENERATOR.git
cd AUTOCAD-PLAN-GENERATOR
pip install -r requirements.txt
python app.py
