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

## Automated Container Image Publishing

This repository is configured with a GitHub Action that automatically builds and publishes a Docker container image to the GitHub Container Registry (GHCR).

### Triggers

The workflow is triggered on every push to any branch and on every pull request event (e.g., opened, synchronized) in the repository.

### Image Tagging

Images are tagged based on the event and branch that triggered the build:

*   **Pushes to `main` branch:**
    *   `ghcr.io/cfullelove/video-audio-extractor:latest`
    *   `ghcr.io/cfullelove/video-audio-extractor:<commit_sha_short>` (e.g., `ghcr.io/cfullelove/video-audio-extractor:abc1234`)
*   **Pushes to other branches (e.g., `feature-branch`):**
    *   `ghcr.io/cfullelove/video-audio-extractor:feature-branch-<commit_sha_short>` (e.g., `ghcr.io/cfullelove/video-audio-extractor:feature-branch-abc1234`)
*   **Pull request events (e.g., for PR #123):**
    *   `ghcr.io/cfullelove/video-audio-extractor:pr-123-<commit_sha_short>` (e.g., `ghcr.io/cfullelove/video-audio-extractor:pr-123-abc1234`)

(Replace `OWNER/REPO` with the actual repository owner and name, which is `${{ github.repository }}` in the workflow.)

### Using the Image

You can pull the image using Docker:

```bash
# Example for the latest image from the main branch
docker pull ghcr.io/cfullelove/video-audio-extractor:latest

# Example for a specific commit on the main branch
docker pull ghcr.io/cfullelove/video-audio-extractor:abcdefg

# Example for a feature branch
docker pull ghcr.io/cfullelove/video-audio-extractor:feature-branch-abcdefg

# Example for a pull request build
docker pull ghcr.io/cfullelove/video-audio-extractor:pr-123-abcdefg
```

To run the container:

```bash
docker run -d -p 5000:5000 ghcr.io/cfullelove/video-audio-extractor:latest
```
This will start the application, and it will be accessible at `http://localhost:5000`.
