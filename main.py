import tkinter
import customtkinter as ctk
from customtkinter import filedialog

import pytube
import ffmpeg
import getpass

current_windows_username = getpass.getuser()

def get_video_streams(streams):
    data = {}
    res = ["1080p", "720p", "480p", "360p", "240p", "144p"]
    for q in res:
        for i in streams:
            if i.resolution == q:
                if q in data:
                    data[q].append(i)
                else:
                    data[q] = [i]
    return data

def get_audio_streams(streams):
    data = {}
    abr = ["160kbps", "128kbps", "70kbps", "50kbps", "48kbps"]
    for q in abr:
        for i in streams:
            if i.abr == q:
                if q in data:
                    data[q].append(i)
                else:
                    data[q] = [i]
    return data

def merge_audio_video(audio, video, output):
    input_audio = ffmpeg.input(audio)
    input_video = ffmpeg.input(video)
    ffmpeg.concat(input_video, input_audio, v=1, a=1).output(output).run()
    return output

#  GUI

app = ctk.CTk()
app.geometry("600x450")
app.title("YouTube Downloader")
app.resizable(False, False)
app.iconbitmap("res/app_icon.ico")
ctk.set_appearance_mode("dark")


#  GUI variables
download_path = ctk.StringVar(value=f"C:/Users/{current_windows_username}/Downloads")
optionmenu_var = ctk.StringVar(value="select quality")
output_var = ctk.StringVar()
progress_var = ctk.StringVar(value="0 %")

#  GUI button commands
def browse_path():
    download_Directory = filedialog.askdirectory(
        initialdir="YOUR DIRECTORY PATH", title="Save Video")
 
    download_path.set(download_Directory)

def download():
    url = url_entry.get()
    res = optionmenu_var.get()
    yt = pytube.YouTube(url, on_progress_callback=on_progress)
    data = get_video_streams(yt.streams.filter(progressive=True))
    if res in data:
        output_var.set(f"Downloading {yt.title}")
        data[res][0].download(download_path.get())
        output_var.set(f"Downloaded : {yt.title}")
        progressbar.set(0)
        progress_var.set("0 %")
    else:
        output_var.set("Quality not found!")

# Youtube callback function
def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    completed = (bytes_downloaded/total_size) * 100
    progress_var.set(f"{int(completed)} %")
    progressbar.set(float(completed)/100)
    progressbar.update()


# GUI widgets
title_label = ctk.CTkLabel(app, text="YouTube Downloader", fg_color="transparent", font=("Inter", 30))
title_label.place(x=170, y=20)

url_entry = ctk.CTkEntry(app, placeholder_text="Enter url to download", font=("Inter", 12), width=500)
url_entry.place(x=50, y=70)

dir_path_entry = ctk.CTkEntry(app, placeholder_text="Download path", font=("Inter", 12), width=400, textvariable=download_path)
dir_path_entry.place(x=50, y=120)


dir_browse_btn = ctk.CTkButton(app, text="Browse", command=browse_path, width=70)
dir_browse_btn.place(x=480, y=120)

optionmenu = ctk.CTkOptionMenu(app, values=["1080p", "720p", "480p", "360p", "240p", "144p"], variable=optionmenu_var)
optionmenu.place(x=50, y=170)

download_btn = ctk.CTkButton(app, text="Download", command=download, width=100)
download_btn.place(x=450, y=170)

progressbar = ctk.CTkProgressBar(app, width=400)
progressbar.set(0)
progressbar.place(x=50, y=250)

progress_label = ctk.CTkLabel(app, text="%", fg_color="transparent", font=("Inter", 14), textvariable=progress_var)
progress_label.place(x=480, y=238)

output_label = ctk.CTkLabel(app, text="test", fg_color="transparent", font=("Inter", 12), textvariable=output_var)
output_label.place(x=50, y=400)

if __name__ == "__main__":
    app.mainloop()