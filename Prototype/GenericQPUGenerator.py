from Prototype.crystal_structure import CrystalStructure

class GenericQPUGenerator:

    def __init__(self, 
                 crystal: CrystalStructure, 
                 atomic_min_distance: float):
        self.crystal = crystal
        self.dimension = crystal.dimension
        self.positions = crystal.positions
        self.potentials = crystal.potentials
        self.interactions = crystal.interactions
        self.atomic_min_distance = atomic_min_distance
    
    def convert(self):
        """Returns a dictionary with the following keys:
            - "positions": A list of tuples (size 2 or 3 depending on crystal dimension) containing the position of the atoms.
            - "detunings": A list of floats containing the detunings corresponding to each atom. This list must  be normalized such that the largest value in the list is 1.
        """
        raise NotImplementedError("This is a generic class")