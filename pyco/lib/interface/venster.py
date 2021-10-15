import pyco.model as pycom

import tkinter as tk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Venster(pycom.BasisObject):
    """
    Verzorgt uitvoer in nieuw venster gebruik makend van tkinter bibliotheek.
    """

    def __init__(self,
                 breedte:int=600,
                 hoogte:int=600,
                 titel:str='pyco'):
        super().__init__()

        self.breedte = breedte
        self.hoogte = hoogte

        self.root = tk.Tk()
        self.root.title(titel)
        self.root.geometry('{}x{}'.format(self.breedte, self.hoogte))

    def tekst(self, tekst:str):
        s = tk.Scrollbar(self.root, width=20)
        s.pack(side=tk.RIGHT, fill=tk.Y)

        t = tk.Text(self.root, yscrollcommand=s.set, width=self.breedte-22)
        t.insert(tk.INSERT, tekst)
        t.config(state='disabled')
        t.pack(side=tk.LEFT, fill=tk.BOTH)
        s.config(command=t.yview)

        self.root.mainloop()

    def figuur(self, figuur:pycom.Figuur):
        canvas = FigureCanvasTkAgg(figuur.fig, master=self.root)
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1.0)
        canvas.draw()

        self.root.mainloop()
