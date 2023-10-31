#pragma once
#include <string>
#include <vector>

class Crystal {
public:
    Crystal(std::string address);

    void load();

    std::vector<std::vector<double>> getQUBOMatrix();
    int getN();
    int getSpecies();
    int getDimension();
    double getEnergy(int *status);
    std::string getCrystalName();
private:
    std::vector<std::vector<double>> qmat;
    int n, species, dimension;
    std::string address;
};