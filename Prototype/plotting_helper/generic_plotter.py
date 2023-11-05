import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os

styles=[os.path.join(
    os.path.dirname(__file__),
    "style.mplstyle"
)]

def getStylishFigureAxes(nrows, ncols, **style):
    if style.get("figsize") is None:
        style["figsize"] = (2 * ncols, 2 * nrows)
    with plt.style.context(styles):
        fig, axes = plt.subplots(nrows, ncols, **style)

    if isinstance(axes, np.ndarray):
        return fig, axes.ravel()
    else:
        return fig, axes

class GenericPlotter:

    def __init__(self,
                 fig: matplotlib.figure.Figure,
                 ax: matplotlib.axes,
                 xlim = None,
                 ylim = None,
                 grid = False,
                 style = None,
                 xticks = None,
                 yticks = None,
                 xlabel = None,
                 ylabel = None,
                 title = None,
                 xlabel_font = None,
                 ylabel_font = None,
                 title_font = None):
        self.fig = fig
        self.ax = ax
        self.xlim = xlim
        self.ylim = ylim
        self.grid = grid
        self.style = style
        self.xticks = xticks
        self.yticks = yticks
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.title = title
        self.xlabel_font = xlabel_font
        self.ylabel_font = ylabel_font
        self.title_font = title_font

    def draw(self):
        result = self._draw()
            
        if self.grid:
            self.ax.grid()

        if self.xlabel is not None:
            if self.xlabel_font is None:
                self.ax.set_xlabel(self.xlabel)
            else:
                self.ax.set_xlabel(self.xlabel, font=self.xlabel_font)
        if self.ylabel is not None:
            if self.ylabel_font is None:
                self.ax.set_ylabel(self.ylabel)
            else:
                self.ax.set_ylabel(self.ylabel, font=self.ylabel_font)

        if self.title is not None:
            if self.title_font is None:
                self.ax.set_title(self.title)
            else:
                self.ax.set_title(self.title, font=self.title_font)

        self.setTicks()

        if self.xlim is not None:
            self.ax.set_xlim(self.xlim)
        if self.ylim is not None:
            self.ax.set_ylim(self.ylim)

        return result, self.fig, self.ax

    def setTicks(self):
        if self.xticks is not None:
            self.ax.set_xticks(self.xticks)
        if self.yticks is not None:
            self.ax.set_yticks(self.yticks)

    def _draw(self):
        raise NotImplementedError("Not implemented for the generic class")