import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
from tkinter.filedialog import askopenfilename
import pathlib
import os
import vlc
import time

PLAY_UNICODE="\u25B6"
PAUSE_UNICODE="\u23F8"
FAST_FORWARD_UNICODE="\u23E9"
REWIND_UNICODE="\u23EA"
MAX_PLAY_RATE=4.0
MIN_PLAY_RATE=0.25

class Screen(tk.Frame):
    '''
        Screen widget: Embedded video player from local or youtube
    '''
    def __init__(self, tkRoot, *args, **kwargs):
        tk.Frame.__init__(self, tkRoot)

        self.initialDirectory = pathlib.Path(os.path.expanduser("~"))
        self.menuFont = Font(family="Verdana", size=20)
        self.defaultFont = Font(family="Times New Roman", size=16)
        self.tkRoot = tkRoot

        self.settings = { # Initializing dictionary settings
            "width" : 1024,
            "height" : 768
        }
        self.settings.update(kwargs) # Changing the default settings
        # Open the video source |temporary
        # self.video_source =  _path_+'asd.mp4'
        self.video_source = 'I:\DOWNLOAD\[Erai-raws] Boku no Hero Academia 4th Season - 10 [1080p][Multiple Subtitle]\[Erai-raws] Boku no Hero Academia 4th Season - 10 [1080p][Multiple Subtitle].mkv' 

        # main menubar
        self.menubar = tk.Menu(self.tkRoot)
        self.menubar.config(font=self.menuFont)

        # cascading file menu
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.createFileMenu()

        self.tkRoot.config(menu=self.menubar)

        # Canvas where to draw video output
        self.video_panel = tk.Frame(self.tkRoot)
        self.canvas = tk.Canvas(self.video_panel, width = self.settings['width'], height = self.settings['height'], bg = "black", highlightthickness = 0)
        self.canvas.pack(fill=tk.BOTH, expand=1)
        self.video_panel.pack(fill=tk.BOTH, expand=1)

        # Creating VLC player
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()


        # Create slider
        timers = ttk.Frame(self.tkRoot)
        self.timeVar = tk.DoubleVar()
        self.timeSliderLastVal = 0
        self.timeSlider = tk.Scale(timers, variable=self.timeVar, command=self.onTime, from_=0, to=1000,
                                    orient=tk.HORIZONTAL, length=500, showvalue=0)
        self.timeSlider.pack(side=tk.LEFT, fill=tk.X, expand=1)
        self.timeSliderUpdated = time.time()
        self.timerText = tk.Label(timers, text="0:00/0:00")
        self.timerText.pack(side=tk.LEFT, fill=tk.X)
        timers.pack(side=tk.BOTTOM, fill=tk.X)

        
        # create control panel
        self.createControlPanel()
        self.initKeyBinds()

        # setup timer task
        self.onTick()

    def onTime(self, e):
        if self.player:
            t = self.timeVar.get()
            if self.timeSliderLastVal != int(t):
                self.player.set_time(int(t * 1e3)) # ms
                self.timeSliderUpdated = time.time()

    def updateTimeText(self, t, length):
        t_str = "%d:%s" % (t//60, str(int(t%60)).zfill(2))
        length_str = "%d:%s" % (length//60, str(int(length%60)).zfill(2))
        self.timerText.config(text="%s/%s" % (t_str, length_str))

    def onTick(self):
        """ Update slider position
        """
        if self.player:
            # adjust length in case it's changed (e.g. changed media file)
            length = self.player.get_length() * 1e-3 # seconds
            if length > 0:
                self.timeSlider.config(to=length)

            t = self.player.get_time() * 1e-3 # seconds
            if t > 0 and time.time() > (self.timeSliderUpdated + 2):
                self.timeSlider.set(t)
                self.updateTimeText(t, length)
                self.timeSliderLastVal = int(self.timeVar.get())
        # repeat every second
        self.tkRoot.after(1000, self.onTick)

    def createFileMenu(self):
        """Create file menu."""
        self.file_menu.add_command(label="Open", command=self.open, font=self.defaultFont, accelerator="ctrl + o")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Quit", command=self.close, font=("Verdana", 14, "bold"), accelerator="ctrl + q")
        self.menubar.add_cascade(label="File", menu=self.file_menu)

    def createControlPanel(self):
        controlPanel = tk.Frame(self.tkRoot, bg="blue")
        def playPause():
            if not self.player.get_media():
                self.open()
            else:
                status = self.pause_unpause()
                if status == 0:
                    playPauseButton.config(text=PLAY_UNICODE)
                else:
                    playPauseButton.config(text=PAUSE_UNICODE)
        def increaseRate():
            self.player.set_rate(min(MAX_PLAY_RATE, self.player.get_rate()*2))

        def decreaseRate():
            self.player.set_rate(max(MIN_PLAY_RATE, self.player.get_rate()/2))
            
        playPauseButton = tk.Button(controlPanel, text=PLAY_UNICODE, command=playPause)
        playPauseButton.pack(side=tk.LEFT, padx=4, pady=4)
        sep = ttk.Separator(controlPanel)
        sep.pack(side="left", fill="y", padx=4, pady=4)

        fastForwardButton = tk.Button(controlPanel, text=FAST_FORWARD_UNICODE, command=increaseRate)
        decreaseRateButton = tk.Button(controlPanel, text=REWIND_UNICODE, command=decreaseRate)
        decreaseRateButton.pack(side=tk.LEFT, padx=4, pady=4)
        fastForwardButton.pack(side=tk.LEFT, padx=4, pady=4)
        controlPanel.pack(side=tk.TOP, fill=tk.X)
    
    def initKeyBinds(self):
        self.tkRoot.bind("<space>", lambda e: self.pause_unpause())
        self.video_panel.bind("<Button-1>", lambda e: self.pause_unpause())

    def GetHandle(self):
        # Getting frame ID
        return self.video_panel.winfo_id()

    def Resize(self, width, height):
        self.canvas.configure(width=width, height=height)

    def open(self):
        """New window allowing user to select a file and play."""
        file = askopenfilename(initialdir=self.initialDirectory)
        if isinstance(file, tuple):
            return
        if os.path.isfile(file):
            self.play(file)

    def play(self, _source):
        # Function to start player from given source
        Media = self.instance.media_new(_source)
        Media.get_mrl()
        self.player.set_media(Media)
        

        self.player.set_hwnd(self.GetHandle())
        self.player.play()
        # w,h = self.player.video_get_size()
        # print(w,h)

    def printSize(self):
        print(self.player.video_get_size())

    def pause_unpause(self):
        if self.player.is_playing():
            self.player.pause()
            return 0
        else:
            self.player.play()
            return 1
    
    def close(self):
        self.tkRoot.quit()
        self.tkRoot.destroy()
        os._exit(1)

 

root = tk.Tk()

screen = Screen(root)
# screen.play(screen.video_source)

root.mainloop()