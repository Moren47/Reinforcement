from tkinter import *

PI = 3.1415926525
PHI_SIGN = "\u03A6"
DEFAULT_FI = PHI_SIGN + u"12"
EMPTY = " - "
PHI_LIST = (
    EMPTY,
    PHI_SIGN + u"8",
    PHI_SIGN + u"10",
    PHI_SIGN + u"12",
    PHI_SIGN + u"16",
    PHI_SIGN + u"20",
    PHI_SIGN + u"25",
)
DEFAULT_DIST = 15
DIST_FROM = 1
DIST_TO = 50
RHO_STEEL = 0.786 #kg/cm2/m
BLACK = "#000000"


class Result(Frame):
    def __init__(self, master, name_left='', name_right=''):
        Frame.__init__(self, master)
        self._label_1 = Label(self, width=15, text=name_left, anchor='e')
        self._label_1.grid(row=0, column=1, pady=3, sticky='E')
        self._entry = Entry(self, state=DISABLED, width=7, justify=CENTER, disabledforeground=BLACK)
        self._entry.grid(row=0, column=2, pady=3)
        self._label_2 = Label(self, width=15, text=name_right, anchor='w')
        self._label_2.grid(row=0, column=3, pady=3, sticky='W')

    def update_result(self, value):
        self._entry['state'] = NORMAL
        self._entry.delete(0, 'end')
        self._entry.insert(0, str(value))
        self._entry['state'] = DISABLED


class ManyBarsDlg(Frame):
    def __init__(self, master, command=None):
        Frame.__init__(self, master)
        self._command = command
        self.menu_variable = StringVar(self)
        self.menu_variable.set(DEFAULT_FI)

        self.menu = OptionMenu(self, self.menu_variable, *PHI_LIST, command=self.command)
        self.menu.grid(row=0, column=1, padx=3, pady=3, sticky='WES')
        self.grid_columnconfigure(1, minsize=80)

        self.scale_variable = IntVar(self)
        self.scale = Scale(self, variable=self.scale_variable, from_=DIST_FROM, to=DIST_TO,
                           orient=HORIZONTAL, command=self.command)
        self.scale.grid(row=0, column=2, padx=3, pady=3, sticky='WEN')
        self.grid_columnconfigure(2, minsize=300)

    def get(self):
        return self.scale.get()

    def command(self, _):
        if self._command is not None:
            variables = (self.menu_variable.get(), self.scale_variable.get())
            self._command(variables)

    def update(self):
        self.scale.update()
        self.menu.update()
        self.scale.set(DEFAULT_DIST)


master = Tk()
master.title(u'Kalkulator masy zbrojenia')
master.iconbitmap('icon.ico')
master.resizable(0, 0)

w1_variable = DoubleVar()
w2_variable = DoubleVar()

def get_weight(vars):
    if vars[0] == EMPTY:
        return 0.
    return (PI*(int(vars[0][1:])/10)**2./4. * 100. / float(vars[1]))

def w1_command(vars):
    w1_variable.set(get_weight(vars))
    update_command()

w1 = ManyBarsDlg(master, command=w1_command)
w1.pack()

def w2_command(vars):
    w2_variable.set(get_weight(vars))
    update_command()

w2 = ManyBarsDlg(master, command=w2_command)
w2.pack()

result_1 = Result(master, name_left="Pole zbrojenia ", name_right=" cm\u00B2/m")
result_1.pack(pady=5)

result_2 = Result(master, name_left="Masa zbrojenia ", name_right=" kg/m")
result_2.pack(pady=5)

def update_command():
    value = (w1_variable.get() + w2_variable.get())
    result_1.update_result("%.3f" % value)
    result_2.update_result("%.3f" % (value*RHO_STEEL))

w1.update()
w2.update()

mainloop()


