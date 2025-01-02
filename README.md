# Video Codec Converter

A Python-based GUI application for video file conversion using `ffmpeg`. This tool allows users to:
- Select a folder containing video files.
- Choose a codec for conversion (e.g., `libx264`, `libx265`, `prores_ks`).
- Optionally select a ProRes profile when using the `prores_ks` codec.
- Track the conversion progress via a progress bar.

The application logs errors for debugging and provides a user-friendly interface using `Tkinter`.

---

## Features
- Support for multiple video codecs: `libx264`, `libx265`, `libvpx-vp9`, `prores_ks`.
- Optional ProRes profile selection for advanced users.
- Real-time progress updates and error logging.

---

## Prerequisites
- Python 3.8 or higher
- `ffmpeg` installed and accessible via the system PATH.

### Required Python Packages
Install the dependencies using `pip`:

```bash
pip install tkinter
