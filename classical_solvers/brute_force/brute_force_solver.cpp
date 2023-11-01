#include <brute_force_solver.h>
#include <iostream>

using namespace std;

BruteForceSolver::BruteForceSolver(Crystal &crystal) : cr(crystal) {
    this->n = crystal.getN();
    this->species = crystal.getSpecies();
    this->qmat = crystal.getQUBOMatrix();
    this->status = new int[n*species];

    for (int i = 0; i < n*species; i++) {
        this->status[i] = i % species == 0;
    }
}

Solution BruteForceSolver::solve() {
    double min_energy = this->cr.getEnergy(this->status);
    static int* best_status = new int[n*species];
    for (int i = 0; i < n*species; i++) {
        best_status[i] = this->status[i];
    }

    double e;
    while (this->nextStatus()) {
        e = this->cr.getEnergy(this->status);
        if (e < min_energy) {
            min_energy = e;
            for (int i = 0; i < n*species; i++) {
                best_status[i] = this->status[i];
            }
        }
    }

    return Solution(this->cr, min_energy, best_status);
}

bool BruteForceSolver::nextStatus() {
    int index = -1, k = -1;
    do {
        index++;
        for (int i = 0; i < this->species; i++) { 
            if (this->status[index*this->species + i]) {
                k = i;
                break;
            }
        }
        status[index*this->species + k] = 0;
        status[index*this->species + (k+1) % species] = 1;
        std::cout << index << std::endl;
    } while (this->status[index*species] && index < n - 1);

    return index < this->n;
}