from tkinter import *
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


class Toolbar:
    def __init__(self, master):
        self.toolbar = Frame(root, bg="blue")
        self.insertButt = Button(self.toolbar, text="Insert Image", command=self.PrintMessage)
        self.insertButt.pack(side=LEFT, padx=2, pady=2)
        self.printButt = Button(self.toolbar, text="Print", command=self.PrintMessage)
        self.printButt.pack(side=LEFT, padx=2, pady=2)
        self.toolbar.pack(side=TOP, fill=X)
        
    def PrintMessage(self):
        print("PRINTING")

class StatusBar:
    def __init__(self, master):
        self.status = Label(master, text="Preparing to do NADA", bd=1, relief=SUNKEN)
        self.status.pack(side=BOTTOM, fill=X)
        
    def PrintMessage(self):
        print("PRINTING")

class Screen(Frame):
    '''
        Screen widget: Embedded video player from local or youtube
    '''
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, bg = 'black')
        self.settings = { # Inizialazing dictionary settings
            "width" : 1024,
            "height" : 768
        }
        self.settings.update(kwargs) # Changing the default settings
        # Open the video source |temporary
        # self.video_source =  _path_+'asd.mp4'
        self.video_source = 'I:\DOWNLOAD\[Erai-raws] Boku no Hero Academia 4th Season - 10 [1080p][Multiple Subtitle]\[Erai-raws] Boku no Hero Academia 4th Season - 10 [1080p][Multiple Subtitle].mkv' 

        # Canvas where to draw video output
        self.canvas = Canvas(self, width = self.settings['width'], height = self.settings['height'], bg = "black", highlightthickness = 0)
        self.canvas.pack()

        # Creating VLC player
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.pack()


    def GetHandle(self):
        # Getting frame ID
        return self.winfo_id()

    def play(self, _source):
        # Function to start player from given source
        Media = self.instance.media_new(_source)
        Media.get_mrl()
        self.player.set_media(Media)

        #self.player.play()
        self.player.set_hwnd(self.GetHandle())
        self.player.play()

root = Tk()

# MyMenu(root)
# Toolbar(root)
# StatusBar(root)
screen = Screen(root)
screen.play(screen.video_source)

root.mainloop()