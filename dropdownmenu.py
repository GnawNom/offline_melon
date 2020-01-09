import tkinter as tk
import vlc

class MyMenu:
    def __init__(self, master):
        self.menu = Menu(master)
        self.subMenu = Menu(self.menu)
        self.subMenu.add_command(label="New Project... ", command=self.PrintMessage) 
        self.subMenu.add_command(label="New... ", command=self.PrintMessage) 
        self.subMenu.add_separator()
        self.subMenu.add_command(label="Exit", command=self.PrintMessage)
        
        self.editMenu = Menu(self.menu)
        self.editMenu.add_command(label="Redo", command=self.PrintMessage)

        master.config(menu=self.menu)
        self.menu.add_cascade(label="File", menu=self.subMenu)
        self.menu.add_cascade(label="Edit", menu=self.editMenu)

    def PrintMessage(self):
        print("PRINTING")

class PlayerControls:
    PLAY_UNICODE="\u25B6"
    PAUSE_UNICODE="\u23F8"
    def __init__(self, master, screen):
        self.screen = screen
        self.toolbar = tk.Frame(root, bg="blue")
        self.playPauseButton = tk.Button(self.toolbar, text=PlayerControls.PLAY_UNICODE, command=self.PlayPauseAction)
        self.playPauseButton.pack(side=tk.LEFT, padx=2, pady=2)
        self.printButt = tk.Button(self.toolbar, text="Print", command=self.PrintMessage)
        self.printButt.pack(side=tk.LEFT, padx=2, pady=2)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)
        
    def PrintMessage(self):
        print("PRINTING")

    def PlayPauseAction(self):
        status = self.screen.pause_unpause()
        if status == 0:
            self.playPauseButton.config(text=PlayerControls.PLAY_UNICODE)
        else:
            self.playPauseButton.config(text=PlayerControls.PAUSE_UNICODE)

class StatusBar:
    def __init__(self, master):
        self.status = Label(master, text="Preparing to do NADA", bd=1, relief=SUNKEN)
        self.status.pack(side=BOTTOM, fill=X)
        
    def PrintMessage(self):
        print("PRINTING")

class Screen(tk.Frame):
    '''
        Screen widget: Embedded video player from local or youtube
    '''
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, bg = '#8abce6' )
        self.settings = { # Inizialazing dictionary settings
            "width" : 1024,
            "height" : 768
        }
        self.settings.update(kwargs) # Changing the default settings
        # Open the video source |temporary
        # self.video_source =  _path_+'asd.mp4'
        self.video_source = 'I:\DOWNLOAD\[Erai-raws] Boku no Hero Academia 4th Season - 10 [1080p][Multiple Subtitle]\[Erai-raws] Boku no Hero Academia 4th Season - 10 [1080p][Multiple Subtitle].mkv' 

        # Canvas where to draw video output
        self.canvas = tk.Canvas(self, width = self.settings['width'], height = self.settings['height'], bg = "black", highlightthickness = 0)
        self.canvas.pack()

        # Creating VLC player
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.pack(fill=tk.X)


    def GetHandle(self):
        # Getting frame ID
        return self.winfo_id()

    def Resize(self, width, height):
        self.canvas.configure(width=width, height=height)

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

root = tk.Tk()

# MyMenu(root)
# Toolbar(root)
# StatusBar(root)
screen = Screen(root)
controls = PlayerControls(root, screen)
screen.play(screen.video_source)
# screen.printSize

root.mainloop()