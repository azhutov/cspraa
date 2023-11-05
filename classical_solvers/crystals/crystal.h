#pragma once
#include <string>
#include <vector>
#include <unordered_map>
#include <linked_list.h>

class Crystal {
public:
    Crystal(std::string address);

    void load();

    std::vector<std::vector<double> > getQUBOMatrix();
    int getN();
    int getSpecies();
    int getDimension();
    double getEnergy(int *status);
    double getLocalEnergy(int index, int *status);
    std::string getCrystalName();
private:
    void sortVertexLinkedList(LinkedList<int> &ll);
    std::vector<std::vector<double> > qmat;
    int n, species, dimension;
    std::string address;
    std::unordered_map<int, LinkedList<int> > vertices_map;
};