"""
ICInventory

This program is designed to work with the Octopart API at octopart.com to allow a user to search for parts and add them
to a local inventory. The main reason I am creating this program is to keep track of the various ICs I have gathered
over the years.

By Taylor Schweizer
"""

from tkinter import *
from tkinter.ttk import *
from main.utilities.settings import Settings
from main.screens.search_screen import SearchScreen
from main.screens.inventory_screen import InventoryScreen
from main.screens.settings_screen import SettingsScreen

def createScreens():
    """
    Initializes all of the screens and adds them to a tkinter notebook
    """
    s=Style()
    s.configure('TNotebook', tabposition=NW)
    notebook=Notebook(root,padding=5)
    notebook.pack()
    searchScreen = SearchScreen(notebook, settings)
    inventoryScreen = InventoryScreen(notebook, settings)
    settingsScreen = SettingsScreen(notebook, settings)
    notebook.add(searchScreen,text="Search")
    notebook.add(inventoryScreen, text='Inventory')
    notebook.add(settingsScreen, text='Settings')

if __name__ == '__main__':
    settings = Settings()
    root=Tk()
    root.title("IC Inventory")
    createScreens()
    root.mainloop()