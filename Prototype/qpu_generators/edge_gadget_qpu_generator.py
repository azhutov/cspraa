from Prototype.qpu_generators.generic_qpu_generator import GenericQPUGenerator
from Prototype.qpu_generators.atom_spec import AtomSpec
from Prototype.crystals.crystal_structure import CrystalStructure
import numpy as np

class EdgeGadgetQPUGenerator(GenericQPUGenerator):

    def __init__(self, 
                 weights_detuning_fraction: float,
                 next_nearest_neighbour_detuning_correction: float,
                 crystal: CrystalStructure,
                 atomic_min_distance: float = 1):
        self.next_nearest_neighbour_detuning_correction = next_nearest_neighbour_detuning_correction
        super().__init__(crystal, atomic_min_distance)

        self.weights_detuning_fraction = weights_detuning_fraction /  max(np.abs(np.array(list(crystal.interactions.values()))).max(), np.abs(np.array(crystal.potentials)).max())

        assert self.crystal.species_count == 2, "This generator is only implementable for binary crystals (two atomic species)."
        assert self.crystal.dimension == 2, "This method only works for 2 dimensional crystals"

    def convert(self):
        """Returns a dictionary with the following keys:
            - "atom_specs": A list of atom specs.
            - "rydberg_radius": The desired rydberg radius for the algorithm.
        """
        atom_specs = []
        rydberg_radius = self.atomic_min_distance * np.sqrt(2)

        self._add_positional_qubits(atom_specs)

        vacancy_flag = set({})
        for i, j in self.crystal.interactions.keys():
            self._add_edge_gadget(atom_specs, i, j, vacancy_flag)

        self._normalize_atom_distance_and_detuning(atom_specs)

        return {
            "atom_specs": atom_specs,
            "rydberg_radius": rydberg_radius
        }
    
    def _normalize_atom_distance_and_detuning(self, atom_specs):
        distance_min = min([np.linalg.norm(self.crystal.positions[i]-self.crystal.positions[j]) 
                            for i, j in self.crystal.interactions.keys()]) / (4 + (1+np.sqrt(3))/np.sqrt(2))
        detuning_max = max(atom_specs, key=lambda a : a.getDetuning()).getDetuning()
        for i in range(len(atom_specs)):
            atom_specs[i].setPosition(
                atom_specs[i].getPosition() * self.atomic_min_distance / distance_min
            )
            atom_specs[i].setDetuning(
                atom_specs[i].getDetuning() / detuning_max
            )

    def _add_positional_qubits(self, atom_specs):
        for i in range(self.crystal.vertices_count):
            linear_pot = self.crystal.potentials[i][1] - self.crystal.potentials[i][0]
            for j in self.crystal.neighbours[i]:
                m, M = sorted([i, j])
                linear_pot -= self.crystal.interactions[m, M][0]

            atom_specs += [AtomSpec(
                self.crystal.positions[i],
                detuning = self.crystal.degrees[i] - linear_pot * self.weights_detuning_fraction,
                target=2*i+1
            )]

    def _add_edge_gadget(self, atom_specs, index1, index2, vacancy_flag):
        interactions = np.array(self.interactions[min(index1, index2), max(index1, index2)]) * self.weights_detuning_fraction
        pos = np.array(self.crystal.positions[index1])
        dir = (self.crystal.positions[index2]-self.crystal.positions[index1]) * np.sqrt(2) / (1 + np.sqrt(3) + 4*np.sqrt(2))

        flag1, flag2 = False, False
        if index1 not in vacancy_flag:
            vacancy_flag.add(index1)
            flag1 = True
        if index2 not in vacancy_flag:
            vacancy_flag.add(index2)
            flag2 = True

        pos += dir
        atom_specs += [AtomSpec(pos, 1, 2*index1 if flag1 else -1)]

        pos += dir
        atom_specs += [AtomSpec(pos, 1, -1)]

        dir = self._rotation(15).dot(dir)
        pos += dir
        atom_specs += [AtomSpec(pos, 4, -1)]
        
        dir = self._rotation(120).dot(dir)
        pos += dir
        atom_specs += [AtomSpec(pos, 4, -1)]

        dir = self._rotation(-30).dot(dir)
        pos += dir
        atom_specs += [AtomSpec(pos, 1 - self.next_nearest_neighbour_detuning_correction, -1)]

        dir = self._rotation(-120).dot(dir)
        pos += dir
        atom_specs += [AtomSpec(pos, 4 - (interactions[0]+interactions[3]-interactions[1]-interactions[2]), -1)]

        dir = self._rotation(30).dot(dir)
        pos += dir
        atom_specs += [AtomSpec(pos, 1 - self.next_nearest_neighbour_detuning_correction, -1)]
        
        dir = self._rotation(-120).dot(dir)
        pos += dir
        atom_specs += [AtomSpec(pos, 4, -1)]

        dir = self._rotation(30).dot(dir)
        pos += dir
        atom_specs += [AtomSpec(pos, 1, -1)]

        dir = self._rotation(75).dot(dir)
        pos += dir
        atom_specs += [AtomSpec(pos, 1, 2*index2 if flag2 else -1)]

    def _rotation(self, degrees):
        angle = degrees / 180 * np.pi
        return np.array([[np.cos(angle),-np.sin(angle)], [np.sin(angle), np.cos(angle)]])