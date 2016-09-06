import json
import shutil
import tempfile


class Inventory:
    def __init__(self, filename):
        self.invFile = filename

    def createInventory(self):
        openedFile = open(self.invFile, 'w+')
        openedFile.close()

    def searchInventory(self, jStream, uid):
        i = 0
        partList = jStream['part']
        for part in partList:
            if part['uid'] == uid:
                returnVal = i
                break
            else:
                returnVal = -1
            i = i + 1

        return returnVal

    def addToInventory(self, jsonString, quantity):
        openedFile = open(self.invFile, 'r+')
        tmpFile = tempfile.NamedTemporaryFile(mode='w+', delete=False)
        stream = json.load(openedFile)
        index = self.searchInventory(stream, jsonString['uid'])
        newStream = jsonString
        if int(quantity) < 1:
            openedFile.close()
            tmpFile.close()
            tmpFile.delete()
        else:

            if index == -1:
                newPart = {}
                newPart['quantity'] = quantity
                newPart['manufacturer'] = newStream['manufacturer']
                newPart['brand'] = newStream['brand']
                newPart['mpn'] = newStream['mpn']
                newPart['uid'] = newStream['uid']
                newPart['octopart_url'] = newStream['octopart_url']
                newPart['specs'] = newStream['specs']
                stream['part'].append(newPart)

            else:
                stream['part'][index]['quantity'] = quantity

            json.dump(stream, tmpFile)
            openedFile.close()

            tmpFile.close()
            shutil.move(tmpFile.name, self.invFile)
            tmpFile.delete
