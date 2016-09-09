from tkinter import *
from main.octopart.octo_utils import *
from main.utilities.multilistbox import MultiListbox


class SearchScreen(Frame):
    """
    Search Screen class shows the interface to search Octopart
    """
    def __init__(self, master, settings):
        """
        Init for SearchScreen
        :param master: Notebook tab
        :type master: tkinter.notebook
        :param settings: Settings object
        :type settings: utilities.global_settings.Settings
        """

        Frame.__init__(self, master)
        self.pack()
        self.currentPage = 1
        self.maxPages = 1
        self.createWidgets()
        self.initializeWidgets()
        self.settings = settings

    def nextPage(self):
        """
        Advances the search results by one page
        """
        self.currentPage = self.currentPage + 1
        self.performOctoSearch()

    def prevPage(self):
        """
        Goes back in the search results by on page
        """
        self.currentPage = self.currentPage - 1
        self.performOctoSearch()

    def createWidgets(self):
        """
        Creates all of the widgets on the Search Screen
        """

        # Search text box
        self.searchQuery = StringVar()
        self.searchText = Entry(self)
        self.searchText.grid(row=0, column=0, padx=10, sticky=EW)

        # Search button
        self.searchButton = Button(self, text='Search')
        self.searchButton.grid(row=0, column=1, sticky=W, pady=5)

        # Results label
        self.resultsLabel = Label(self, text='Results')
        self.resultsLabel.grid(row=1, column=0, pady=5)

        # Tech specs label
        self.specsLabel = Label(self, text='Tech Specs')
        self.specsLabel.grid(row=1, column=1, pady=5)

        # Image label
        self.descLabel = Label(self, text='Descriptions')
        self.descLabel.grid(row=1, column=2, pady=5)

        # The results boxes need to be made out of a custom class. I am using the code from this website:
        # http://www.mypythonadventure.com/2014/03/18/a-quest-begins/
        # to create a MultiListbox class
        self.resultListLabels = ['Part Number', 'Manufacturer', 'Description']
        self.resultsListWidths = (20, 25, 75)
        self.resultsList = MultiListbox(self.resultListLabels, self.resultsListWidths, self, NORMAL, False)
        self.resultsList.grid(row=2, column=0, padx=10, pady=5)

        # Repeat the previous to make a box for the tech specs
        self.techSpecsLabels = ['Description', 'Value']
        self.techSpecsWidths = (30, 30)
        self.techSpecsFrame = Frame(self)
        self.techSpecsFrame.grid(row=2, column=1, padx=10, pady=5)
        self.techSpecsList = MultiListbox(self.techSpecsLabels, self.techSpecsWidths, self.techSpecsFrame, DISABLED,
                                          True)
        self.techSpecsList.grid(row=0, column=0, padx=10, pady=5)

        # Show text specs button
        self.showTechSpecButton = Button(self, text='Show Tech Specs')
        self.showTechSpecButton.grid(row=3, column=0, pady=5)

        # Page control buttons - need to make new frame for grid layout
        self.pageNavigationFrame = Frame(self)
        self.pageNavigationFrame.grid(row=4, column=0, pady=5)
        self.prevPageButton = Button(self.pageNavigationFrame, text='Prev')
        self.prevPageButton.grid(row=0, column=0)
        self.nextPageButton = Button(self.pageNavigationFrame, text='Next')
        self.nextPageButton.grid(row=0, column=2)
        self.pageNavigationLabel = Label(self.pageNavigationFrame, text='Page _ of _')
        self.pageNavigationLabel.grid(row=0, column=1)

        # Add to inventory button
        self.inventoryFrame = Frame(self)
        self.inventoryFrame.grid(row=3, column=1, pady=5)
        self.quantitySpinbox = Spinbox(self.inventoryFrame, from_=0, to_=100, increment=1, text='Qty:')
        self.quantitySpinbox.grid(row=0, column=0)
        self.inventoryButton = Button(self.inventoryFrame, text='Add to Inventory')
        self.inventoryButton.grid(row=0, column=1)

        # Descriptions placeholder
        self.descText = Label(self, width=80)
        self.descText.grid(row=2, column=2)

    def initializeWidgets(self):
        """
        Assigns commands and states to widgets
        """
        self.searchText['textvariable'] = self.searchQuery
        self.searchButton['command'] = lambda: self.performOctoSearch(reset=True)
        self.nextPageButton['command'] = self.nextPage
        self.prevPageButton['command'] = self.prevPage
        self.showTechSpecButton['command'] = self.showTechSpecs
        self.prevPageButton['state'] = DISABLED
        self.nextPageButton['state'] = DISABLED
        self.inventoryButton['state'] = DISABLED
        self.inventoryButton['command'] = lambda: self.settings.inventory.addToInventory(self.activeOctopart,
                                                                                         self.quantitySpinbox.get())
        self.quantitySpinbox['command'] = self.invButtonState

    def invButtonState(self):
        """
        Configures the state of the inventory button
        """
        if int(self.quantitySpinbox.get()) == 0:
            self.inventoryButton.configure(state=DISABLED)
        else:
            self.inventoryButton.configure(state=NORMAL)

    def showTechSpecs(self):
        """
        Shows the tech specs in a multilistbox
        """
        row = self.resultsList.getSelectedRow()
        self.activeOctopart = self.octoList[row]
        self.activeOctopart.getTechSpecs(self.settings.getAPIKey(), images=False, description=True, datasheets=True)
        self.techSpecsList.listEnable()
        self.techSpecsList.addList(self.octoList[row].specs)
        s = ''
        for i in range(0, len(self.octoList[row].descriptions)):
            s += '\n'
            s += self.octoList[row].descriptions[i]
            s += '\n'

        self.descText['text'] =s

    def performOctoSearch(self, reset=False):
        """
        Searches Octopart for the search text and handles the page turn buttons
        """
        self.searchResults = None
        if (reset == True):
            self.currentPage = 1
        if self.currentPage <= 1:
            self.currentPage = 1
            self.prevPageButton['state'] = DISABLED
        else:
            self.prevPageButton['state'] = NORMAL
        startNumber = self.currentPage * 10 - 10
        self.octoList = octoSearch(self.settings.getAPIKey(), startNumber, self.searchQuery.get())
        self.maxPages = self.octoList[len(self.octoList) - 1]
        self.octoList.remove(self.maxPages)
        if self.currentPage >= self.maxPages:
            self.currentPage = self.maxPages
            self.nextPageButton['state'] = DISABLED
        else:
            self.nextPageButton['state'] = NORMAL
        self.resultsList.addList(getOctoList(self.octoList))
        self.pageNavigationLabel['text'] = 'Page {0} of {1}'.format(self.currentPage, self.maxPages)
