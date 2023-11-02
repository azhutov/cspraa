from Prototype.GenericQPUGenerator import GenericQPUGenerator, AtomSpec
import numpy as np

class ArbitraryConnectivityQPUGenerator(GenericQPUGenerator):

    def __init__(self, 
                 weights_detuning_fraction: float,
                 copy_gadget_detuning_correction: float,
                 next_nearest_neighbour_detuning_correction: float,
                 *args):
        self.weights_detuning_fraction = weights_detuning_fraction
        self.copy_gadget_detuning_correction = copy_gadget_detuning_correction
        self.next_nearest_neighbour_detuning_correction = next_nearest_neighbour_detuning_correction
        super().__init__(*args)

    def convert(self):
        """Returns a dictionary with the following keys:
            - "atom_specs": A list of atom specs.
            - "rydberg_radius": The desired rydberg radius for the algorithm.
        """
        atom_specs = []
        rydberg_radius = self.atomic_min_distance * np.sqrt(5) / 4

        # for i in range()
        # self.add_target_line()

        