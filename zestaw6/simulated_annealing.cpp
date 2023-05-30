#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>
#include <ctime>
#include <cstdlib>
#include <algorithm>

#define MAX_IT 10000

struct Vertex{
    int x;
    int y;
};

double distance(Vertex& v_1, Vertex& v_2){
    return sqrt(pow(v_1.x - v_2.x, 2) + pow(v_1.y - v_2.y, 2));
}

double cycle_length(std::vector<Vertex>& vertices,  std::vector<int>& cycle){
    double length = 0.;
    int n = vertices.size();
    for (int i = 0; i < n - 1; i++) {
        length += distance(vertices[cycle[i]], vertices[cycle[i + 1]]);
    }
    length += distance(vertices[cycle[n - 1]], vertices[cycle[0]]);
    return length;
}

void opt(std::vector<int>& cycle, int i, int j) {
    while (i < j) {
        std::swap(cycle[i], cycle[j]);
        i++;
        j--;
    }
}

std::vector<int> algorithm(std::vector<Vertex>& vertices) {
    int n = vertices.size();
    int distance = 0;
    double T;
    int a, b, c, d;
    double r, p;
    std::vector<int> curr_cycle(n);
    std::vector<int> new_cycle(n);

    for (int i = 0; i < n; ++i) {
        curr_cycle[i] = i;
    }

    double curr_length = cycle_length(vertices, curr_cycle);

    for (int i = 100; i >= 1; i--) {
        T = 0.001 * pow(i, 2);
        for (int it = 0; it < MAX_IT; it++) {
            a = rand() % n;
            b = rand() % n;
            c = rand() % n;
            d = rand() % n;

            while(a == c || a == d){
                a = rand() % n;
            }
            while(b == c || b == d){
                b = rand() % n;
            }

            new_cycle = curr_cycle;

            opt(new_cycle, a, b);
            opt(new_cycle, c, d);

            double new_length = cycle_length(vertices, new_cycle);

            if (new_length < curr_length) {
                curr_cycle = new_cycle; 
                curr_length = new_length;
            } 
            else{
                r = (double)(rand()) / RAND_MAX;
                if(r < exp((curr_length - new_length) / T)) {
                    curr_cycle = new_cycle;
                    curr_length = new_length;
                }
            }
        }
    }
    distance = curr_length;
    std::cout << "distance: " << distance << std::endl; 
    return curr_cycle;
}

int main() {
    srand(time(NULL));

    std::ifstream inputFile("input_150.dat");
    std::vector<Vertex> vertices;
    Vertex vertex;
    int x, y;
    while(inputFile >> x >> y){
        vertex.x = x;
        vertex.y = y;
        vertices.push_back(vertex);
    }
    inputFile.close();

    std::vector<int> best_cycle = algorithm(vertices);

    std::ofstream outputFile("data_cycle.dat"); 

    if (outputFile.is_open()){
        for (int i = 0; i < vertices.size(); i++){
            outputFile << vertices[best_cycle[i]].x << " " << vertices[best_cycle[i]].y << std::endl;
        }
        outputFile << vertices[best_cycle[0]].x << " " << vertices[best_cycle[0]].y << std::endl;
        outputFile.close();
    }
    else{
        std::cout << "Error" << std::endl;
    }

    return 0;
}
