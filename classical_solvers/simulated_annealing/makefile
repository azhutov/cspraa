# Detect the operating system
ifeq ($(OS),Windows_NT)
    detected_OS := Windows
else
    detected_OS := $(shell uname -s)
endif

# Compiler and compiler flags
CXX = g++
CXXFLAGS = -Wall -O2
ifeq ($(detected_OS),Windows)
    CXXFLAGS += -std=c++17
    EXECUTABLE = brute_force.exe
else ifeq ($(detected_OS),Darwin)  # Darwin is the system name for macOS
    CXXFLAGS += -std=c++17
    EXECUTABLE = brute_force
endif

# Source file and executable name
SOURCES = main.cpp annealing_solver.cpp ../crystals/crystal.cpp ../crystals/crystal_solution.cpp
DIRECT_IMPORTS = ../crystals/linked_list.h

# Object files (automatically generated)
OBJECTS = $(SOURCES:.cpp=.o)

# Include directories
INCLUDES = -I. -I../crystals/

# Executable name based on detected OS
ifeq ($(detected_OS),Windows)
    EXECUTABLE = annealing.exe
else
    EXECUTABLE = annealing
endif

# Default target
all: $(EXECUTABLE)

# Build the executable from object files
$(EXECUTABLE): $(OBJECTS)
	$(CXX) $(CXXFLAGS) $(INCLUDES) -o $@ $(OBJECTS)

# Compile source files to object files
%.o: %.cpp $(DIRECT_IMPORTS)
	$(CXX) $(CXXFLAGS) $(INCLUDES) -c $< -o $@

# Clean up
clean:
ifeq ($(detected_OS),Windows)
	del /f /q $(subst /,\,$(OBJECTS)) $(subst /,\,$(EXECUTABLE))
else
	rm -f $(OBJECTS) $(EXECUTABLE)
endif

.PHONY: all clean
