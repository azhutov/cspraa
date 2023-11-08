from Prototype.qpu_generators import *
from Prototype.crystals.crystal_structure import CrystalStructure
import numpy as np
from Prototype.simulation.machine_generator import MachineGenerator
from pulser import Pulse, Register, Sequence
from pulser.register.register_layout import RegisterLayout
from pulser.devices import Chadoq2
from typing import Union
import yaml
import os
from pulser.waveforms import *

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
    
    def _add_adiabatic_pulse_with_local_channels(self, 
                                                 seq: Sequence, 
                                                 qpu_properties: dict):
        time = self.configs["time"]
        omega_max = self.omega_max
        detuning_min = self.configs["adiabatic_waveform"]["detunings"]["detuning_min"]
        detuning_base = self.configs["adiabatic_waveform"]["detunings"]["detuning_base"]
        detuning_max = self.configs["adiabatic_waveform"]["detunings"]["detuning_max"]
        atom_detunings = [atom.getDetuning() for atom in qpu_properties["atom_specs"]]

        amp_waveform = InterpolatedWaveform(
            duration = time,
            values = [0, omega_max, 0]
        )
        for i in range(len(atom_detunings)):
            di = detuning_base + atom_detunings[i] * (detuning_max-detuning_base)
            detuning_waveform = InterpolatedWaveform(
                time,
                [-di, 0, di]
            )
            pulse = Pulse(
                amp_waveform,
                detuning_waveform,
                phase = 0
            )
            seq.declare_channel(f"my_dmm_{i}","rydberg_local", initial_target=f"q{i}")
            seq.add(pulse, f"my_dmm_{i}", protocol="no-delay")

    def _calculate_omega_max(self, qpu_properties: dict, machine: Chadoq2):
        radius = qpu_properties["rydberg_radius"] * self.configs["rydberg_correction_factor"]
        return machine.interaction_coeff / radius**6
    
    def _generate_back_converter(self, qpu_propertiesL: dict):
        return globals()[self.configs["qpu_generator"]["back_converter"]](
            qpu_propertiesL
        )

    def create_sequence(self):
        qpu_properties = self._generate_qpu_properties()
        back_converter = self._generate_back_converter(qpu_properties)
        
        machine = MachineGenerator.getMachine(self.configs["machine"])
        self.omega_max = self._calculate_omega_max(qpu_properties, machine)

        register = self._create_register(qpu_properties)
        # detunings_map = self._create_detunings_map(qpu_properties)

        seq = Sequence(register, machine)
        self._add_adiabatic_pulse_with_local_channels(
            seq, qpu_properties
        )

        return seq, back_converter




