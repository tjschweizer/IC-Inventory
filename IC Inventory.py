"""
IC Inventory

Main Window Setup

by Taylor Schweizer
"""

#Import Statements
from tkinter import *
from tkinter.ttk import *
from SearchScreen import SearchScreen
from InventoryScreen import InventoryScreen
from SettingsScreen import SettingsScreen

#createScreens function - initializes everything
def createScreens():

    #create a new notebook
    s=Style()
    s.configure('TNotebook', tabposition=NW)
    notebook=Notebook(root,padding=5)
    notebook.pack()

    #Create an instance of each screen
    searchScreen = SearchScreen(notebook)
    inventoryScreen = InventoryScreen(notebook)
    settingsScreen = SettingsScreen(notebook)

    #Add screen instances to notebook
    notebook.add(searchScreen,text="Search")
    notebook.add(inventoryScreen, text='Inventory')
    notebook.add(settingsScreen, text='Settings')


#Run the program
if __name__ == '__main__':
    root=Tk()
    root.title("IC Inventory")
    createScreens()
    root.mainloop()