from Prototype.GenericQPUGenerator import GenericQPUGenerator, AtomSpec
from Prototype.crystal_structure import CrystalStructure
import numpy as np

class ArbitraryConnectivityQPUGenerator(GenericQPUGenerator):

    def __init__(self, 
                 weights_detuning_fraction: float,
                 copy_gadget_detuning_correction: float,
                 next_nearest_neighbour_detuning_correction: float,
                 two_species_penalty: float,
                 no_species_penalty: float,
                 crystal: CrystalStructure,
                 atomic_min_distance: float = 1):
        self.weights_detuning_fraction = weights_detuning_fraction
        self.copy_gadget_detuning_correction = copy_gadget_detuning_correction
        self.next_nearest_neighbour_detuning_correction = next_nearest_neighbour_detuning_correction
        self.two_species_penalty = two_species_penalty
        self.no_species_penalty = no_species_penalty
        super().__init__(crystal, atomic_min_distance)

        self.n = self.crystal.species_count * self.crystal.vertices_count

    def convert(self):
        """Returns a dictionary with the following keys:
            - "atom_specs": A list of atom specs.
            - "rydberg_radius": The desired rydberg radius for the algorithm.
        """
        atom_specs = []
        rydberg_radius = self.atomic_min_distance * np.sqrt(5) / 4

        for i in range(self.n):
            self._add_target_line(atom_specs, i)
        for i in range(self.n-1):
            for j in range(i+1, self.n):
                self._add_crossing_gadget(atom_specs, i, j)

        self._normalize_atom_distance_and_detuning(atom_specs)

        return {
            "atom_specs": atom_specs,
            "rydberg_radius": rydberg_radius
        }
    
    def _normalize_atom_distance_and_detuning(self, atom_specs):
        detuning_max = max(atom_specs, key=lambda a : a.getDetuning()).getDetuning()
        for i in range(len(atom_specs)):
            atom_specs[i].setPosition(
                atom_specs[i].getPosition() * self.atomic_min_distance
            )
            atom_specs[i].setDetuning(
                atom_specs[i].getDetuning() / detuning_max
            )
    
    def _add_crossing_gadget(self, atom_specs, i, j):
        i, j = sorted([i, j])
        center = self._get_crossing_gadget_center(i, j)

        if i // self.crystal.species_count == j // self.crystal.species_count:
            pot = -self.two_species_penalty - 2*self.no_species_penalty
        else:
            key = i // self.crystal.species_count, j // self.crystal.species_count

            if key not in self.interactions.keys():
                pot = 0
            else:
                pot = self.interactions[
                    key
                ][
                    (i % self.crystal.species_count) * self.crystal.species_count + j % self.crystal.species_count
                ]
        for d1 in range(2):
            for d2 in range(2):
                position = center + np.array([
                    d1-1/2,
                    d2-1/2,
                ])
                is_control = (j%2 == d1) and (i%2 == d2)

                atom_specs += [
                    AtomSpec(
                        position = position,
                        detuning = 4 + pot * is_control,
                        target = -1
                    )
                ]

    def _get_crossing_gadget_center(self, i: int, j: int):
        assert i != j, "No crossing gadget between a qubit and itself"
        return np.array([
            3*j - 3/2,
            -3*i
        ])
                
    def _add_target_line(self, atom_specs, index):
        vertex_index = index // self.crystal.species_count
        species_index = index % self.crystal.species_count

        start = self._get_target_line_start(index)
        end = self._get_target_line_end(index)
        
        current = np.array(start)
        while True:
            if current[0] == end[0] or current[1] == end[1] or current[1] > end[1] + 3/2:
                is_start = (current == start).all()
                atom_specs += [AtomSpec(
                    position = np.array(current),
                    detuning = 1 - self.weights_detuning_fraction*self.potentials[vertex_index][species_index]*is_start - self.no_species_penalty*is_start,
                    target = index if is_start else -1
                )]
                if (current == end).all():
                    break
                current += np.array([3,0]) if current[1]==end[1] else np.array([0,-3])
            elif current[1] == end[1] + 3/2:
                atom_specs += [AtomSpec(
                    position = np.array(current),
                    detuning = 1 + self.copy_gadget_detuning_correction + self.next_nearest_neighbour_detuning_correction,
                    target = -1
                )]
                current += np.array([3/4,-3/4])
            elif current[1] == end[1] + 3/4:
                atom_specs += [AtomSpec(
                    position = np.array(current),
                    detuning = 1 + self.copy_gadget_detuning_correction,
                    target = -1
                )]
                current += np.array([3/4,-3/4])
            elif current[1] < end[1]:
                raise Exception("Unexpected behavior. This is a logical error.")
            else:
                raise Exception("Unexpected behavior. This is a logical error.")

        if self.n % 2: # To make 0/1 balanced when n is odd
            atom_specs += [AtomSpec(
                position = end+np.array([1,0]),
                detuning = 1,
                target = -1
                )]
                
    def _get_target_line_start(self, index):
        return np.array([(3/2+3*(index-1))*(index>0), 3/2*(index>0)])

    def _get_target_line_end(self, index):
        return np.array([3*(self.n-1)-3/2*(index==self.n-1), -3*index+3/2*(index==self.n-1)])