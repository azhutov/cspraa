from Prototype.qpu_generators import *
from Prototype.crystals.crystal_structure import CrystalStructure
import matplotlib.pyplot as plt
import numpy as np
from Prototype.simulation.machine_generator import MachineGenerator
from pulser import Pulse, Register, Sequence
from pulser.register.register_layout import RegisterLayout
from enum import Enum
from typing import Union
import yaml
import os

class SequenceBuilder:

    def __init__(self,
                 crystal: CrystalStructure,
                 configs: Union[str, dict] = "default"):
        self.crystal = crystal
        
        self.update_configs(configs, True)

    def update_configs(self, configs: Union[str, dict], override: bool = False):
        if type(configs) == str:
            configs = yaml.safe_load(
                open(os.path.join(
                    os.path.dirname(__file__),
                    "configs",
                    f"{configs}.yml"
                ))
            )
        elif type(configs) != dict:
            raise Exception(f"Unexpected type error for configs: {type(configs)}")
        
        if override:
            self.configs = configs
        else:
            self.configs = {**self.configs, **configs}
        
    def _generate_qpu_properties(self):
        qpu_generation_configs = self.configs["qpu_generator"]
        qpu_generator: GenericQPUGenerator = globals()[qpu_generation_configs["type"]](
            crystal = self.crystal,
            **qpu_generation_configs["args"]
        )
        return qpu_generator.convert()
        
    def _create_register(self, qpu_properties: dict):
        coords = np.array([atomSpec.getPosition() for atomSpec in qpu_properties["atom_specs"]])
        
        return Register.from_coordinates(
            coords,
            center = True,
            prefix = "q"
        )

    def _create_detunings_map(self, qpu_properties: dict):
        coords = np.array([atomSpec.getPosition() for atomSpec in qpu_properties["atom_specs"]])
        detunings = np.array([atomSpec.getDetuning() for atomSpec in qpu_properties["atom_specs"]])
        detunings_normalized = detunings / detunings.sum()
        
        register_layout = RegisterLayout(coords)
        return register_layout.define_detuning_map({
            i: detunings_normalized[i] for i in range(len(coords))
        })
    
    def _add_adiabatic_pulse(self, seq: Sequence, qpu_properties: dict):
        pass

    def _add_detunings(self, seq: Sequence, detunings_map: dict):
        pass
    
    def create_sequence(self):
        machine = MachineGenerator.getMachine(self.configs["machine"])
        qpu_properties = self._generate_qpu_properties()
        register = self._create_register(qpu_properties)
        detunings_map = self._create_detunings_map(qpu_properties)

        seq = Sequence(register, machine)
        self._add_adiabatic_pulse(seq, qpu_properties)
        self._add_detunings(seq, detunings_map)

        return seq




