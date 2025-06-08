# 🎵 Video to Audio Extractor (Self-Hosted Docker Utility)

A minimal, self-hosted web utility that extracts audio from uploaded video files using `ffmpeg`. Built with Flask and packaged in a lightweight Docker container.

## 🚀 Features

- Upload any video file supported by `ffmpeg` (e.g., `.mp4`, `.mkv`, `.avi`, etc.)
- Extracts audio only (no video) and allows selection of output format:
  - **MP3**
  - **M4A (AAC)**
- `ffmpeg` command output is logged to the terminal (Docker logs) for easier debugging.
- Lightweight and fast — runs entirely locally
- No authentication (intended for private/local use)
- Fully containerized with Docker

## 🖼️ Screenshot

**Note:** The screenshot below is outdated due to recent UI changes (addition of format selection).
![Screenshot](docs/screenshot.png) <!-- Optional: Add if you take a screenshot -->

## 📦 Getting Started

### 1. Clone This Repo

```bash
git clone https://github.com/cfullelove/video-audio-extractor.git
cd video-audio-extractor
```

### 2. Build the Docker Image
```bash
docker build -t video-audio-extractor .
```

### 3. Run the Container
```bash
docker run --rm -p 5000:5000 --name extractor video-audio-extractor
```
Now open your browser to: `http://localhost:5000`

Upload a video file and get an .mp3 audio file back.

# 🔧 Technical Details
Uses Flask for the web interface

- Uses `ffmpeg` to extract audio. The command varies based on the selected output format:
  - **MP3:** `ffmpeg -i input.ext -vn -acodec libmp3lame -ab 192k -ar 44100 -y output.mp3`
  - **M4A (AAC):** `ffmpeg -i input.ext -vn -acodec aac -b:a 192k -y output.m4a`
- `ffmpeg` output is now directed to standard output/error, visible in Docker logs.
- Saves uploads and outputs temporarily in `/tmp/uploads` and `/tmp/outputs` (within the container)
- Supports common video formats:
mp4, mov, avi, mkv, flv, wmv, webm, mpeg, mpg

# 📁 Project Structure
```bash
video-to-audio/
├── Dockerfile              # Docker image definition
├── app.py                  # Flask app
├── requirements.txt        # Python dependencies
├── templates/
│   └── upload.html         # HTML upload form
└── README.md               # This file
```

# 🧼 Cleanup Notes

This utility stores uploaded and converted files in /tmp directories inside the container. When the container stops (thanks to --rm), these files are automatically discarded.

If you modify the app to run persistently, consider implementing a cleanup mechanism for stale files.

# 🛡️ Security Notice

This app is not secured and does not include authentication, HTTPS, or rate-limiting. It's intended to run:

Locally on a trusted machine

Behind a reverse proxy (if exposed externally)

Do not expose it to the public internet without additional security layers.

# 📄 License
MIT License. Do what you like — no warranty provided.

Created with 💻 + ☕ for quick and simple local audio extraction.
