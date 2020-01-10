import tkinter as tk
from tkinter.font import Font
from tkinter.filedialog import askopenfilename
import pathlib
import os
import vlc

PLAY_UNICODE="\u25B6"
PAUSE_UNICODE="\u23F8"

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

        
        # create control panel
        self.createControlPanel()
        self.initKeyBinds()

    def createFileMenu(self):
        """Create file menu."""
        self.file_menu.add_command(label="Open", command=self.open, font=self.defaultFont, accelerator="ctrl + o")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Quit", command=self.close, font=("Verdana", 14, "bold"), accelerator="ctrl + q")
        self.menubar.add_cascade(label="File", menu=self.file_menu)

    def createControlPanel(self):
        toolbar = tk.Frame(self.tkRoot, bg="blue")
        def playPause():
            if not self.player.get_media():
                self.open()
            else:
                status = self.pause_unpause()
                if status == 0:
                    playPauseButton.config(text=PLAY_UNICODE)
                else:
                    playPauseButton.config(text=PAUSE_UNICODE)
            
        playPauseButton = tk.Button(toolbar, text=PLAY_UNICODE, command=playPause)
        playPauseButton.pack(side=tk.LEFT, padx=2, pady=2)

        # fastForwardButton = tk.Button(self.tool)
        # rewindButton = tk.Button()
        toolbar.pack(side=tk.TOP, fill=tk.X)
    
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

# MyMenu(root)
# Toolbar(root)
# StatusBar(root)
screen = Screen(root)
# screen.play(screen.video_source)
# screen.printSize

root.mainloop()