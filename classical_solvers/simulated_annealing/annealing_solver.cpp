#include <iostream>
#include <annealing_solver.h>
#include <fstream>
#include <cstring>
#include <random>
#include <cmath>

using namespace std;

MetropolisSolver::MetropolisSolver(Crystal &cr,
                                   double (*temperature_function)(double)) : crystal(cr) {
    this->temperature_function = temperature_function;   
}

Solution MetropolisSolver::solve_repeat(int repetitions, int iterations, int *initial_status) {
    Solution *best_solution = nullptr;

    for (int i = 0; i < repetitions; i++) {
        Solution solution = this->solve(iterations, initial_status);
        if (best_solution == nullptr || best_solution->getEnergy() > solution.getEnergy()) {
            best_solution = new Solution(crystal, solution.getEnergy(), solution.getSolution());
        }
    }

    return *best_solution;
}

Solution MetropolisSolver::solve(int iterations, int *initial_status) {
    int *status = new int[crystal.getN() * crystal.getSpecies()];
    double t, energy;
    
    for (int i = 0; i < crystal.getN() * crystal.getSpecies(); i++) { 
        status[i] = initial_status[i];
    }
    energy = crystal.getEnergy(status);
    for (int i = 0; i < iterations; i++) {
        t = i / (iterations - 1);
        step(t, status, energy);
    }

    return Solution(crystal, energy, status);
}

bool MetropolisSolver::step(double t, int *status, double &energy) {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<int> vertex_random_generator(0, crystal.getN()-1);
    std::uniform_int_distribution<int> species_random_generator(1, crystal.getSpecies()-1);

    int vertex = vertex_random_generator(gen);
    int current_species;
    for (int i = 0; i < crystal.getSpecies(); i++) {
        if (status[vertex*crystal.getSpecies()+i]) {
            current_species = i;
            break;
        }
    }
    int new_species = (species_random_generator(gen) + current_species) % crystal.getSpecies();

    double current_energy = crystal.getLocalEnergy(vertex, status);
    status[vertex*crystal.getSpecies()+current_species] = 0;
    status[vertex*crystal.getSpecies()+new_species] = 1;
    double new_energy = crystal.getLocalEnergy(vertex, status);

    bool change = true;
    if (new_energy > current_energy) {
        std::uniform_real_distribution<double> movement_random_generator(0.0, 1.0);
        double a = movement_random_generator(gen);
        double temperature = temperature_function(t);
        if (temperature <= 0 || a > exp(-(new_energy - current_energy) / temperature)) {
            change = false;
            status[vertex*crystal.getSpecies()+current_species] = 1;
            status[vertex*crystal.getSpecies()+new_species] = 0;
        }
    }
    
    energy += change * (new_energy - current_energy);
    return change;
}