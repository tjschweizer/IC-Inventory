import pickle
from urllib import request

class Inventory:
    """
    Inventory class is used to manage the local inventory of ICs. Class provides methods for working with the
    inventory file. Inventory is saved as a pickle stream
    """

    def __init__(self, filename):
        """
        Called on initialization of class. Assigns filename to object variable.

        :param filename: String representing the filename of the inventory file.
        :type filename: str
        """
        self.invFile = filename
        self.inventory = []

    def createInventory(self):
        """
        Creates a new file with the object's filename. Creates a temporary empty list and uses pickle to dump the list
        into the file. Closes the file before ending.

        :return: None
        :rtype: None
        """
        openedFile = open(self.invFile, 'wb')
        tmp = []
        pickle.dump(tmp, openedFile)
        openedFile.close()

    def openInventory(self):
        """
        Opens an inventory file with the object's filename and assigns the pickled list to an object variable.

        :return:
        :rtype:
        """
        openedFile = open(self.invFile, 'rb+')
        self.inventory = pickle.load(openedFile)
        openedFile.close()

    def saveInventory(self):
        """
        Pickle dumps the current inventory list to the object's filename. Calls self.openInventory() when finished.

        :return:
        :rtype:
        """
        openedFile = open(self.invFile, 'rb+')
        tmp = sorted(self.inventory, key=lambda part: part.mpn)
        pickle.dump(tmp, openedFile)
        openedFile.close()
        self.openInventory()

    def searchInventory(self, octoPart):
        """
        Searches the inventory list to see if the Octopart Item to be added is already in the inventory. This
        function is called by addToInventory().

        :param octoPart: Octopart object with a valid uid
        :type octoPart: octo_utils.Octopart
        :return: -1 if Octopart does not current exist in inventory, list index of part if it does
        :rtype: int
        """
        index = -1
        for i in range(len(self.inventory)):
            if self.inventory[i].uid == octoPart.uid:
                index = i
                break
        return index

    def addToInventory(self, octoPart, quantity):
        """
        Adds quantity of Octopart to the inventory. Performs a searchInventory to determine if part is already in
        inventory, then either adds the part to the inventory or simply updates the quantity if the part already
        exists.

        :param octoPart: Octopart object to add
        :type octoPart: octo_utils.Octopart
        :param quantity: Quantity of part to add to inventory
        :type quantity: int
        :return: None
        :rtype: None
        """
        index = self.searchInventory(octoPart)
        if index == -1:
            octoPart.quantity = quantity
            self.inventory.append(octoPart)
        else:
            self.inventory[index].quantity += quantity
        self.saveInventory()

        if octoPart.dataFile:
            request.urlretrieve(octoPart.dataURL, octoPart.dataFile)
