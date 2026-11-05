#include <iostream>
#include <vector>
#include <algorithm>
#include <climits>
#include <random>
#include <iomanip>
#include <numeric>
#include <sstream>
#include "tsp_comun.h"
using namespace std;

// Optimo real por fuerza bruta (misma logica del ejercicio 1).
int optimoFuerzaBruta(const vector<vector<int>> &dist, int N) {
    vector<int> perm;
    for (int i = 1; i < N; i++) perm.push_back(i);
    int mejor = INT_MAX;
    do {
        if (perm.front() > perm.back()) continue;
        mejor = min(mejor, costoRuta(dist, perm));
    } while (next_permutation(perm.begin(), perm.end()));
    return mejor;
}

// Una corrida de Monte Carlo: devuelve el mejor costo visto tras "iteraciones" rutas al azar.
int monteCarlo(const vector<vector<int>> &dist, int N, int iteraciones, mt19937 &rng) {
    vector<int> ruta;
    for (int i = 1; i < N; i++) ruta.push_back(i);
    int mejor = INT_MAX;
    for (int it = 0; it < iteraciones; it++) {
        shuffle(ruta.begin(), ruta.end(), rng); 
        mejor = min(mejor, costoRuta(dist, ruta)); 
    }
    return mejor;
}

int main() {
    const int N = 10;
    const unsigned SEMILLA = 2026;          // misma instancia que el ejercicio 1
    const int REPETICIONES = 100;  

    vector<vector<int>> dist = matrizDistancias(generarCiudades(N, SEMILLA));
    int optimo = optimoFuerzaBruta(dist, N);
    cout << "Optimo real (fuerza bruta): " << optimo << "\n\n";

    mt19937 rng(12345);
    vector<int> configuraciones = {100, 1000, 10000};

    cout << "Cada fila resume " << REPETICIONES << " corridas independientes de Monte Carlo.\n\n";
    cout << left << setw(12) << "Iteraciones" << setw(14) << "1ra corrida"
         << setw(12) << "Mejor" << setw(12) << "Peor" << setw(12) << "Promedio"
         << setw(14) << "Brecha prom." << "Veces optimo\n";
    cout << string(88, '-') << "\n";

    for (int k : configuraciones) {
        vector<int> resultados;
        for (int r = 0; r < REPETICIONES; r++)
            resultados.push_back(monteCarlo(dist, N, k, rng));

        int mejor = *min_element(resultados.begin(), resultados.end());
        int peor = *max_element(resultados.begin(), resultados.end());
        double prom = accumulate(resultados.begin(), resultados.end(), 0.0) / REPETICIONES;
        double brecha = (prom - optimo) * 100.0 / optimo;
        int aciertos = count(resultados.begin(), resultados.end(), optimo);

        cout << left << setw(12) << k << setw(14) << resultados[0]
             << setw(12) << mejor << setw(12) << peor
             << setw(12) << fixed << setprecision(1) << prom
             << setw(14) << ([&]{ ostringstream o; o << fixed << setprecision(1) << brecha << "%"; return o.str(); }())
             << aciertos << "/" << REPETICIONES << "\n";
    }
    return 0;
}