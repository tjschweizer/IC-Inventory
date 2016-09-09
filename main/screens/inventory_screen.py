"""
IC Inventory

Inventory Screen Setup

by Taylor Schweizer
"""

#Import Statements
from tkinter import *
from tkinter.ttk import *

from main.utilities.multilistbox import MultiListbox
from main.octopart.octo_utils import *


#Inventory Screen Class
class InventoryScreen(Frame):
    """
    Inventory Screen class contains the widgets for the inventory screen
    """
    def __init__(self, master, settings):
        """
        Init for inventory screen

        :param master: Tkinter notebook
        :type master: tkinter.notebook
        :param settings: Settings object
        :type settings: utilities.global_settings.Settings
        """
        Frame.__init__(self, master)
        self.pack()
        self.settings = settings
        self.createWidgets()
        self.loadInventory()
        self.bind('<Visibility>', self.on_visibility)

    def on_visibility(self, event):
        """
        Updates the inventory list every time the tab changes
        """
        self.loadInventory()

    def createWidgets(self):
        """
        Creates the widgets
        """
        self.resultListLabels = ['Part Number', 'Manufacturer', 'Description']
        self.resultsListWidths = (20, 25, 75)
        self.inventoryList = MultiListbox(self.resultListLabels, self.resultsListWidths, self, NORMAL, True)
        self.inventoryList.grid(row=0, column=0, padx=10, pady=5)

    def loadInventory(self):
        """
        Adds inventory to inventory list
        """
        tmp = getOctoList(self.settings.inventory.inventory)
        if tmp:
            self.inventoryList.addList(tmp)
