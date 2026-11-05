#include <iostream>
#include <vector>
#include <algorithm>
#include <random>
#include <climits>
using namespace std;

int main() {
    vector<vector<int>> dist = {
        { 0, 10, 15, 20, 25 },
        { 10, 0, 35, 25, 30 },
        { 15, 35, 0, 30, 5 },
        { 20, 25, 30, 0, 15 },
        { 25, 30, 5, 15, 0 }
    };
    vector<int> ciudades = { 1, 2, 3, 4 };

    mt19937 rng(random_device{}());
    int mejorCosto = INT_MAX;
    vector<int> mejorRuta;
    int iteraciones = 200;

    for (int it = 0; it < iteraciones; it++) {
        shuffle(ciudades.begin(), ciudades.end(), rng);

        int costo = dist[0][ciudades[0]];
        for (int i = 0; i < (int)ciudades.size() - 1; i++)
            costo += dist[ciudades[i]][ciudades[i + 1]];
        costo += dist[ciudades.back()][0];

        if (costo < mejorCosto) {
            mejorCosto = costo;
            mejorRuta = ciudades;
        }
    }

    cout << "Mejor ruta encontrada (Monte Carlo, " << iteraciones << " iter): 0 -> ";
    for (int c : mejorRuta) cout << c << " -> ";
    cout << "0" << endl;
    cout << "Costo encontrado: " << mejorCosto << endl;

    return 0;
}
