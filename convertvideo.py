from tkinter import Tk, filedialog, Label, Button, StringVar, OptionMenu, messagebox, ttk
import os
import subprocess


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
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to convert {filename}. Continuing with other files.")

        # Update progress bar
        progress_bar["value"] = i + 1
        root.update_idletasks()

    messagebox.showinfo("Success", f"Conversion completed! Files saved in: {output_folder}")


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

    convert_videos(input_folder, codec, profile)


def update_profile_visibility(*args):
    if codec_var.get() == "prores_ks":
        profile_dropdown.config(state="normal")
    else:
        profile_dropdown.config(state="disabled")


# Tkinter UI setup
root = Tk()
root.title("Video Codec Converter")
root.geometry("400x400")  # Adjusted window size

folder_path = StringVar()
codec_var = StringVar(value="Select Codec")
profile_var = StringVar(value="Select Profile")

# Folder selection
Label(root, text="Select Folder:").pack(pady=5)
Button(root, text="Browse", command=select_folder).pack(pady=5)
Label(root, textvariable=folder_path, wraplength=350).pack(pady=5)

# Codec selection
Label(root, text="Select Codec:").pack(pady=5)
codec_options = ["libx264", "libx265", "libvpx-vp9", "prores_ks"]
OptionMenu(root, codec_var, *codec_options).pack(pady=5)

# ProRes profile selection
Label(root, text="Select ProRes Profile (if applicable):").pack(pady=5)
profile_options = {
    "Proxy (0)": "0",
    "LT (1)": "1",
    "Normal (2)": "2",
    "HQ (3)": "3"
}
profile_dropdown = OptionMenu(root, profile_var, *profile_options.keys())
profile_dropdown.pack(pady=5)
profile_dropdown.config(state="disabled")

# Progress bar
progress_bar = ttk.Progressbar(root, length=300, mode="determinate")
progress_bar.pack(pady=10)

# Start button with proper colors for visibility
start_button = Button(
    root, 
    text="Start Conversion", 
    command=start_conversion, 
    bg="#4CAF50",   # Light green background
    fg="white",     # White text
    activebackground="#45A049",  # Slightly darker green when clicked
    activeforeground="white"     # Keep text visible when clicked
)
start_button.pack(pady=20)

# Update profile visibility dynamically
codec_var.trace_add("write", update_profile_visibility)

root.mainloop()
