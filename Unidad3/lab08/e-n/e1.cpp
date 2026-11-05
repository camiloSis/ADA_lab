#include <iostream>
#include <vector>
#include <algorithm>
#include <climits>
#include <chrono>
#include <iomanip>
#include "tsp_comun.h"
using namespace std;

int main() {
    const int N = 10;
    const unsigned SEMILLA = 2026;

    vector<Ciudad> ciudades = generarCiudades(N, SEMILLA);
    vector<vector<int>> dist = matrizDistancias(ciudades);

    cout << "Ciudades generadas (id: x, y):\n";
    for (int i = 0; i < N; i++)
        cout << "  " << i << ": (" << ciudades[i].x << ", " << ciudades[i].y << ")\n";

    // La ciudad 0 es el origen fijo; se permutan solo las ciudades 1..N-1.
    vector<int> perm;
    for (int i = 1; i < N; i++) perm.push_back(i);

    int mejorCosto = INT_MAX;
    vector<int> mejorRuta;
    long long evaluadas = 0;

    auto inicio = chrono::steady_clock::now();

    do {
        if (perm.front() > perm.back()) continue;

        evaluadas++;
        int costo = costoRuta(dist, perm);
        if (costo < mejorCosto) {
            mejorCosto = costo;
            mejorRuta = perm;
        }
    } while (next_permutation(perm.begin(), perm.end()));

    auto fin = chrono::steady_clock::now();
    double ms = chrono::duration<double, milli>(fin - inicio).count();

    cout << "\nRuta optima (fuerza bruta): 0 -> ";
    for (int c : mejorRuta) cout << c << " -> ";
    cout << "0\n";
    cout << "Costo optimo: " << mejorCosto << "\n";
    cout << "Rutas distintas evaluadas: " << evaluadas << "\n";
    cout << fixed << setprecision(3);
    cout << "Tiempo de ejecucion: " << ms << " ms\n";

    return 0;
}