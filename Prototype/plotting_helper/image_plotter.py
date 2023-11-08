from Prototype.plotting_helper.generic_plotter import GenericPlotter
import matplotlib.pyplot as plt
import matplotlib


class ImagePlotter(GenericPlotter):

    def __init__(self, 
                 fig: matplotlib.figure.Figure, 
                 ax: matplotlib.axes, 
                 image,
                colorbar = True, 
                **inputs):
        if inputs.get("style") is None:
            inputs["style"] = {"origin": "lower"}
        if inputs["style"].get("origin") is None:
            inputs["style"]["origin"] = "lower"
        super().__init__(fig, ax, **inputs)
        self.image = image
        self.colorbar = colorbar

    def _draw(self):
        if self.style is None:
            im = self.ax.imshow(self.image)
        else:
            im = self.ax.imshow(self.image, **self.style)
        if self.colorbar:
            colorbar = plt.colorbar(im)
        else:
            colorbar = None
        return im, colorbar