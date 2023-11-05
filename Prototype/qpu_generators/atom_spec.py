from typing import Tuple
import numpy as np

class AtomSpec:

    def __init__(self, position: Tuple, detuning: float, target: int):
        """_summary_

        Args:
            position (Tuple): A tuple containing the coordinates of the atom in the QPU.
            detuning (float): A float determining the relative detuning of the atom, in units of delta_max.
            target (int): An integer determining the target of the qubit. If the qubit is ancillary, this value is -1.
        """
        self.position = np.array(position)
        self.detuning = detuning
        self.target = target

    def getPosition(self):
        return self.position
    
    def getDetuning(self):
        return self.detuning

    def getTarget(self):
        return self.target
    
    def setPosition(self, position):
        self.position = position

    def setDetuning(self, detuning):
        self.detuning = detuning

    def setTarget(self, target):
        self.target = target