#include <vector>
#include <crystal_solution.h>
#include <crystal.h>

class BruteForceSolver {
public:
    BruteForceSolver(Crystal &crystal);

    Solution solve();
private:
    Crystal cr;
    int n;
    int species;
    std::vector<std::vector<double> > qmat;
    int *status;

    bool nextStatus();
};