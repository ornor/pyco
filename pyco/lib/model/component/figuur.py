# import pyco.toepassing as pycot
import pyco.model as pycom
# import pyco.functies as pycof
# import pyco.data as pycod

import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.patches as mpatches

from typing import Union

import numpy as np
import os
import shutil
import tkinter as tk
from tkinter.filedialog import asksaveasfile

# verbergen van waarschuwingen van Matplotlib
import warnings
warnings.filterwarnings('ignore')


class Figuur(pycom.BasisObject):

    def __init__(self,
                 breedte=8,
                 hoogte=8,
                 raster:bool=False,
                 legenda:bool=False,
                 titel:str='',
                 x_as_titel:str='',
                 y_as_titel:str='',
                 gelijke_assen:bool=False,
                 verberg_assen:bool=False,
                 x_as_log:bool=False,
                 y_as_log:bool=False):

        super().__init__()

        self.fig, self.ax = plt.subplots(1, 1, figsize=(breedte, hoogte))

        self.min_x = None
        self.max_x = None
        self.min_y = None
        self.max_y = None

        self.marge_x = 0.05
        self.marge_y = 0.05

        self.maak_raster=raster
        self.maak_legenda=legenda

        if self.maak_raster:
           self.ax.axhline(y=0, color='darkgrey', linewidth=1.2)
           self.ax.axvline(x=0, color='darkgrey', linewidth=1.2)

        if titel != '':
            self.ax.set_title(titel)
        if x_as_titel != '':
            self.ax.set_xlabel(x_as_titel)
        if y_as_titel != '':
            self.ax.set_ylabel(y_as_titel)

        if gelijke_assen:
            self.ax.axis('equal')

        if verberg_assen:
            self.ax.set_axis_off()

        if x_as_log:
            self.ax.set_xscale('log')

        if y_as_log:
            self.ax.set_yscale('log')

        # if True:
        #     self.ax.spines['top'].set_visible(False)

    def _check_coordinaten(self, coordinaten:Union[list, tuple]):
        if not isinstance(coordinaten, list) and not isinstance(coordinaten, tuple):
            raise ValueError('coordinaten is geen lijst of tupel')
        for coordinaat in coordinaten:
            if len(coordinaat) != 2:
                raise ValueError('coordinaat heeft minder of meer dan 2 elementen: {}'.format(coordinaat))

        x_waarden = [x for x, _ in coordinaten]
        y_waarden = [y for _, y in coordinaten]

        if self.min_x is not None:
            x_waarden = x_waarden + [self.min_x]
        if self.max_x is not None:
            x_waarden = x_waarden + [self.max_x]
        if self.min_y is not None:
            y_waarden = y_waarden + [self.min_y]
        if self.max_x is not None:
            y_waarden = y_waarden + [self.max_y]

        self.min_x = min(x_waarden)
        self.max_x = max(x_waarden)
        self.min_y = min(y_waarden)
        self.max_y = max(y_waarden)

        return coordinaten

    def lijn(self,
             coordinaten:Union[list, tuple],
             breedte=1,
             kleur='black',
             vullen=False,
             arcering='',
             naam:str=None):

        coordinaten = self._check_coordinaten(coordinaten)
        codes = [mpath.Path.MOVETO, *[mpath.Path.LINETO for _ in range(len(coordinaten)-1)]]
        path = mpath.Path(coordinaten, codes)
        patch = mpatches.PathPatch(path,
                                   linewidth=breedte,
                                   hatch=arcering,
                                   fill=vullen,
                                   color=kleur,
                                   label=naam)
        self.ax.add_patch(patch)
        return self

    def punt(self,
             coordinaten:Union[list, tuple],
             breedte=1,
             kleur='black',
             stijl='o',
             naam:str=None):

        coordinaten = self._check_coordinaten(coordinaten)
        X = [x for x, _ in coordinaten]
        Y = [y for _, y in coordinaten]
        self.ax.scatter(X, Y,
                        color=kleur,
                        marker=stijl,
                        s=breedte*30,
                        label=naam)
        return self

    def tekst(self,
             coordinaten:Union[list, tuple],
             teksten:Union[list, tuple],
             kleur='black',
             tekst_grootte:str='medium', # {'xx-small', 'x-small', 'small', 'medium', 'large', 'x-large', 'xx-large'}
             tekst_font:str='sans-serif', # {FONTNAME, 'serif', 'sans-serif', 'cursive', 'fantasy', 'monospace'}
             tekst_stijl:str='normal', # {'normal', 'italic', 'oblique'}
             tekst_gewicht:str='normal', # {'ultralight', 'light', 'normal', 'regular', 'book', 'medium', 'roman', 'semibold', 'demibold', 'demi', 'bold', 'heavy', 'extra bold', 'black'}
             hor_uitlijnen:str='center', # {'center', 'right', 'left'}
             vert_uitlijnen:str='center', # {'center', 'top', 'bottom', 'baseline', 'center_baseline'}
             roteren:Union[float, int, str]=0): # float in degrees

        coordinaten = self._check_coordinaten(coordinaten)
        X = [x for x, _ in coordinaten]
        Y = [y for _, y in coordinaten]
        for i, tekst in enumerate(teksten):
            x = X[i]
            y = Y[i]
            self.ax.text(x, y,
                            s=tekst,
                            color=kleur,
                            fontsize=tekst_grootte,
                            fontfamily=tekst_font,
                            fontstyle=tekst_stijl,
                            fontweight=tekst_gewicht,
                            horizontalalignment=hor_uitlijnen,
                            verticalalignment=vert_uitlijnen,
                            rotation=roteren)
        return self

    def kolom(self,
             coordinaten:Union[list, tuple],
             kleur:str='black',
             breedte:Union[float, int]=0.8,
             lijn_kleur:str='black',
             lijn_breedte:Union[float, int]=0,
             naam:str=None):

        waardes = self._check_coordinaten(coordinaten)
        X = [x for x, _ in waardes]
        hoogtes = [h for _, h in waardes]
        self.ax.bar(X,
                    height=hoogtes,
                    color=kleur,
                    width=breedte,
                    linewidth=lijn_breedte,
                    edgecolor=lijn_kleur,
                    label=naam)
        return self

    def fx(self,
           functie,
           x:Union[list, tuple],
           breedte=1,
           kleur='black',
           naam:str=None,
           aantal_punten=100):

        if len(x) != 2:
            raise ValueError('x waarde moet een lijst of tupel zijn met 2 getallen')

        X = np.linspace(x[0], x[1], aantal_punten)
        f = np.vectorize(functie)
        Y = f(X)

        self.min_x = min(self.min_x, x[0]) if self.min_x is not None else x[0]
        self.max_x = max(self.max_x, x[1]) if self.max_x is not None else x[1]
        self.min_y = min(self.min_y, min(Y)) if self.min_y is not None else min(Y)
        self.max_y = max(self.max_y, max(Y)) if self.max_y is not None else max(Y)

        self.ax.plot(X, Y, label=naam, color=kleur, linewidth=breedte)
        return self

    def __call__(self):
        min_x = self.min_x if self.min_x is not None else 0
        max_x = self.max_x if self.max_x is not None else 1
        min_y = self.min_y if self.min_y is not None else 0
        max_y = self.max_y if self.max_y is not None else 1

        marge_x = (max_x - min_x) * self.marge_x
        marge_y = (max_y - min_y) * self.marge_y

        self.ax.axis([min_x - marge_x, max_x + marge_x, min_y - marge_y, max_y + marge_y])

        if self.maak_raster:
           self.ax.grid(color='grey', linestyle='-', linewidth=0.2)

        if self.maak_legenda:
            self.ax.legend()

        self.fig.show()

        return self

    def bewaar_als_svg(self):
        FILENAME = 'tmp.svg'
        plt.savefig(FILENAME)

        class TkFileDialog(tk.Frame):
            def __init__(self, root):
                tk.Frame.__init__(self, root)
                button_opt = {'fill': tk.BOTH, 'padx': 5, 'pady': 5}
                tk.Button(self, text='bewaar figuur als SVG bestand', command=self.asksaveasfilename).pack(**button_opt)
                self.file_opt = options = {}
                options['filetypes'] = [('all files', '.*'), ('SVG bestand', '.svg')]
                options['initialfile'] = 'figuur.svg'
                options['parent'] = root

            def asksaveasfilename(self):
                new_filename = asksaveasfile(**self.file_opt)

                if new_filename:
                    shutil.copyfile(FILENAME, new_filename)

        root = tk.Tk()
        TkFileDialog(root).pack()
        root.mainloop()

        os.remove(FILENAME)
