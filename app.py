from flask import Flask, render_template, request, send_from_directory, redirect
import os

app = Flask(__name__)

os.makedirs("uploads", exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def HomePage():
    if request.method == "POST":

        if 'file' not in request.files:
            return "No file part", 400
    
        file = request.files['file']
        if file.filename == "":
            return "No selected file", 400
        
        file_path = os.path.join("uploads", file.filename)
        file.save(file_path)

        files = os.listdir("uploads")

        return render_template('upload.html', file=file.filename, files=files)
    else:
        files = os.listdir("uploads")

        return render_template('upload.html', files=files)

@app.route("/<filename>")
def uploads(filename):
    html_code = f"<br> <a href='/{filename}/delete'>delete the file</a><br>"

    return render_template("file.html", title=filename, head=filename, code=html_code)

@app.route("/<filename>/see")
def download_file(filename):
    return send_from_directory("uploads", filename)

@app.route("/<filename>/delete")
def delete_file(filename):
    try:
        os.remove(f"uploads/{filename}")
    except:
        pass

    return redirect("/", code=302)


app.run(debug=True, port=5500, host="0.0.0.0")