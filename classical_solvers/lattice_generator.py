import os
import numpy as np
from math import sqrt
from Prototype.crystal_structure import CrystalStructure


class LatticeGenerator:
    def __init__(self, base_directory, species_count, dimension):
        self.base_directory = base_directory
        self.species_count = species_count
        self.dimension = dimension

    def generate_lattice(self, nx, ny):
        raise NotImplementedError("Subclasses should implement this method")

    def generate_filename(self, nx, ny, vertices_count):
        raise NotImplementedError("Subclasses should implement this method")

    def save_structure(self, nx, ny):
        positions, interactions = self.generate_lattice(nx, ny)
        vertices_count = len(positions)
        crystal = CrystalStructure(vertices_count, self.species_count, self.dimension)

        for position in positions:
            crystal.add_position(*position)

        for interaction_pair, interaction_value in interactions.items():
            crystal.add_interaction(*interaction_pair, interaction_value)

        filename = self.generate_filename(nx, ny, vertices_count)
        filepath = os.path.join(self.base_directory, filename)
        crystal.to_file(filepath)


class GrapheneLatticeGenerator(LatticeGenerator):
    def generate_lattice(self, nx, ny):
        positions = self.generate_positions(nx, ny)
        interactions = self.find_bonded_interactions(positions, bond_length=1.01, interaction_energy=[0, 0, 0, -0.1])
        return positions, interactions

    def generate_positions(self, nx, ny):
        PRECISION = 5
        b1 = np.array([1, 0])
        b2 = np.array([0.5, sqrt(3)/2])
        positions = set()

        for i in range(nx):
            for j in range(ny):
                pos = (i * b1 + j * b2) * sqrt(3)
                for k in range(6):
                    angle = 2 * np.pi * k / 6
                    offset = np.array([np.sin(angle), np.cos(angle)])
                    vertex = tuple(np.around(pos + offset, decimals=PRECISION))
                    positions.add(vertex)
        return list(positions)

    def find_bonded_interactions(self, positions, bond_length, interaction_energy):
        new_interactions = {}
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                if self.calculate_distance(positions[i], positions[j]) <= bond_length:
                    new_interactions[(i, j)] = interaction_energy
        return new_interactions

    @staticmethod
    def calculate_distance(pos1, pos2):
        return sqrt(sum((p1 - p2) ** 2 for p1, p2 in zip(pos1, pos2)))

    def generate_filename(self, nx, ny, vertices_count):
        return f'graphene_supercell_nx_{nx}_ny_{ny}.dat'
