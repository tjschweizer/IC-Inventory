"""
IC Inventory

Main Window Setup

by Taylor Schweizer
"""
#Import Statements
from tkinter import *
from tkinter.ttk import *

from GlobalSettings import Settings
from InventoryScreen import InventoryScreen
from SearchScreen import SearchScreen
from SettingsScreen import SettingsScreen


#createScreens function - initializes everything
def createScreens():

    #create a new notebook
    s=Style()
    s.configure('TNotebook', tabposition=NW)
    notebook=Notebook(root,padding=5)
    notebook.pack()

    #Create an instance of each screen
    searchScreen = SearchScreen(notebook, settings)
    inventoryScreen = InventoryScreen(notebook)
    settingsScreen = SettingsScreen(notebook)

    #Add screen instances to notebook
    notebook.add(searchScreen,text="Search")
    notebook.add(inventoryScreen, text='Inventory')
    notebook.add(settingsScreen, text='Settings')


#Run the program
if __name__ == '__main__':
    settings = Settings()
    root=Tk()
    root.title("IC Inventory")
    createScreens()
    root.mainloop()