from .errorbar_plotter import ErrorbarPlotter
from .image_plotter import ImagePlotter
from .plot_plotter import PlotPlotter
from .scatter_plotter import ScatterPlotter
from .histogram_plotter import HistogramPlotter
from .generic_plotter import getStylishFigureAxes

import numpy as np
import matplotlib.pyplot as plt

XLIM_PERCENTAGE = 0.1 # Margin added on both left and right as percentage of total width 
YLIM_PERCENTAGE = 0.1 # Margin added on both top and bottom as percentage of total height
    
def adjustAxisLimits(ax):
    ax.set_aspect("auto")
    ax.autoscale()
    ax.set_xmargin(XLIM_PERCENTAGE)
    ax.set_ymargin(YLIM_PERCENTAGE)

def plot_histogram_array(datas, 
                         rng, 
                         titles, 
                         ncols, 
                         style = {}, 
                         suptitle = None, 
                         suptitle_style = {}, 
                         title_style = {}, 
                         fig=None, 
                         ax=None):
    nrows = int(np.ceil(len(datas) / ncols))
    if fig is None:
        fig, ax = getStylishFigureAxes(nrows, ncols)
    
    for a, data, title in zip(ax, datas, titles):
        HistogramPlotter(
            fig = fig,
            ax = a,
            data = data,
            range = rng,
            title = title,
            title_font = title_style,
            style = style
        ).draw()
    for a in ax[len(datas):]:
        a.set_visible(False)

    if suptitle:
        plt.suptitle(suptitle, **suptitle_style)
    plt.tight_layout()

    return fig, ax

def plot_image_array(images, titles, ncols, style = {}, suptitle = None, suptitle_style = {}, title_style = {}, fig = None, ax = None):
    nrows = int(np.ceil(len(images) / ncols))
    if fig is None:
        fig, ax = getStylishFigureAxes(nrows, ncols)
    
    for a, im, title in zip(ax, images, titles):
        ImagePlotter(
            fig = fig,
            ax = a,
            image = im,
            colorbar = False,
            title = title,
            title_font = title_style,
            style = style,
            xticks = [],
            yticks = []
        ).draw()
    for a in ax[len(images):]:
        a.set_visible(False)

    if suptitle:
        plt.suptitle(suptitle, **suptitle_style)
    plt.tight_layout()

    return fig, ax

__all__ = [
    "ErrorbarPlotter",
    "ImagePlotter",
    "PlotPlotter",
    "ScatterPlotter",
    "HistogramPlotter",
    "getStylishFigureAxes",
    "adjustAxisLimits",
    "plot_histogram_array",
    "plot_image_array"
]