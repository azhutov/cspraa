from Prototype.crystals.crystal_structure import CrystalStructure
from typing import Dict
import numpy as np

class GenericQPUGenerator:

    def __init__(self, 
                 crystal: CrystalStructure, 
                 atomic_min_distance: float = 1):
        self.crystal = crystal
        self.dimension = crystal.dimension
        self.positions = crystal.positions
        self.potentials = crystal.potentials
        self.interactions = crystal.interactions
        self.atomic_min_distance = atomic_min_distance
    
    def convert(self) -> Dict:
        """Returns a dictionary with the following keys:
            - "atom_specs": A list of atom specs.
            - "rydberg_radius": The desired rydberg radius for the algorithm.
        """
        raise NotImplementedError("This is a generic class")