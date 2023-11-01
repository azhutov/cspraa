# Makefile for a C++ program

# Compiler and compiler flags
CXX = g++
CXXFLAGS = -Wall -O2

# Source file and executable name
SOURCE = main.cpp ../crystal.cpp brute_force_solver.cpp ../linked_list.h ../crystal_solution.cpp
EXECUTABLE = brute_force.exe
DIRECT_IMPORTS = ../linked_list.h

# Object files (automatically generated)
OBJECTS = $(SOURCE:.cpp=.o)

# Default target
all: $(EXECUTABLE)

# Build the executable from object files
$(EXECUTABLE): $(OBJECTS)
	$(CXX) $(CXXFLAGS) -o $@ $^ -I.. -I.

# Compile source files to object files
%.o: %.cpp $(DIRECT_IMPORTS)
	$(CXX) $(CXXFLAGS) -c -o $@ $< -I.. -I.

# Clean up
clean:
	rm -f $(OBJECTS) $(EXECUTABLE)

.PHONY: all clean
