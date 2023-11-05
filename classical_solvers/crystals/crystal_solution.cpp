#include <crystal_solution.h>
#include <fstream>

Solution::Solution(Crystal &cr, double energy, int *solution) : crystal(cr) {
    this->n = cr.getN();
    this->species = cr.getSpecies();
    this->energy = energy;
    this->solution = solution;
}

int Solution::getN() const {
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

void Solution::save(std::string name) const {
    std::string address = name;
    std::ofstream file(address);

    file << "crystal: " << crystal.getCrystalName() << std::endl;
    file << "energy: " << this->energy << std::endl;

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