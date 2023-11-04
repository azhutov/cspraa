#include <iostream>
#include <crystal.h>
#include <fstream>
#include <stdexcept>
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
    static std::vector<std::vector<double> > qmat(n*species, std::vector<double>(n*species));

    int dimension; // This value is ignored, as it has no role in the QUBO problem.
    inputFile >> dimension;
    
    // Skipping n lines in the file; coordinates are not part of the QUBO matrix.
    for (int i = 0; i < n+1; i++) {
        std::string line;
        std::getline(inputFile, line);
    }

    double w;
    for (int i = 0; i < n * species; i++) {
        inputFile >> w;
        qmat[i][i] = w;
    }

    int vertices_count;
    inputFile >> vertices_count;
    
    double v1, v2;
    for (int i = 0; i < vertices_count; i++) {
        inputFile >> v1 >> v2;
        
        if (vertices_map.find(v1) == vertices_map.end()) {
            vertices_map[v1] = LinkedList<int>();
        }
        vertices_map[v1].put(v2);

        if (vertices_map.find(v2) == vertices_map.end()) {
            vertices_map[v2] = LinkedList<int>();
        }
        vertices_map[v2].put(v1);

        for (int j = 0; j < species; j++) {
            for (int k = 0; k < species; k++) {
                inputFile >> w;
                qmat[v1*species+j][v2*species+k] += w / 2;
                qmat[v2*species+k][v1*species+j] += w / 2;
            }
        }
    }

    for (int i = 0; i < n; i++) {
        if (vertices_map.find(i) == vertices_map.end()) {
            continue;
        }
        sortVertexLinkedList(vertices_map[i]);
    }

    inputFile.close();

    this->qmat = qmat;
    this->n = n;
    this->species = species;
    this->dimension = dimension;
}

double Crystal::getLocalEnergy(int index, int *status) {
    double output = 0;

    for (int i = 0; i < species; i++) {
        output += qmat[index*species+i][index*species+i] * status[index*species+i];
    }
    if (vertices_map.find(index) == vertices_map.end()) {
        return output;
    }
    Node<int> *node = vertices_map[index].getStartNode();
    while (node != nullptr) {
        int j = node->value;
        for (int r1 = 0; r1 < species; r1++) {
            for (int r2 = 0; r2 < species; r2++) {
                output += qmat[index*species+r1][j*species+r2]*status[index*species+r1]*status[j*species+r2];
                output += qmat[j*species+r2][index*species+r1]*status[index*species+r1]*status[j*species+r2];
            }
        }
        node = node->next;
    }

    return output;
}

double Crystal::getEnergy(int *status) {
    double output = 0;

    // Linear terms
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < species; j++) {
            if (status[i*species+j]) {
                output += qmat[i*species+j][i*species+j];
                break;
            }
        }
    }

    // Second order terms
    for (int i = 0; i < n; i++) {
        int j;
        if (vertices_map.find(i) == vertices_map.end()) {
            continue;
        }
        Node<int>* n = vertices_map[i].getStartNode();
        while (n != nullptr) {
            j = n->value;
            if (j > i) {
                break;
            }
            n = n->next;

            for (int r1 = 0; r1 < species; r1++) {
                for (int r2 = 0; r2 < species; r2++) {
                    output += qmat[i*species+r1][j*species+r2]*status[i*species+r1]*status[j*species+r2];
                    output += qmat[j*species+r2][i*species+r1]*status[i*species+r1]*status[j*species+r2];
                }
            }
        }
    }

    return output;
}

void Crystal::sortVertexLinkedList(LinkedList<int> &ll) {
    bool flag;
    do {
        flag = false;
        Node<int>* n = ll.getStartNode(), * next, * previous;
        for (int i = 0; i < ll.getSize()-1; i++) {
            if (n->value <= n->next->value) {
                continue;
            }
            flag = true;
            next = n->next;
            previous = n->previous;

            n->next = n->next->next;
            n->previous = n;

            next->next = n;
            next->previous = previous;
            
            n = next;
            if (i == 0) {
                ll.setStartNode(next);
            }
        }
    } while (flag);
}

std::vector<std::vector<double> > Crystal::getQUBOMatrix() {
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