#include <iostream>
#include <vector>
#include <algorithm>
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
    vector<int> ciudades = { 1, 2, 3, 4 }; // se fija la ciudad 0 como origen

    int mejorCosto = INT_MAX;
    vector<int> mejorRuta;

    sort(ciudades.begin(), ciudades.end());
    do {
        int costo = dist[0][ciudades[0]];
        for (int i = 0; i < (int)ciudades.size() - 1; i++)
            costo += dist[ciudades[i]][ciudades[i + 1]];
        costo += dist[ciudades.back()][0];

        if (costo < mejorCosto) {
            mejorCosto = costo;
            mejorRuta = ciudades;
        }
    } while (next_permutation(ciudades.begin(), ciudades.end()));

    cout << "Ruta optima (fuerza bruta): 0 -> ";
    for (int c : mejorRuta) cout << c << " -> ";
    cout << "0" << endl;
    cout << "Costo optimo: " << mejorCosto << endl;

    return 0;
}
