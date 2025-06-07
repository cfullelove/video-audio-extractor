import os
import uuid
import subprocess
from flask import Flask, request, redirect, url_for, send_file, render_template, flash

app = Flask(__name__)
app.secret_key = "replace-this-with-something-random"  # Not used for real auth—just suppresses warning

# Directory to store temporary uploads and outputs
UPLOAD_FOLDER = "/tmp/uploads"
OUTPUT_FOLDER = "/tmp/outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {
    # Any extension ffmpeg will accept; here we just check common video extensions.
    "mp4", "mov", "avi", "mkv", "flv", "wmv", "webm", "mpeg", "mpg"
}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # Check if the POST request has the file part
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # Save uploaded file to a temp path
            unique_id = str(uuid.uuid4())
            input_path = os.path.join(UPLOAD_FOLDER, f"{unique_id}_{file.filename}")
            file.save(input_path)

            # Define output filename (e.g. same base name + .mp3)
            base_name = os.path.splitext(file.filename)[0]
            output_filename = f"{base_name}_{unique_id}.mp3"
            output_path = os.path.join(OUTPUT_FOLDER, output_filename)

            # Run ffmpeg to extract audio only (convert to mp3)
            # -y = overwrite if exists
            cmd = [
                "ffmpeg",
                "-i", input_path,
                "-vn",  # no video
                "-acodec", "libmp3lame",
                "-ab", "192k",
                "-ar", "44100",
                "-y",
                output_path
            ]
            try:
                subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except subprocess.CalledProcessError as e:
                # ffmpeg failed
                flash("Error extracting audio.")
                return redirect(request.url)

            # Send the resulting file
            return send_file(output_path, as_attachment=True)
        else:
            flash("Invalid file type. Supported: " + ", ".join(sorted(ALLOWED_EXTENSIONS)))
            return redirect(request.url)
    # GET: show upload form
    return render_template("upload.html")


if __name__ == "__main__":
    # Listen on 0.0.0.0 so Docker can expose it
    app.run(host="0.0.0.0", port=5000, debug=False)
