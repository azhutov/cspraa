#include "annealing_solver.h"
#include <iostream>
#include <fstream>
#include <sstream>
#include <memory>
#include <crystal.h>
#include <vector>
#include <filesystem>
#include <chrono>

namespace fs = std::filesystem;

void saveSolution(Solution& solution, const std::string& outputFilePath) {
    solution.save(outputFilePath, true);
    std::cout << "Solution saved to " << outputFilePath << std::endl;
}

void appendBenchmarkData(const std::string& benchmarkFilePath, Crystal& crystal, long long duration, const std::string& inputFilePath) {
    std::ofstream benchmarkFile;
    bool fileExists = fs::exists(benchmarkFilePath);

    benchmarkFile.open(benchmarkFilePath, std::ios_base::app); // Open in append mode

    if (!fileExists) {
        benchmarkFile << "solver,problem_size,runtime,input_file\n";
    }

    benchmarkFile << "\"simulated_annealing\"," << crystal.getN() << "," << duration << ",\"" << inputFilePath << "\"\n";
    benchmarkFile.close();
}

double linearTemperatureFunction(double t) {
    return 0.05 - t;
}


int main(int argc, char** argv) {
    if (argc < 6) {
        std::cerr << "Usage: " << argv[0] << " <crystal_structure_file> <solutions_directory> <benchmark_file_path> <repetitions> <iterations>" << std::endl;
        return 1;
    }

    try {
        std::string inputFilePath = argv[1];
        std::string solutionsDirectory = argv[2];
        std::string benchmarkFilePath = argv[3];
        int repetitions = std::stoi(argv[4]);
        int iterations = std::stoi(argv[5]);

        Crystal crystal(inputFilePath);
        crystal.load();

        std::unique_ptr<int[]> initial_status(new int[crystal.getN() * crystal.getSpecies()]);
        for (int i = 0; i < crystal.getN() * crystal.getSpecies(); i++) {
            initial_status[i] = i % crystal.getSpecies() == 0;
        }

        auto start = std::chrono::high_resolution_clock::now();

        MetropolisSolver metropolis_solver(crystal, linearTemperatureFunction);
        Solution solution = metropolis_solver.solve_repeat(repetitions, iterations, initial_status.get());
        
        auto stop = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(stop - start).count();

        std::cout << "Energy: " << solution.getEnergy() << std::endl;

        fs::path outputPath(argv[2]);
        fs::create_directories(outputPath);
        std::string outputFileName = fs::path(inputFilePath).stem().string() + "_solution.yaml";
        std::string outputFilePath = outputPath / outputFileName;

        saveSolution(solution, outputFilePath);
        std::cout << "Time taken by function: " << duration << " milliseconds" << std::endl;

        appendBenchmarkData(benchmarkFilePath, crystal, duration, inputFilePath);
    } catch (const std::exception& e) {
        std::cerr << "An error occurred: " << e.what() << std::endl;
        return 1;
    }

    return 0;
}