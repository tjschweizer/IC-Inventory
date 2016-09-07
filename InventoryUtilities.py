import pickle


class Inventory:
    def __init__(self, filename):
        self.invFile = filename
        self.inventory = []

    def createInventory(self):
        openedFile = open(self.invFile, 'wb')
        tmp = []
        pickle.dump(tmp, openedFile)
        openedFile.close()

    def openInventory(self):
        openedFile = open(self.invFile, 'rb+')
        self.inventory = pickle.load(openedFile)
        openedFile.close()

    def saveInventory(self):
        openedFile = open(self.invFile, 'rb+')
        tmp = sorted(self.inventory, key=lambda part: part.mpn)
        pickle.dump(tmp, openedFile)
        openedFile.close()
        self.openInventory()

    def searchInventory(self, octoPart):
        index = -1
        for i in range(len(self.inventory)):
            if self.inventory[i].uid == octoPart.uid:
                index = i
                break
        return index

    def addToInventory(self, octoPart, quantity):
        index = self.searchInventory(octoPart)
        if index == -1:
            octoPart.quantity = quantity
            self.inventory.append(octoPart)
        else:
            self.inventory[index].quantity += quantity
        self.saveInventory()
