from tkinter import *
from tkinter.ttk import *


class MultiListbox(Frame):
    """
    MultiListbox is a tkinter listbox with multiple columns
    """

    def __init__(self, labels, widths, master=NONE, listState=NORMAL, scrollbar=False):
        """
        Initialization method

        :param labels: List[] of the column labels
        :type labels: list
        :param widths: List[] of column widths
        :type widths: list
        :param master: Parent tkinter object
        :type master:
        :param listState: Tkinter state, NORMAL makes the list enabled, DISABLED disables the list
        :type listState: tkinter.state
        :param scrollbar: Boolean that enables or disables a scrollbar
        :type scrollbar: bool
        """

        Frame.__init__(self, master)
        self.labels = labels
        self.widths = widths
        self.lists = []
        i = 0
        for j in labels:
            frame = Frame(self)
            frame.grid(row=0, column=i)
            Label(frame, text=j, borderwidth=1, relief=RAISED).grid(row=0, column=i, sticky=E + W)
            lb = Listbox(frame, width=widths[i], borderwidth=0, selectborderwidth=0, highlightthickness=0,
                         relief=FLAT, exportselection=FALSE, selectmode=SINGLE, activestyle='none',
                         disabledforeground='black')
            lb.grid(row=1, column=i, sticky=N + S + E + W)
            lb.bind('<1>', lambda e, s=self: s._select(e.y))
            for k in range(0, 9):
                lb.insert(k, ' ')
            lb.configure(state=listState)
            self.lists.append(lb)
            i = i + 1

        if scrollbar == True:
            scrollbarHandle = Scrollbar(self.master, orient=VERTICAL)
            scrollbarHandle.grid(row=0, column=1, sticky=N + S + E)
            for i in range(0, len(self.lists)):
                self.lists[i]['yscrollcommand'] = scrollbarHandle.set
                scrollbarHandle['command'] = self.OnVsb
            for i in range(0, len(self.lists)):
                self.lists[i].bind("<MouseWheel>", self.OnMouseWheel)


    def _select(self, y):
        """
        Determines which row is selected, and selects all columns in the row

        :param y: tkinter event
        :type y: tkinter.event
        """
        self.row = self.lists[0].nearest(y)
        for l in self.lists:
            l.selection_clear(0, l.size())
            l.selection_set(self.row)
            l.focus_set()
        return 'break'

    def addList(self, listAdd):
        """
        Adds listAdd to the lists

        :param listAdd: nested list to add
        :type listAdd: list
        """
        for i in range(0, len(self.lists)):
            self.lists[i].delete(0, self.lists[i].size() - 1)

        for i in range(0, len(listAdd)):
            for j in range(0, len(listAdd[i])):
                self.lists[j].insert(i, listAdd[i][j])

    def listEnable(self):
        """
        Enables the multilistbox
        """
        for i in range(0, len(self.lists)):
            self.lists[i].configure(state=NORMAL)

    def listDisable(self):
        """
        Disables the multilistbox
        """
        for i in range(0, len(self.lists)):
            self.lists[i].configure(state=DISABLED)

    def getSelectedRow(self):
        """
        Returns the selected row
        """
        return self.row

    def bindScroll(self):
        """
        Binds the scrollbar to the lists
        """
        for i in range(0, len(self.lists)):
            self.lists[i].bind("<MouseWheel>", self.OnMouseWheel)


    def OnVsb(self, *args):
        """
        Something about capturing an event
        """
        for i in range(0, len(self.lists)):
            self.lists[i].yview(*args)

    def OnMouseWheel(self, event):
        """
        Something about the mouse scroll wheel
        """
        scrollAmount = int(-event.delta / 120)
        for i in range(0, len(self.lists)):
            self.lists[i].yview_scroll(scrollAmount, UNITS)
        # this prevents default bindings from firing, which
        # would end up scrolling the widget twice
        return "break"
