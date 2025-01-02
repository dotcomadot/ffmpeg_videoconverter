from tkinter import Tk, filedialog, StringVar, messagebox, ttk
import os
import subprocess
import threading
import logging
from datetime import datetime

# Configure logging with a timestamped log file
log_file_name = f"conversion_errors_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    filename=log_file_name,
    level=logging.DEBUG,  # Log both errors and debug information
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def convert_videos(input_folder, codec, profile=None):
    if not input_folder:
        messagebox.showerror("Error", "No folder selected!")
        return

    output_folder = os.path.join(input_folder, "converted")
    os.makedirs(output_folder, exist_ok=True)

    video_extensions = (".mp4", ".avi", ".mkv", ".mov")
    files = [f for f in os.listdir(input_folder) if f.lower().endswith(video_extensions)]

    if not files:
        messagebox.showerror("Error", "No video files found in the selected folder.")
        return

    logging.info(f"Starting video conversion for {len(files)} files in folder: {input_folder}")

    # Show loading label
    root.after(0, lambda: loading_label.config(text="Processing... Please wait"))
    root.update_idletasks()

    # Progress bar setup
    progress_bar["maximum"] = len(files)
    progress_bar["value"] = 0

    for i, filename in enumerate(files):
        input_file = os.path.join(input_folder, filename)
        output_file = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_{codec}.mov")

        command = ["ffmpeg", "-i", input_file, "-c:v", codec]

        if codec == "prores_ks" and profile:
            command.extend(["-profile:v", profile])

        command.extend(["-c:a", "aac", output_file])

        try:
            logging.info(f"Converting {filename} with command: {' '.join(command)}")
            # Capture stdout and stderr for logging
            result = subprocess.run(
                command, check=True, text=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE
            )
            logging.info(f"Successfully converted {filename} to {output_file}")
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to convert {filename}. Command: {' '.join(command)}\nError: {e.stderr}")
            root.after(0, lambda: messagebox.showerror(
                "Error", f"Failed to convert {filename}. Check logs for details."
            ))

        # Update progress bar safely
        root.after(0, lambda value=i + 1: progress_bar.config(value=value))

    # Remove loading label and show success message
    root.after(0, lambda: loading_label.config(text=""))
    logging.info("Video conversion process completed.")
    root.after(0, lambda: messagebox.showinfo("Success", f"Conversion completed! Files saved in: {output_folder}\nLog: {log_file_name}"))

def select_folder():
    folder = filedialog.askdirectory(title="Select Folder")
    folder_path.set(folder)

def start_conversion():
    input_folder = folder_path.get()
    codec = codec_var.get()
    profile = profile_options.get(profile_var.get(), None) if codec == "prores_ks" else None

    if not input_folder:
        messagebox.showerror("Error", "Please select a folder.")
        return

    if codec == "Select Codec":
        messagebox.showerror("Error", "Please select a codec.")
        return

    # Disable interactive elements
    start_button.config(state="disabled")
    codec_menu.config(state="disabled")
    profile_dropdown.config(state="disabled")

    def run_conversion():
        convert_videos(input_folder, codec, profile)
        # Re-enable interactive elements after conversion
        root.after(0, lambda: start_button.config(state="normal"))
        root.after(0, lambda: codec_menu.config(state="normal"))
        root.after(0, lambda: profile_dropdown.config(state="normal"))

    # Start a new thread for the conversion process
    conversion_thread = threading.Thread(target=run_conversion)
    conversion_thread.start()

def update_profile_visibility(*args):
    if codec_var.get() == "prores_ks":
        profile_dropdown.config(state="normal")
    else:
        profile_dropdown.config(state="disabled")

# Tkinter UI setup
root = Tk()
root.title("Video Codec Converter")
root.geometry("400x450")  # Adjusted window size

folder_path = StringVar()
codec_var = StringVar(value="Select Codec")
profile_var = StringVar(value="Select Profile")

# Folder selection
ttk.Label(root, text="Select Folder:").pack(pady=5)
ttk.Button(root, text="Browse", command=select_folder).pack(pady=5)
ttk.Label(root, textvariable=folder_path, wraplength=350).pack(pady=5)

# Codec selection
ttk.Label(root, text="Select Codec:").pack(pady=5)
codec_options = ["libx264", "libx265", "libvpx-vp9", "prores_ks"]
codec_menu = ttk.OptionMenu(root, codec_var, *codec_options)
codec_menu.pack(pady=5)

# ProRes profile selection
ttk.Label(root, text="Select ProRes Profile (if applicable):").pack(pady=5)
profile_options = {
    "Proxy (0)": "0",
    "LT (1)": "1",
    "Normal (2)": "2",
    "HQ (3)": "3"
}
profile_dropdown = ttk.OptionMenu(root, profile_var, *profile_options.keys())
profile_dropdown.pack(pady=5)
profile_dropdown.config(state="disabled")

# Progress bar
progress_bar = ttk.Progressbar(root, length=300, mode="determinate")
progress_bar.pack(pady=10)

# Loading label
loading_label = ttk.Label(root, text="", foreground="red")
loading_label.pack(pady=10)

# Start button
start_button = ttk.Button(root, text="Start Conversion", command=start_conversion)
start_button.pack(pady=20)

# Update profile visibility dynamically
codec_var.trace_add("write", update_profile_visibility)

root.mainloop()
