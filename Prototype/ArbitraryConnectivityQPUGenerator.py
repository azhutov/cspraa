from Prototype.GenericQPUGenerator import GenericQPUGenerator

class ArbitraryConnectivityQPUGenerator(GenericQPUGenerator):

    def __init__(self, *args):
        super().__init__(*args)

    def convert(self):
        """Returns a dictionary with the following keys:
            - "positions": A list of tuples (size 2 or 3 depending on crystal dimension) containing the position of the atoms.
            - "detunings": A list of floats containing the detunings corresponding to each atom. This list must  be normalized such that the largest value in the list is 1.
        """
        