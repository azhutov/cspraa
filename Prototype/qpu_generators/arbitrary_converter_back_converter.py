from typing import List
import numpy as np
from .back_converter import BackConverter
from Prototype.crystals.crystal_structure import CrystalStructure

class ArbitraryConverterBackConverter(BackConverter):

    def __init__(self, qpu_properties: dict):
        super().__init__(qpu_properties)

    def _verify(self, state: List[int]):
        return True # Not implemented yet