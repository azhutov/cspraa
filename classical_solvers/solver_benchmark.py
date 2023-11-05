import os
import subprocess
from tqdm import tqdm
from lattice_generator import GrapheneLatticeGenerator

class SolverBenchmark:
    def __init__(self, name, executable, nx_list, ny_list, crystals_directory, repetitions=None, iterations=None, traversal_method='nested'):
        self.name = name
        self.executable = executable
        self.nx_list = nx_list
        self.ny_list = ny_list
        self.crystals_directory = crystals_directory
        self.repetitions = repetitions
        self.iterations = iterations
        self.traversal_method = traversal_method

    def generate_problems(self):
        os.makedirs(self.crystals_directory, exist_ok=True)
        graphene_generator = GrapheneLatticeGenerator(self.crystals_directory, species_count=2, dimension=2)

        if self.traversal_method == 'nested':
            for nx in self.nx_list:
                for ny in self.ny_list:
                    graphene_generator.save_structure(nx, ny)
        elif self.traversal_method == 'zip':
            for nx, ny in zip(self.nx_list, self.ny_list):
                graphene_generator.save_structure(nx, ny)
        else:
            raise ValueError("Invalid traversal method. Supported methods are 'nested' and 'zip'.")

    def run(self, nx, ny):
        crystal_file = f'{self.crystals_directory}/graphene_supercell_nx_{nx}_ny_{ny}.dat'
        cmd = [self.executable, crystal_file]

        if self.repetitions is not None and self.iterations is not None:
            cmd.extend([str(self.repetitions), str(self.iterations)])

        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode != 0:
            print(f"Error running {self.name}: {result.stderr}")
            return None

        return None
    
    @staticmethod
    def extract_time_from_output(output):
        lines = output.split('\n')
        for line in lines:
            if "Time taken by function:" in line:
                return int(line.split()[-2])  # Assuming the time is always in milliseconds
        return None  # If the time is not found, return None