# Makefile for a C++ program

# Compiler and compiler flags
CXX = g++
CXXFLAGS = -Wall -O2

# Source file and executable name
SOURCE = main.cpp brute_force_solver.cpp ../crystals/crystal.cpp ../crystals/linked_list.h ../crystals/crystal_solution.cpp
EXECUTABLE = brute_force.exe
DIRECT_IMPORTS = ../crystals/linked_list.h

# Object files (automatically generated)
OBJECTS = $(SOURCE:.cpp=.o)

# Default target
all: $(EXECUTABLE)

# Build the executable from object files
$(EXECUTABLE): $(OBJECTS)
	$(CXX) $(CXXFLAGS) -o $@ $^ -I. -I../crystals/

# Compile source files to object files
%.o: %.cpp $(DIRECT_IMPORTS)
	$(CXX) $(CXXFLAGS) -c -o $@ $< -I. -I../crystals/

# Clean up
clean:
	rm -f $(OBJECTS) $(EXECUTABLE)

.PHONY: all clean
