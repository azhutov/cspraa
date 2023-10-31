#include <iostream>
#include <crystal.h>
#include <brute_force_solver.h>
#include <vector>

using namespace std;

int main() {
    Crystal crystal("../../native_crystal_database/hexagon_three.dat");
    crystal.load();
    
    BruteForceSolver solver(crystal);
    Solution s = solver.solve();

    s.save("./solutions/output.yaml");

    return 0;
}