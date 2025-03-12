from flask import Flask, render_template, request, send_from_directory
import os


app = Flask(__name__)

os.makedirs("uploads", exist_ok=True)

@app.route('/')
def HomePage():
    files = os.listdir("uploads")

    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    
    file = request.files['file']
    if file.filename == "":
        return "No selected file", 400
    
    file_path = os.path.join("uploads", file.filename)
    file.save(file_path)

    files = os.listdir("uploads")

    return render_template('index.html', file=file.filename, files=files)

@app.route("/uploads/<filename>")
def uploads(filename):
    return send_from_directory("uploads", filename)


app.run(debug=True)