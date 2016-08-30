"""
IC Inventory

Search Screen Setup

by Taylor Schweizer
"""

#Import Statements
from tkinter import *
from tkinter.ttk import *

#Search Screen Class
class SearchScreen(Frame):

    #Override init
    def __init__(self,master):
        Frame.__init__(self,master)
        self.pack()
        self.createWidgets()

    #Here we will create all of the widgets
    def createWidgets(self):

        #Start with the search bar
        searchText=Entry(self)
        searchText.grid(row=0,column=0,padx=10,sticky=EW)

        #Search button
        searchButton = Button(self,text='Search')
        searchButton.grid(row=0,column=1,sticky=W,pady=5)

        #Results label
        resultsLabel = Label(self,text='Results')
        resultsLabel.grid(row=1,column=0,pady=5)

        #Tech specs label
        specsLabel=Label(self,text='Tech Specs')
        specsLabel.grid(row=1,column=1,pady=5)

        #Image label
        imageLabel = Label(self,text='Image')
        imageLabel.grid(row=1,column=2,pady=5)

        #The results boxes need to be made out of a custom class. I am using the code from this website:
        #http://www.mypythonadventure.com/2014/03/18/a-quest-begins/
        #to create a MultiListbox class
        resultListLabels = ['Part Number','Manufacturer']
        resultsListWidths=(30,30)
        resultsList = MultiListbox(self,resultListLabels,resultsListWidths,NORMAL)
        resultsList.grid(row=2,column=0,padx=10,pady=5)

        #Repeat the previous to make a box for the tech specs
        techSpecsLabels=['Description','Value']
        techSpecsWidths=(30,30)
        techSpecsList=MultiListbox(self,techSpecsLabels,techSpecsWidths,DISABLED)
        techSpecsList.grid(row=2,column=1,padx=10,pady=5)

        #Show text specs button
        showTechSpecs=Button(self,text='Show Tech Specs')
        showTechSpecs.grid(row=3,column=0,pady=5)

        #Page control buttons - need to make new frame for grid layout
        pageNavigationFrame = Frame(self)
        pageNavigationFrame.grid(row=4,column=0,pady=5)
        prevPage = Button(pageNavigationFrame,text='Prev')
        prevPage.grid(row=0,column=0)
        nextPage=Button(pageNavigationFrame,text='Next')
        nextPage.grid(row=0,column=2)
        pageNavigationLabel = Label(pageNavigationFrame,text='Page _ of _')
        pageNavigationLabel.grid(row=0,column=1)

        #Add to inventory button
        inventoryFrame = Frame(self)
        inventoryFrame.grid(row=3,column=1,pady=5)
        quantitySpinbox = Spinbox(inventoryFrame,from_=0,to_=100,increment=1,text='Qty:')
        quantitySpinbox.grid(row=0,column=0)
        inventoryButton=Button(inventoryFrame,text='Add to Inventory')
        inventoryButton.grid(row=0,column=1)

        #Image placeholder
        imageFrame = Frame(self,width=300)
        imageFrame.grid(row=2,column=2)
        imageFrame.grid_propagate(0)
class MultiListbox(Frame):


    def __init__(self, master,labels,widths,st):
        Frame.__init__(self, master)
        self.labels=labels
        self.widths=widths
        self.lists=[]
        i=0
        for j in labels:
            frame=Frame(self)
            frame.pack(side=LEFT,expand=TRUE,fill=BOTH)
            Label(frame,text=j,borderwidth=1,relief=RAISED).pack(fill=X)
            lb=Listbox(frame,width=widths[i],borderwidth=0, selectborderwidth=0,highlightthickness=0,
                 relief=FLAT, exportselection=FALSE,selectmode=SINGLE,activestyle='none',disabledforeground='black')
            lb.pack(expand=YES,fill=BOTH)
            lb.bind('<1>',lambda e,s=self:s._select(e.y))
            for k in range(0,10):
                lb.insert(k,'example')
            lb.configure(state=st)
            self.lists.append(lb)
            i=i+1
    def _select(self,y):
        row=self.lists[0].nearest(y)
        for l in self.lists:
            l.selection_clear(0,l.size())
            l.selection_set(row)
            l.focus_set()
        return 'break'
