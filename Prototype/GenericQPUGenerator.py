from Prototype.crystal_structure import CrystalStructure
from typing import List, Dict, Tuple

class AtomSpec:

    def __init__(self, position: Tuple, detuning: float, target: int):
        """_summary_

        Args:
            position (Tuple): A tuple containing the coordinates of the atom in the QPU.
            detuning (float): A float determining the relative detuning of the atom, in units of delta_max.
            target (int): An integer determining the target of the qubit. If the qubit is ancillary, this value is -1.
        """
        self.position = position
        self.detuning = detuning
        self.target = target

    def getPosition(self):
        return self.position
    
    def getDetuning(self):
        return self.detuning
    
    def setPosition(self, position):
        self.position = position

    def setDetuning(self, detuning):
        self.detuning = detuning

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