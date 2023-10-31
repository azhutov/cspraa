#include <iostream>
#include <crystal.h>
#include <fstream>
#include <stdexcept>
#include <vector>
#include <filesystem>

using namespace std;

Crystal::Crystal(std::string address) {
    this->address = address; 
}

void Crystal::load() {
    std::ifstream inputFile(address);
    if (!inputFile.is_open()) {
        throw std::runtime_error("Could not open the file " + address);
    }

    int n, species;
    inputFile >> n >> species;
    static std::vector<std::vector<double>> qmat(n*species, std::vector<double>(n*species));

    int dimension; // This value is ignored, as it has no role in the QUBO problem.
    inputFile >> dimension;
    
    // Skipping n lines in the file; coordinates are not part of the QUBO matrix.
    for (int i = 0; i < n+1; i++) {
        std::string line;
        std::getline(inputFile, line);
    }

    int vertices_count;
    inputFile >> vertices_count;
    
    double v1, v2, w;
    for (int i = 0; i < vertices_count; i++) {
        inputFile >> v1 >> v2;
        for (int j = 0; j < species; j++) {
            for (int k = 0; k < species; k++) {
                inputFile >> w;
                qmat[v1*species+j][v2*species+k] = w/2;
                qmat[v2*species+k][v1*species+j] = w/2;
            }
        }
    }

    inputFile.close();

    this->qmat = qmat;
    this->n = n;
    this->species = species;
    this->dimension = dimension;
}

double Crystal::getEnergy(int *status) {
    double output = 0;
    for (int i = 0; i < this->n*this->species; i++) {
        for (int j = 0; j < this->n*this->species; j++) {
            output += this->qmat[i][j] * status[i] * status[j];
        }
    }
    return output;
}

std::vector<std::vector<double>> Crystal::getQUBOMatrix() {
    return this->qmat;
}

int Crystal::getN() {
    return this->n;
}

int Crystal::getSpecies() {
    return this->species;
}

int Crystal::getDimension() {
    return this->dimension;
}

std::string Crystal::getCrystalName() {
    std::filesystem::path file_path = this->address;
    return file_path.filename().stem().string();
}