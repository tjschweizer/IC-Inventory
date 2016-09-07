"""
IC_Inventory

This program is designed to work with the Octopart API at octopart.com to allow a user to search for parts and add them
to a local inventory. The main reason I am creating this program is to keep track of the various ICs I have gathered
over the years.

By Taylor Schweizer
"""

#Import Statements
from tkinter import *
from tkinter.ttk import *
from GlobalSettings import Settings
from InventoryScreen import InventoryScreen
from SearchScreen import SearchScreen
from SettingsScreen import SettingsScreen
from InventoryUtilities import Inventory

#createScreens function - initializes everything
def createScreens():

    #create a new notebook
    s=Style()
    s.configure('TNotebook', tabposition=NW)
    notebook=Notebook(root,padding=5)
    notebook.pack()

    #Create an instance of each screen
    searchScreen = SearchScreen(notebook, settings)
    inventoryScreen = InventoryScreen(notebook, settings)
    settingsScreen = SettingsScreen(notebook, settings)

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