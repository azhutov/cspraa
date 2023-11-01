#include <crystal.h>
#include <string>

class Solution {
public:
    Solution(Crystal &cr, double energy, int *solution);

    int getN();
    int getSpecies();
    double getEnergy();
    int* getSolution();
    Crystal getCrystal();

    void save(std::string name);
private:
    Crystal crystal;
    int n;
    int species;
    double energy;
    int *solution;
};