"""
IC Inventory

Inventory Screen Setup

by Taylor Schweizer
"""

#Import Statements
from tkinter import *
from tkinter.ttk import *
from MultiListBox import MultiListbox

#Inventory Screen Class
class InventoryScreen(Frame):
    def __init__(self, master, settings):
        # Initialize the Frame
        Frame.__init__(self, master)
        self.pack()
        self.settings = settings
        self.createWidgets()
        self.loadInventory()
        self.bind('<Visibility>', self.on_visibility)

    def on_visibility(self, event):
        self.loadInventory()

    def createWidgets(self):
        self.resultListLabels = ['Part Number', 'Manufacturer', 'Description']
        self.resultsListWidths = (20, 25, 75)
        self.techScroll = Scrollbar(self, orient=VERTICAL)
        self.techScroll.grid(row=0, column=1, sticky=N + S)
        self.inventoryList = MultiListbox(self.resultListLabels, self.resultsListWidths, self, NORMAL, True,
                                          self.techScroll)
        self.inventoryList.grid(row=0, column=0, padx=10, pady=5)

    def loadInventory(self):
        self.inventoryList.addOctopartList(self.settings.inventory.inventory)
