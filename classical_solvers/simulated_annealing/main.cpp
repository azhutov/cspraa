#include <annealing_solver.h>
#include <iostream>
#include <crystal.h>
#include <vector>

using namespace std;

int main() {
    Crystal crystal("../../native_crystal_database/hexagon_three.dat");
    crystal.load();

    int *initial_status = new int[crystal.getN() * crystal.getSpecies()];
    for (int i = 0; i < crystal.getN()*crystal.getSpecies(); i++) {
        initial_status[i] = i % crystal.getSpecies() == 0;
    }
    int repetitions = 100;
    int iterations = 500;

    double (*temperature_function)(double) = [](double t) -> double {
        return 1 - t;
    };
    
    MetropolisSolver metropolis_solver(crystal, temperature_function);
    Solution solution = metropolis_solver.solve_repeat(repetitions, iterations, initial_status);
    
    cout << "energy: " << solution.getEnergy() << endl;
    solution.save("./solutions/output.yaml");
    
    return 0;
}