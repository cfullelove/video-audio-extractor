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

            # Get desired output format from form (default to m4a)
            output_format = request.form.get("output_format", "m4a").lower()
            if output_format not in ["mp3", "m4a"]:
                flash("Invalid output format selected.")
                return redirect(request.url)

            # Get desired bitrate from form (default to 192k)
            bitrate = request.form.get("bitrate", "192k").lower()
            if bitrate not in ["64k", "128k", "192k"]:
                flash("Invalid bitrate selected.")
                return redirect(request.url)

            # Define output filename
            base_name = os.path.splitext(file.filename)[0]
            output_filename = f"{base_name}_{unique_id}.{output_format}"
            output_path = os.path.join(OUTPUT_FOLDER, output_filename)

            # Base ffmpeg command
            cmd = [
                "ffmpeg",
                "-i", input_path,
                "-vn",  # no video
                "-y",   # overwrite if exists
            ]

            # Add format-specific options
            if output_format == "mp3":
                cmd.extend(["-acodec", "libmp3lame", "-ab", bitrate, "-ar", "44100"])
            elif output_format == "m4a":
                cmd.extend(["-acodec", "aac", "-b:a", bitrate])

            cmd.append(output_path)

            try:
                print(f"Executing ffmpeg command: {' '.join(cmd)}")
                process = subprocess.run(cmd, check=True) # Removed stdout/stderr PIPE
                print(f"FFmpeg process completed successfully.")
            except subprocess.CalledProcessError as e:
                print(f"FFmpeg failed. Return code: {e.returncode}")
                print(f"FFmpeg stdout: {e.stdout}")
                print(f"FFmpeg stderr: {e.stderr}")
                flash(f"Error extracting audio: FFmpeg failed (see logs for details).")
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
