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

# Source files and executable name
SOURCES = main.cpp brute_force_solver.cpp ../crystals/crystal.cpp ../crystals/crystal_solution.cpp
OBJECTS = $(SOURCES:.cpp=.o)
INCLUDES = -I. -I../crystals/

# Default target
all: $(EXECUTABLE)

# Build the executable from object files
$(EXECUTABLE): $(OBJECTS)
	$(CXX) $(CXXFLAGS) $(INCLUDES) -o $@ $(OBJECTS)

# Compile source files to object files
%.o: %.cpp
	$(CXX) $(CXXFLAGS) $(INCLUDES) -c $< -o $@

# Clean up
clean:
ifeq ($(detected_OS),Windows)
	del /f /q $(subst /,\,$(OBJECTS)) $(subst /,\,$(EXECUTABLE))
else
	rm -f $(OBJECTS) $(EXECUTABLE)
endif

.PHONY: all clean
