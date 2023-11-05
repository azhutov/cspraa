from typing import List, Tuple
import numpy as np


class CrystalStructure:
    def __init__(self, vertices_count: int, species_count: int, dimension: int = 3):
        self.vertices_count = vertices_count
        self.species_count = species_count
        self.dimension = dimension
        self.positions: List[Tuple[float, ...]] = []
        self.potentials: List[List[float]] = [[0.0 for _ in range(species_count)] for _ in range(vertices_count)]
        self.interactions = {}
        self.degrees = {}
        self.neighbours = {}

    def add_position(self, *coords: float) -> None:
        if len(coords) != self.dimension:
            raise ValueError(f"Expected {self.dimension} coordinates, got {len(coords)}")
        if len(self.positions) < self.vertices_count:
            self.positions.append(np.array(coords))

    def set_potential(self, position_idx: int, potentials: List[float]) -> None:
        if 0 <= position_idx < self.vertices_count:
            self.potentials[position_idx] = potentials

    def add_interaction(self, position_idx1: int, position_idx2: int, interactions) -> None:
        if (0 <= position_idx1 < self.vertices_count and 0 <= position_idx2 < self.vertices_count):
            position_idx1, position_idx2 = sorted([position_idx1, position_idx2])
            self.interactions[position_idx1, position_idx2] = interactions
            
            self.degrees[position_idx1] = self.degrees.get(position_idx1, 0) + 1
            self.degrees[position_idx2] = self.degrees.get(position_idx2, 0) + 1

            self.neighbours[position_idx1] = self.neighbours.get(position_idx1,[]) + [position_idx2]
            self.neighbours[position_idx2] = self.neighbours.get(position_idx2,[]) + [position_idx1]

    @staticmethod
    def from_string(encoded_str: str) -> 'CrystalStructure':
        lines = encoded_str.strip().split("\n")
        vertices_count, species_count = map(int, lines[0].split())
        dimension = int(lines[1])
        structure = CrystalStructure(vertices_count, species_count, dimension)

        for line in lines[2:2+vertices_count]:
            coords = list(map(float, line.split()))
            structure.add_position(*coords)

        for idx, line in enumerate(lines[2+vertices_count:2+2*vertices_count]):
            potentials = list(map(float, line.split()))
            structure.set_potential(idx, potentials)

        for line in lines[3+2*vertices_count:]:
            parts = list(map(float, line.split()))
            position_idx1, position_idx2 = int(parts[0]), int(parts[1])
            interactions = parts[2:]
            structure.add_interaction(position_idx1, position_idx2, interactions)

        return structure

    def to_string(self) -> str:
        encoded = []
        encoded.append(f"{self.vertices_count} {self.species_count}")
        encoded.append(str(self.dimension))
        for position in self.positions:
            encoded.append(" ".join(map(str, position)))

        for potentials in self.potentials:
            encoded.append(" ".join(map(str, potentials)))

        encoded.append(str(len(self.interactions)))
        for k, interactions in self.interactions.items():
            position_idx1, position_idx2 = k
            interaction_str = " ".join(map(str, interactions))
            encoded.append(f"{position_idx1} {position_idx2} {interaction_str}")

        return "\n".join(encoded)

    @staticmethod
    def from_file(file_path: str) -> 'CrystalStructure':
        with open(file_path, 'r') as file:
            encoded_str = file.read()
        return CrystalStructure.from_string(encoded_str)

    def to_file(self, file_path: str) -> None:
        with open(file_path, 'w') as file:
            file.write(self.to_string())
