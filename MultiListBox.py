from tkinter import *
from tkinter.ttk import *


class MultiListbox(Frame):
    def __init__(self, master, labels, widths, st, scrollbar):
        Frame.__init__(self, master)
        self.labels = labels
        self.widths = widths
        self.lists = []
        i = 0
        for j in labels:
            frame = Frame(self)
            frame.pack(side=LEFT, expand=TRUE, fill=BOTH)
            Label(frame, text=j, borderwidth=1, relief=RAISED).pack(fill=X)
            lb = Listbox(frame, width=widths[i], borderwidth=0, selectborderwidth=0, highlightthickness=0,
                         relief=FLAT, exportselection=FALSE, selectmode=SINGLE, activestyle='none',
                         disabledforeground='black')
            lb.pack(expand=YES, fill=BOTH)
            lb.bind('<1>', lambda e, s=self: s._select(e.y))
            for k in range(0, 9):
                lb.insert(k, ' ')
            lb.configure(state=st)
            self.lists.append(lb)
            i = i + 1
        if scrollbar == True:
            self.lists[0]['yscrollcommand'] = self.master.master.techScroll.set
            self.lists[1]['yscrollcommand'] = self.master.master.techScroll.set
            self.master.master.techScroll['command'] = self.OnVsb
            self.lists[0].bind("<MouseWheel>", self.OnMouseWheel)
            self.lists[1].bind("<MouseWheel>", self.OnMouseWheel)

    def _select(self, y):
        self.row = self.lists[0].nearest(y)
        for l in self.lists:
            l.selection_clear(0, l.size())
            l.selection_set(self.row)
            l.focus_set()
        return 'break'

    def addItem(self, item):
        self.lists[0].delete(0, 9)
        self.lists[1].delete(0, 9)
        self.lists[2].delete(0, 9)
        for i in range(0, 10):
            for j in range(0, 3):
                self.lists[j].insert(i, item[i][j])

    def techSpecEnable(self):
        self.lists[0].configure(state=NORMAL)
        self.lists[1].configure(state=NORMAL)

    def addTechSpec(self, specList):

        self.lists[0].delete(0, 9)
        self.lists[1].delete(0, 9)
        i = 0
        for spec in specList:
            specData = specList[spec]
            self.lists[0].insert(i, specData['metadata']['name'])
            valueString = specData['display_value']
            # if(specData['metadata']['unit']!=None):
            #    valueString += '  '
            #    valueString += specData['metadata']['unit']['symbol']
            self.lists[1].insert(i, valueString)
            i += 1

    def getSelectedRow(self):

        return self.row

    def bindScroll(self):
        self.lists[0].bind("<MouseWheel>", self.OnMouseWheel)
        self.lists[1].bind("<MouseWheel>", self.OnMouseWheel)

    def OnVsb(self, *args):
        self.lists[0].yview(*args)
        self.lists[1].yview(*args)

    def OnMouseWheel(self, event):
        scrollAmount = int(-event.delta / 120)
        self.lists[0].yview_scroll(scrollAmount, UNITS)
        self.lists[1].yview_scroll(scrollAmount, UNITS)
        # this prevents default bindings from firing, which
        # would end up scrolling the widget twice
        return "break"
