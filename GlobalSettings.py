import os.path
import tkinter
from configparser import ConfigParser
from tkinter import Tk
from tkinter import ttk

from InventoryUtilities import Inventory


class Settings:
    def __init__(self):
        self.inventory = Inventory('Inventory.p')

        if os.path.isfile('config.ini') == True and os.path.isfile('Inventory.p') == True:
            self.openConfig()
            self.openInventory()

        elif os.path.isfile('config.ini') == False and os.path.isfile('Inventory.p') == True:
            msgText = "There is no valid Config file found in \n{0}.\n" \
                      "Click 'OK' to continue and create a new file in the program directory".format(
                os.getcwd())
            self.invalidInventoryPopup(msgText, self.createConfig(), self.openInventory())

        elif os.path.isfile('config.ini') == True and os.path.isfile('Inventory.p') == False:
            msgText = "There is no valid Inventory file found in \n{0}.\n" \
                      "Click 'OK' to continue and create a new file in the program directory".format(
                os.getcwd())
            self.invalidInventoryPopup(msgText, self.openConfig(), self.inventory.createInventory())

        elif os.path.isfile('config.ini') == False and os.path.isfile('Inventory.p') == False:
            msgText = "There is no valid Config or Inventory file found in \n{0}.\n" \
                      "Click 'OK' to continue and create the new files in the program directory".format(
                os.getcwd())
            self.invalidInventoryPopup(msgText, self.createConfig(), self.inventory.createInventory())

        if self.config.has_option('main', 'api') == False:
            msgText = "There is no API Key. You will not be able to \nsearch until you enter an API key in the settings page."
            self.invalidInventoryPopup(msgText)

    def createConfig(self):
        self.config = ConfigParser()
        self.config.read('config.ini')
        self.config.add_section('main')
        with open('config.ini', 'w') as f:
            self.config.write(f)
        f.close()

    def openConfig(self):
        self.config = ConfigParser()
        self.config.read('config.ini')

    def openInventory(self):
        self.inventory.openInventory()

    def invalidInventoryPopup(self, msg, *mainFuncs):
        # combine_funcs from
        # http://stackoverflow.com/questions/13865009/have-multiple-commands-when-button-is-pressed-in-tkinter-with-python-2-7


        window = Tk()
        window.wm_title('Invalid Inventory File')

        message = ttk.Label(window, text=msg)
        message.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky=tkinter.N + tkinter.S)
        okButton = ttk.Button(window, text="OK", command=lambda: self.combine_funcs(window.destroy(), window.quit()))
        okButton.grid(row=1, column=1, sticky=tkinter.N + tkinter.S)
        window.mainloop()

    def getAPIKey(self):
        apiKey = self.config.get('main', 'api')
        return apiKey

    def setAPIKey(self, api):
        self.config.set('main', 'api', api)
        with open('config.ini', 'r+') as f:
            self.config.write(f)
        f.close()

    def combine_funcs(*funcs):
        def combined_func(*args, **kwargs):
            for f in funcs:
                f(*args, **kwargs)

        return combined_func
