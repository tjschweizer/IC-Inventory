"""
IC Inventory

Search Screen Setup

by Taylor Schweizer
"""

# Import Statements
from MultiListBox import MultiListbox
from OctoUtils import *
from tkinter import *

class SearchScreen(Frame):
    # Override init
    def __init__(self, master, settings):
        # Initialize the Frame
        Frame.__init__(self, master)

        # Pack the Frame
        self.pack()

        # Initialize some variables
        self.currentPage = 1
        self.maxPages = 1

        #Create the widgets
        self.createWidgets()
        self.initializeWidgets()
        self.settings = settings

    def nextPage(self):
        self.currentPage = self.currentPage + 1
        self.performOctoSearch()

    def prevPage(self):
        self.currentPage = self.currentPage - 1
        self.performOctoSearch()

    def createWidgets(self):
        # Search Bar
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
        self.imageLabel = Label(self, text='Image')
        self.imageLabel.grid(row=1, column=2, pady=5)

        # The results boxes need to be made out of a custom class. I am using the code from this website:
        # http://www.mypythonadventure.com/2014/03/18/a-quest-begins/
        # to create a MultiListbox class
        self.resultListLabels = ['Part Number', 'Manufacturer', 'Description']
        self.resultsListWidths = (20, 25, 75)
        self.resultsList = MultiListbox(self, self.resultListLabels, self.resultsListWidths, NORMAL, False)
        self.resultsList.grid(row=2, column=0, padx=10, pady=5)

        # Repeat the previous to make a box for the tech specs
        self.techSpecsLabels = ['Description', 'Value']
        self.techSpecsWidths = (30, 30)
        self.techSpecsFrame = Frame(self)
        self.techSpecsFrame.grid(row=2, column=1, padx=10, pady=5)
        self.techScroll = Scrollbar(self.techSpecsFrame, orient=VERTICAL)
        self.techScroll.grid(row=0, column=1, sticky=N + S)
        self.techSpecsList = MultiListbox(self.techSpecsFrame, self.techSpecsLabels, self.techSpecsWidths, DISABLED,
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

        # Image placeholder
        self.imageFrame = Frame(self, width=300)
        self.imageFrame.grid(row=2, column=2)
        self.imageFrame.grid_propagate(0)

    def initializeWidgets(self):
        self.searchText['textvariable'] = self.searchQuery
        self.searchButton['command'] = lambda: self.performOctoSearch(reset=True)
        self.nextPageButton['command'] = self.nextPage
        self.prevPageButton['command'] = self.prevPage
        self.showTechSpecButton['command'] = self.showTechSpecs
        self.prevPageButton['state'] = DISABLED
        self.nextPageButton['state'] = DISABLED
        self.inventoryButton['command'] = lambda: self.settings.inventory.addToInventory(self.techSpecDict,
                                                                                         self.quantitySpinbox.get())

    def showTechSpecs(self):
        row = self.searchResults[self.resultsList.getSelectedRow()]
        uid = row[3]
        self.techSpecDict = getTechSpecs(self.settings.getAPIKey(), uid)
        self.techSpecsList.techSpecEnable()
        self.techSpecsList.addTechSpec(self.techSpecDict['specs'])

    def performOctoSearch(self, reset=False):
        self.searchResults = None
        if (reset == True):
            self.currentPage = 1

        if self.currentPage <= 1:
            self.currentPage = 1
            self.prevPageButton['state'] = DISABLED
        else:
            self.prevPageButton['state'] = NORMAL

        startNumber = self.currentPage * 10 - 10
        octoDict = octoSearch(self.settings.getAPIKey(), startNumber, self.searchQuery.get())
        self.maxPages = getMaxPages(getHits(octoDict))

        if self.currentPage >= self.maxPages:
            self.currentPage = self.maxPages
            self.nextPageButton['state'] = DISABLED
        else:
            self.nextPageButton['state'] = NORMAL

        self.searchResults = []
        for result in octoDict['results']:
            item = result['item']
            self.searchResults.append((item['mpn'], item['brand']['name'], item['short_description'], item['uid']))

        self.resultsList.addItem(self.searchResults)
        self.pageNavigationLabel['text'] = 'Page {0} of {1}'.format(self.currentPage, self.maxPages)
