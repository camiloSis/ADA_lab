// Funciones compartidas por los ejercicios 1 y 2 para que ambos trabajen
#pragma once
#include <vector>
#include <random>
#include <cmath>
using namespace std;

struct Ciudad {
    int x, y;
};

// Genera n ciudades con coordenadas enteras aleatorias en [0, 100].
inline vector<Ciudad> generarCiudades(int n, unsigned semilla) {
    mt19937 rng(semilla);
    uniform_int_distribution<int> coord(0, 100);
    vector<Ciudad> ciudades(n);
    for (auto &c : ciudades) {
        c.x = coord(rng);
        c.y = coord(rng);
    }
    return ciudades;
}

// Matriz simetrica de distancias euclidianas redondeadas a entero.
inline vector<vector<int>> matrizDistancias(const vector<Ciudad> &c) {
    int n = (int)c.size();
    vector<vector<int>> d(n, vector<int>(n, 0));
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            d[i][j] = (int)lround(hypot(c[i].x - c[j].x, c[i].y - c[j].y));
    return d;
}

inline int costoRuta(const vector<vector<int>> &d, const vector<int> &ruta) {
    int costo = d[0][ruta.front()];
    for (size_t i = 0; i + 1 < ruta.size(); i++)
        costo += d[ruta[i]][ruta[i + 1]];
    costo += d[ruta.back()][0];
    return costo;
}