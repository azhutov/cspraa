#include <crystal_solution.h>
#include <fstream>

Solution::Solution(Crystal &cr, double energy, int *solution) : crystal(cr) {
    this->n = cr.getN();
    this->species = cr.getSpecies();
    this->energy = energy;
    this->solution = solution;
}

int Solution::getN() {
    return this->n;
}

int Solution::getSpecies() {
    return this->species;
}

double Solution::getEnergy() {
    return this->energy;
}

int* Solution::getSolution() {
    return this->solution;
}

Crystal Solution::getCrystal() {
    return crystal;
}

void Solution::save(std::string name, bool save_ground_state) {
    std::string address = name;
    std::ofstream file(address);

    file << "crystal: " << crystal.getCrystalName() << std::endl;
    file << "energy: " << this->energy << std::endl;
    if (save_ground_state) { // assuming ground state is all 1's
        int *ground_state = new int[crystal.getN() * crystal.getSpecies()];
        for (int i = 0; i < crystal.getN() * crystal.getSpecies(); i++) {
            ground_state[i] = i % crystal.getSpecies() == 1;
        }
        file << "ground_state_energy: " << crystal.getEnergy(ground_state) << std::endl;
    }
    file << "atoms:" << std::endl;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < species; j++) {
            if (solution[i*species+j]) {
                file << " - " << j << std::endl;
                break;
            }
        }
    }
}