#include <crystal.h>
#include <crystal_solution.h>
#include <string>

class MetropolisSolver {
public:
    MetropolisSolver(Crystal &cr,
                    double (*temperature_function)(double));
    Solution solve(int iterations, int *initial_status);
    Solution solve_repeat(int repetitions, int iterations, int *initial_status);
private:
    Crystal crystal;
    double (*temperature_function)(double);
    bool step(double t, int *status, double &energy);
};