from typing import List
import numpy as np

class BackConverter:

    def __init__(self, qpu_properties: dict):
        self.qpu_properties = qpu_properties
        
        self.bits_count = 0
        for spec in qpu_properties["atom_specs"]:
            self.bits_count += spec.getTarget() != -1
    
    def convert_to_atoms(self, state: List[int]):
        if not self._verify(state):
            return {
                "valid": False
            }

        bits = np.full((self.bits_count), np.nan, np.int16)
        for i in range(len(self.qpu_properties["atom_specs"])):
            t = self.qpu_properties["atom_specs"][i].getTarget()
            if t == -1:
                continue
            bits[t] = int(state[i])
        
        return {
            "bits": bits
        }

    def _verify(self, state: List[int]):
        raise NotImplementedError("Not implemented; this is a generic class.")