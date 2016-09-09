from tkinter import *
from tkinter.ttk import *

class SettingsScreen(Frame):
    """
    Settings Screen class contains the widgets for the settings screen
    """
    def __init__(self, master, settings):
        """
        Init for settings screen

        :param master: Tkinter notebook
        :type master: tkinter.notebook
        :param settings: Settings object
        :type settings: utilities.global_settings.Settings
        """
        Frame.__init__(self, master)
        self.apiText = StringVar()
        self.pack()
        self.settings = settings
        self.createWidgets()

    def createWidgets(self):
        """
        Creates the widgets for the settings screen
        """
        self.apiEntry = Entry(self)
        self.apiEntry.grid(row=0, column=0)
        apiButton = Button(self, text='Save API Key', command=self.saveApi)
        apiButton.grid(row=0, column=1)
        self.apiEntry['textvariable'] = self.apiText
        self.downloadBool = IntVar()
        self.enableDatasheet = Checkbutton(self, text='Enable Datasheet Download', variable=self.downloadBool,
                                           command=self.enableDownload)
        self.enableDatasheet.grid(row=1, column=0, columnspan=2)

    def enableDownload(self):
        """
        Sets the config file to enable or disable datasheet download based on checkbutton
        """
        self.settings.setDownloadBool(str(self.downloadBool.get()))

    def saveApi(self):
        """
        Saves the API key to the config file
        """
        self.settings.setAPIKey(self.apiText.get())
