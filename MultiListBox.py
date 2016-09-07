from tkinter import *
from tkinter.ttk import *


class MultiListbox(Frame):
    def __init__(self, labels, widths, master=NONE, listState=NORMAL, scrollbar=False, scrollbarHandle=NONE):
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
            lb.configure(state=listState)
            self.lists.append(lb)
            i = i + 1
        if scrollbar == True:
            for i in range(0, len(self.lists)):
                self.lists[i]['yscrollcommand'] = scrollbarHandle.set
                scrollbarHandle['command'] = self.OnVsb
            for i in range(0, len(self.lists)):
                self.lists[i].bind("<MouseWheel>", self.OnMouseWheel)


    def _select(self, y):
        self.row = self.lists[0].nearest(y)
        for l in self.lists:
            l.selection_clear(0, l.size())
            l.selection_set(self.row)
            l.focus_set()
        return 'break'

    def addOctopartList(self, octoList):
        for i in range(0, len(self.lists)):
            self.lists[i].delete(0, self.lists[i].size() - 1)
        for i in range(0, len(octoList)):
            self.lists[0].insert(i, octoList[i].mpn)
            self.lists[1].insert(i, octoList[i].manufacturer)
            self.lists[2].insert(i, octoList[i].shortDescription)

    def addTechSpecList(self, octoPart):
        for i in range(0, len(self.lists)):
            self.lists[i].delete(0, self.lists[i].size() - 1)
        for i in range(0, len(octoPart.specs)):
            self.lists[0].insert(i, octoPart.specs[i]['name'])
            self.lists[1].insert(i, octoPart.specs[i]['value'])

    def listEnable(self):
        for i in range(0, len(self.lists)):
            self.lists[i].configure(state=NORMAL)

    def getSelectedRow(self):
        return self.row

    def bindScroll(self):
        for i in range(0, len(self.lists)):
            self.lists[i].bind("<MouseWheel>", self.OnMouseWheel)


    def OnVsb(self, *args):
        for i in range(0, len(self.lists)):
            self.lists[i].yview(*args)

    def OnMouseWheel(self, event):
        scrollAmount = int(-event.delta / 120)
        for i in range(0, len(self.lists)):
            self.lists[i].yview_scroll(scrollAmount, UNITS)
        # this prevents default bindings from firing, which
        # would end up scrolling the widget twice
        return "break"
