import warnings
import re


class CrystalStructure:
    def __init__(self, vertices_count, species_count):
        self.vertices_count = vertices_count
        self.species_count = species_count
        self.positions = []
        self.potentials = [[] for _ in range(vertices_count)]
        self.interactions = {}

    def add_position(self, *args):
        # Single position mode
        if len(args) == 3:
            x, y, z = args
            if len(self.positions) < self.vertices_count:
                self.positions.append((x, y, z))
            else:
                warnings.warn(
                    f"Position limit reached ({self.vertices_count} positions allowed). Position ({x}, {y}, {z}) was not added.")
        # Bulk mode
        elif len(args) == 1 and isinstance(args[0], list):
            for position in args[0]:
                if len(self.positions) < self.vertices_count:
                    self.positions.append(position)
                else:
                    x, y, z = position
                    warnings.warn(
                        f"Position limit reached ({self.vertices_count} positions allowed). Position ({x}, {y}, {z}) and subsequent positions were not added.")
                    break
        else:
            raise ValueError("Invalid arguments for add_position")

    def set_potential(self, *args):
        # Single potential mode
        if len(args) == 2:
            position_idx, potentials = args
            if 0 <= position_idx < self.vertices_count:
                self.potentials[position_idx] = potentials
        # Bulk mode
        elif len(args) == 1 and isinstance(args[0], list):
            for position_idx, potentials in args[0]:
                if 0 <= position_idx < self.vertices_count:
                    self.potentials[position_idx] = potentials
        else:
            raise ValueError("Invalid arguments for set_potential")

    def set_interaction(self, *args):
        # Single interaction mode
        if len(args) == 3:
            position_idx1, position_idx2, interactions = args
            if (0 <= position_idx1 < self.vertices_count and 0 <= position_idx2 < self.vertices_count):
                key = (position_idx1, position_idx2)
                self.interactions[key] = interactions
        # Bulk mode
        elif len(args) == 1 and isinstance(args[0], list):
            for position_idx1, position_idx2, interactions in args[0]:
                if (0 <= position_idx1 < self.vertices_count and 0 <= position_idx2 < self.vertices_count):
                    key = (position_idx1, position_idx2)
                    self.interactions[key] = interactions
        else:
            raise ValueError("Invalid arguments for set_interaction")

    def encode(self):
        encoded = []
        encoded.append(f"{self.vertices_count} {self.species_count}")

        for i, (x, y, z) in enumerate(self.positions):
            encoded.append(f"#{i}: {x}, {y}, {z}")

        for i in range(self.vertices_count):
            potentials = self.potentials[i]
            encoded_potentials = ", ".join([f"({j}, {w:.1f})" for j, w in potentials])
            encoded.append(f"#{i}: {encoded_potentials}")

        for (position_idx1, position_idx2), interactions in self.interactions.items():
            encoded_interactions = ", ".join([f"({i}, {j}, {w:.1f})" for i, j, w in interactions])
            encoded.append(f"#{position_idx1}, #{position_idx2}: {encoded_interactions}")

        return "\n".join(encoded)

    @classmethod
    def decode(cls, encoded_str):
        # Extract vertices_count and species_count
        header_pattern = re.compile(r"^\s*(\d+) (\d+)")
        match = header_pattern.search(encoded_str)
        if not match:
            raise ValueError("Failed to decode header information.")
        vertices_count, species_count = map(int, match.groups())

        structure = cls(vertices_count, species_count)

        # Extract positions
        position_pattern = re.compile(r"#(\d+): (-?\d+\.\d+), (-?\d+\.\d+), (-?\d+\.\d+)")
        for match in position_pattern.finditer(encoded_str):
            x, y, z = map(float, match.groups()[1:])
            structure.add_position(x, y, z)

        # Extract potentials
        potential_pattern = re.compile(r"#(\d+): ((\(\d+, -?\d+\.\d+\),? ?)+)")
        for match in potential_pattern.finditer(encoded_str):
            potentials = [(int(p[0]), float(p[1])) for p in re.findall(r"\((\d+), (-?\d+\.\d+)\)", match.group(2))]
            structure.set_potential(int(match.group(1)), potentials)

        # Extract interactions
        interaction_pattern = re.compile(r"#(\d+), #(\d+): ((\(\d+, \d+, -?\d+\.\d+\),? ?)+)")
        for match in interaction_pattern.finditer(encoded_str):
            interactions = [(int(i[0]), int(i[1]), float(i[2]))
                            for i in re.findall(r"\((\d+), (\d+), (-?\d+\.\d+)\)", match.group(3))]
            structure.set_interaction(int(match.group(1)), int(match.group(2)), interactions)

        return structure

    def write_to_file(self, file_path):
        with open(file_path, 'w') as file:
            file.write(self.encode())

    @classmethod
    def read_from_file(cls, file_path):
        with open(file_path, 'r') as file:
            encoded_str = file.read()
        return cls.decode(encoded_str)