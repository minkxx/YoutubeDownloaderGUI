import os
import getpass

try:
    import customtkinter as ctk
    from customtkinter import filedialog
except ImportError:
    os.system("pip install customtkinter")

try:
    import pytube
except ImportError:
    os.system("pip install pytube")

try:
    import ffmpeg
except ImportError:
    os.system("pip install ffmpeg-python")

try:
    from PIL import Image
except ImportError:
    os.system("pip install pillow")

current_windows_username = getpass.getuser()

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x450")
        self.title("YouTube Downloader")
        self.resizable(False, False)
        self.iconbitmap("res/app_icon.ico")
        ctk.set_appearance_mode("dark")

        # add variables to app
        self.download_path = ctk.StringVar(value=f"C:/Users/{current_windows_username}/Downloads")
        self.optionmenu_var = ctk.StringVar(value="select quality")
        self.output_var = ctk.StringVar()
        self.progress_var = ctk.StringVar(value="0 %")
        self.url_var = ctk.StringVar()

        # add image varibales to app
        # my_image = ctk.CTkImage(light_image=Image.open("<path to light mode image>"),
        #                           dark_image=Image.open("<path to dark mode image>"),
        #                           size=(30, 30))

        # add widgets to app
        title_label = ctk.CTkLabel(self, text="YouTube Downloader", fg_color="transparent", font=("Inter", 30))
        title_label.place(x=170, y=20)

        self.url_entry = ctk.CTkEntry(self, placeholder_text="Enter url to download", font=("Inter", 12), width=400, textvariable=self.url_var)
        self.url_entry.place(x=50, y=90)

        self.search_btn = ctk.CTkButton(self, text="Search", command=self.search, width=70)
        self.search_btn.place(x=480, y=90)

        self.dir_path_entry = ctk.CTkEntry(self, placeholder_text="Download path", font=("Inter", 12), width=400, textvariable=self.download_path)
        self.dir_path_entry.place(x=50, y=140)


        self.dir_browse_btn = ctk.CTkButton(self, text="Browse", command=self.browse_path, width=70)
        self.dir_browse_btn.place(x=480, y=140)

        self.optionmenu = ctk.CTkOptionMenu(self, variable=self.optionmenu_var, state="disabled", command=self.test)
        self.optionmenu.place(x=50, y=190)

        self.download_btn = ctk.CTkButton(self, text="Download", command=self.download, width=100, state="disabled")
        self.download_btn.place(x=450, y=190)

        self.progressbar = ctk.CTkProgressBar(self, width=400)
        self.progressbar.set(0)
        self.progressbar.place(x=50, y=250)

        self.progress_label = ctk.CTkLabel(self, text="%", fg_color="transparent", font=("Inter", 14), textvariable=self.progress_var)
        self.progress_label.place(x=480, y=238)

        # image_label = ctk.CTkLabel(self, image=my_image, text="")  # display image with a CTkLabel

        self.output_label = ctk.CTkLabel(self, text="test", fg_color="transparent", font=("Inter", 12), textvariable=self.output_var)
        self.output_label.place(x=50, y=400)
        
    # add methods to app
    def browse_path(self):
        download_Directory = filedialog.askdirectory(
            initialdir="YOUR DIRECTORY PATH", title="Save Video")
    
        self.download_path.set(download_Directory)

    def search(self):
        url = self.url_var.get()
        if url == "":
            self.output_var.set("Please enter an url!")
        else:
            self.yt = pytube.YouTube(url, on_progress_callback=self.on_progress)
            self.video_streams = self.get_video_streams(self.yt.streams.filter(progressive=False))
            self.audio_streams = self.get_audio_streams(self.yt.streams)
            streams = []
            for i in self.video_streams:
                streams.append(i)
            for i in self.audio_streams:
                streams.append(i)
            self.optionmenu.configure(values=streams, state="normal")


    def test(self, option):
        self.download_btn.configure(state="normal")


    def download(self):
        res = self.optionmenu_var.get()
        if res in self.video_streams:
            self.output_var.set(f"Downloading {self.yt.title}")
            video_path = self.video_streams[res][0].download(output_path="temp",filename_prefix="video_")
            audio_path = self.audio_streams["128kbps"][0].download(output_path="temp", filename_prefix="audio_")
            self.output_var.set("Merging...")
            self.merge_audio_video(audio_path, video_path, f"{self.yt.title}.mp4")
            self.output_var.set(f"Downloaded : {self.yt.title}")
            os.remove(video_path)
            os.remove(audio_path)
        elif res in self.audio_streams:
            self.output_var.set(f"Downloading {self.yt.title}")
            self.audio_streams[res][0].download(self.download_path.get())
            self.output_var.set(f"Downloaded Audio: {self.yt.title}")
        else:
            self.output_var.set("Quality not found!")

        self.progressbar.set(0)
        self.progress_var.set("0 %")
        self.optionmenu_var.set("select quality")
        self.optionmenu.configure(state="disabled")
        self.url_var.set("")
        self.download_btn.configure(state="disabled")

    def download_audio(self):
        pass

    def download_thumb(self):
        pass

    # Youtube callback function
    def on_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        completed = (bytes_downloaded/total_size) * 100
        self.progress_var.set(f"{int(completed)} %")
        self.progressbar.set(float(completed)/100)
        self.progressbar.update()
        
    def get_video_streams(self, streams):
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

    def get_audio_streams(self, streams):
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

    def merge_audio_video(self, audio, video, output):
        input_audio = ffmpeg.input(audio)
        input_video = ffmpeg.input(video)
        ffmpeg.concat(input_video, input_audio, v=1, a=1).output(os.path.join(self.download_path.get(), output)).run()
        return output


if __name__ == "__main__":
    app = App()
    app.mainloop()