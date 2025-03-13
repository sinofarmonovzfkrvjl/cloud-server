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
    html_code = f"<br> <a href='/uploads/{filename}/delete'>delete the file</a><br>"

    return render_template("file.html", title=filename, head=filename, code=html_code)

@app.route("/uploads/<filename>/see")
def download_file(filename):
    return send_from_directory("uploads", filename)

@app.route("/uploads/<filename>/delete")
def delete_file(filename):
    os.remove(f"uploads/{filename}")
    files = os.listdir("uploads")

    return render_template("index.html", files=files)


app.run(debug=True, port=5500, host="0.0.0.0")