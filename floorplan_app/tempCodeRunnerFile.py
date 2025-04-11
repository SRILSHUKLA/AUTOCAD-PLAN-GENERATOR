from flask import Flask, request, render_template, send_file
import os
from werkzeug.utils import secure_filename
from trace_to_dxf import trace_image_to_dxf_with_text

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        image = request.files['image']
        if image:
            filename = secure_filename(image.filename)
            input_path = os.path.join(UPLOAD_FOLDER, filename)
            output_path = os.path.join(OUTPUT_FOLDER, filename.rsplit('.', 1)[0] + '.dxf')

            image.save(input_path)
            trace_image_to_dxf_with_text(input_path, output_path)
            return send_file(output_path, as_attachment=True)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
