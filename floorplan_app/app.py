# app.py
from flask import Flask, request, render_template, send_file, jsonify
import os
import json
from werkzeug.utils import secure_filename
from trace_to_dxf import trace_image_to_dxf_with_text
from PIL import Image
import base64
from io import BytesIO

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
DATASET_FOLDER = 'dataset'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Load the JSON data
with open(os.path.join(DATASET_FOLDER, 'room_vectors_with_area.json'), 'r') as f:
    data = json.load(f)

def calculate_distance(input_counts, input_areas, entry_counts, entry_areas):
    # Calculate the difference in room counts
    counts_diff = 0
    all_rooms = set(input_counts.keys()).union(set(entry_counts.keys()))
    for room in all_rooms:
        counts_diff += (input_counts.get(room, 0) - entry_counts.get(room, 0)) ** 2
    
    # Calculate the difference in areas
    areas_diff = 0
    for room in all_rooms:
        areas_diff += (input_areas.get(room, 0) - entry_areas.get(room, 0)) ** 2

    # Return the combined distance (MSE for counts and areas)
    return counts_diff + areas_diff

def find_closest_match(user_input):
    input_counts = user_input.get("counts", {})
    input_areas = user_input.get("areas", {})

    closest_image = None
    min_distance = float('inf')

    # Compare the user input with each entry in the data
    for entry in data:
        entry_counts = entry["input"].get("counts", {})
        entry_areas = entry["input"].get("areas", {})
        
        distance = calculate_distance(input_counts, input_areas, entry_counts, entry_areas)
        
        if distance < min_distance:
            min_distance = distance
            closest_image = entry["image"]

    return closest_image

def find_model_image(image_name):
    # Replace 'img.png' with 'model.png' to find the corresponding model image
    model_image_name = image_name.replace("img.png", "model.png")
    
    # Define the path to the rendered_images folder
    model_image_path = os.path.join(DATASET_FOLDER, "rendered_pngs", model_image_name)
    
    # Check if the model image exists
    if os.path.exists(model_image_path):
        return model_image_path
    else:
        return None  # Return None if the model image is not found

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/find_plan', methods=['POST'])
def find_plan():
    try:
        # Get JSON data from request
        user_input = request.json
        
        # Find the closest matching image
        closest_image = find_closest_match(user_input)
        
        if not closest_image:
            return jsonify({"error": "No matching floor plan found"}), 404
        
        # Find the model image
        model_image_path = find_model_image(closest_image)
        
        if not model_image_path:
            return jsonify({"error": "Model image not found"}), 404
        
        # Load the image and convert to base64 for preview
        with open(model_image_path, "rb") as img_file:
            img_data = img_file.read()
        
        # Save the image to upload folder for processing
        input_path = os.path.join(UPLOAD_FOLDER, f"recommended_{os.path.basename(model_image_path)}")
        with open(input_path, "wb") as f:
            f.write(img_data)
        
        # Create a unique name for the output DXF file
        output_filename = f"plan_{os.path.basename(model_image_path).split('.')[0]}.dxf"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        
        # Process the image to DXF
        trace_image_to_dxf_with_text(input_path, output_path)
        
        # Return the image preview and DXF download path
        base64_img = base64.b64encode(img_data).decode('utf-8')
        
        return jsonify({
            "success": True,
            "image_preview": f"data:image/png;base64,{base64_img}",
            "dxf_path": f"/download/{output_filename}"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return jsonify({"error": "No file part"}), 400
        
    image = request.files['image']
    
    if image.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    if image:
        filename = secure_filename(image.filename)
        input_path = os.path.join(UPLOAD_FOLDER, filename)
        output_filename = f"{filename.rsplit('.', 1)[0]}.dxf"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)

        image.save(input_path)
        
        try:
            trace_image_to_dxf_with_text(input_path, output_path)
            return jsonify({
                "success": True,
                "dxf_path": f"/download/{output_filename}"
            })
        except Exception as e:
            return jsonify({"error": f"Processing error: {str(e)}"}), 500
    
    return jsonify({"error": "Unknown error"}), 500

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_file(os.path.join(OUTPUT_FOLDER, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
