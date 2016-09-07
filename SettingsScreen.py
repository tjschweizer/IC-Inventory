"""
IC Inventory

Settings Screen Setup

by Taylor Schweizer
"""

#Import Statements
from tkinter import *
from tkinter.ttk import *

#Settings Screen Class
class SettingsScreen(Frame):
    def __init__(self, master, settings):
        Frame.__init__(self, master)
        self.apiText = StringVar()
        self.pack()
        self.settings = settings
        self.createWidgets()

    def createWidgets(self):
        self.apiEntry = Entry(self)
        self.apiEntry.grid(row=0, column=0)
        apiButton = Button(self, text='Save API Key', command=self.saveApi)
        apiButton.grid(row=0, column=1)
        self.apiEntry['textvariable'] = self.apiText

    def saveApi(self):
        self.settings.setAPIKey(self.apiText.get())
