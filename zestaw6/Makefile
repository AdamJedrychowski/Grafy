CXX := g++
CXXFLAGS := -Wall -std=c++14
SOURCES := $(wildcard *.cpp)
EXECUTABLES := $(SOURCES:.cpp=)

all: $(EXECUTABLES) run plots

$(EXECUTABLES): % : %.cpp
	$(CXX) $(CXXFLAGS) $< -o $@ $(LDLIBS)

run: $(EXECUTABLES)
	./$(EXECUTABLES)

plots:
	gnuplot plot.sh

clean:
	rm -f $(EXECUTABLES)
	rm -f *.png
	rm -f data_cycle.dat
