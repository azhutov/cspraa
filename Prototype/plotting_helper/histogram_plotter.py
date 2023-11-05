from Prototype.plotting_helper.generic_plotter import GenericPlotter
import numpy as np
import matplotlib


class HistogramPlotter(GenericPlotter):

    def __init__(self, 
                 fig: matplotlib.figure.Figure, 
                 ax: matplotlib.axes, 
                 data, 
                 range,
                 **inputs):
        super().__init__(fig, ax, **inputs)
        self.data = data
        self.range = range

        if self.style is not None and self.style.get("align") is None:
            self.style["align"] = "mid"

    def _draw(self):
        counts, bins = np.histogram(self.data, self.range)
        if self.style is None:
            return self.ax.hist(bins[:-1], bins, weights=counts)
        else:
            return self.ax.hist(bins[:-1], bins, weights=counts, **self.style)