import tkinter as tk
from tkinter import ttk
from pytube import YouTube
from moviepy.editor import *
import threading
import os
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


def download_video():
    url = url_entry.get()
    quality = quality_combobox.get()
    try:
        video = YouTube(url)
        stream = video.streams.filter(only_audio=True).first()

        output_folder = "DownloadedFiles"
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # download
        downloaded_file = stream.download(output_path=output_folder)
        progress_bar['value'] = 50
        app.update_idletasks()

        base, ext = os.path.splitext(downloaded_file)
        new_file = os.path.join(output_folder, os.path.basename(base) + '.mp3')

        target_bitrate = quality
        audio = AudioFileClip(downloaded_file)
        audio.write_audiofile(new_file, bitrate=target_bitrate)
        
        os.remove(downloaded_file)

        progress_bar['value'] = 100
        app.update_idletasks()
        url_entry.delete(0, 'end')
    except Exception as e:
        progress_bar['value'] = 0
        print(f"Error: {e}")


def start_download_thread():
    progress_bar['value'] = 0
    threading.Thread(target=download_video).start()

app = tk.Tk()
app.title("YouTube to Audio Converter")



tk.Label(app, text="YouTube URL:").pack()
url_entry = tk.Entry(app, width=50)
url_entry.pack()

tk.Label(app, text="Select Audio Quality:").pack()
quality_combobox = ttk.Combobox(app, values=["128k", "256k", "320k"], state="readonly")
quality_combobox.pack()
quality_combobox.set("256k")

progress_bar = ttk.Progressbar(app, length=100, mode='determinate')
progress_bar.pack()

download_button = tk.Button(app, text="Download", command=start_download_thread)
download_button.pack()

app.mainloop()
