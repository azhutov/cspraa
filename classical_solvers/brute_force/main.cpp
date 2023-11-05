#include "brute_force_solver.h"
#include <iostream>
#include <fstream>
#include <sstream>
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

    benchmarkFile << "\"brute_force\"," << crystal.getN() << "," << duration << ",\"" << inputFilePath << "\"\n";
    benchmarkFile.close();
}   

int main(int argc, char** argv) {
    if (argc < 4) {
        std::cerr << "Usage: " << argv[0] << " <crystal_structure_file> <solutions_directory> <benchmark_file_name>" << std::endl;
        return 1;
    }

    try {
        std::string inputFilePath = argv[1];
        std::string benchmarkFilePath = argv[3];
        Crystal crystal(inputFilePath);
        crystal.load();

        auto start = std::chrono::high_resolution_clock::now();

        BruteForceSolver solver(crystal);
        Solution s = solver.solve();

        auto stop = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(stop - start).count();

        fs::path outputPath(argv[2]);
        fs::create_directories(outputPath);
        std::string outputFileName = fs::path(inputFilePath).stem().string() + "_solution.yaml";
        std::string outputFilePath = outputPath / outputFileName;

        saveSolution(s, outputFilePath);
        std::cout << "Time taken by function: " << duration << " milliseconds" << std::endl;

        appendBenchmarkData(benchmarkFilePath, crystal, duration, inputFilePath);
    } catch (const std::exception& e) {
        std::cerr << "An error occurred: " << e.what() << std::endl;
        return 1;
    }

    return 0;
}
