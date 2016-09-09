import os.path
import tkinter
from configparser import ConfigParser
from tkinter import Tk
from tkinter import ttk

from main.utilities.inventory_utilities import Inventory


class Settings:
    """
    Settings class to work with creating inventory and config files
    """
    def __init__(self):
        """
        Initialization method that generates popup windows if certain files don't exist
        """
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

        if not os.path.isdir('datasheets'):
            os.mkdir('datasheets')
    def createConfig(self):
        """
        Creates a configuration file 'config.ini'
        """
        self.config = ConfigParser()
        self.config.read('config.ini')
        self.config.add_section('main')
        self.config.set('main', 'downloadDatasheets', '1')
        with open('config.ini', 'w') as f:
            self.config.write(f)
        f.close()

    def openConfig(self):
        """
        Opens the configuration file and assigns it to a ConfigParser
        """
        self.config = ConfigParser()
        self.config.read('config.ini')

    def openInventory(self):
        """
        Opens the inventory file
        """
        self.inventory.openInventory()

    def invalidInventoryPopup(self, msg, *mainFuncs):
        """
        Creates a popupwindow and binds the button to multiple functions

        :param msg: Text message displayed in the popupwindow
        :type msg: str
        :param mainFuncs: List of functions to be run when the user clicks OK
        """
        window = Tk()
        window.wm_title('Invalid Inventory File')

        message = ttk.Label(window, text=msg)
        message.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky=tkinter.N + tkinter.S)
        okButton = ttk.Button(window, text="OK", command=lambda: self.combine_funcs(window.destroy(), window.quit()))
        okButton.grid(row=1, column=1, sticky=tkinter.N + tkinter.S)
        window.mainloop()

    def getDownloadBool(self):
        """
        Returns whether the config should allow datasheet download or not
        :return: True or False to download datasheets
        :rtype: bool
        """

        return self.config.get('main', 'downloadDatasheets')

    def setDownloadBool(self, downloadBool):
        """
        Sets the downloadDatasheets boolean from the settings page
        :param downloadBool: Sets the boolean key in the config file
        :type downloadBool: bool
        """
        self.config.set('main', 'downloadDatasheets', downloadBool)
        with open('config.ini', 'r+') as f:
            self.config.write(f)
        f.close()

    def getAPIKey(self):
        """
        Returns the API key
        :return: API Key
        :rtype: str
        """
        apiKey = self.config.get('main', 'api')
        return apiKey

    def setAPIKey(self, api):
        """
        Sets the API key from the settings page
        :param api: Sets the API key in the config file
        :type api: str
        """
        self.config.set('main', 'api', api)
        with open('config.ini', 'r+') as f:
            self.config.write(f)
        f.close()

    def combine_funcs(*funcs):
        """
        combine_funcs from
        http://stackoverflow.com/questions/13865009/have-multiple-commands-when-button-is-pressed-in-tkinter-
        with-python-2-7
        :param funcs: List of functions to be combined
        """
        def combined_func(*args, **kwargs):
            for f in funcs:
                f(*args, **kwargs)

        return combined_func
