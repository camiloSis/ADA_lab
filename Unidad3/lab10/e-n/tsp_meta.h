// tsp_meta.h
// Utilidades compartidas por los ejercicios del Laboratorio 10 (ILS e IG para el TSP).
//
// Convenciones:
//  - Una ruta es un vector<int> con una permutacion de 0..n-1 y se interpreta como
//    circuito CERRADO (despues de la ultima ciudad se vuelve a la primera).
//  - Las distancias son euclidianas en double, guardadas en una matriz n x n.
#pragma once
#include <vector>
#include <random>
#include <cmath>
#include <algorithm>
#include <limits>
using namespace std;

struct Punto { double x, y; };
using Matriz = vector<vector<double>>;
using Ruta = vector<int>;

const double EPS = 1e-9;
const double INF = numeric_limits<double>::infinity();

// ---------------------------------------------------------------------------
// Instancias
// ---------------------------------------------------------------------------

// n puntos con coordenadas de un decimal en [0, lado]. Se usa mt19937 "a mano"
// (sin distribuciones de <random>) para que la instancia sea reproducible.
inline vector<Punto> generarPuntos(int n, unsigned semilla, double lado) {
    mt19937 rng(semilla);
    int pasos = (int)lround(lado * 10) + 1;
    vector<Punto> p(n);
    for (auto &q : p) {
        q.x = (rng() % pasos) / 10.0;
        q.y = (rng() % pasos) / 10.0;
    }
    return p;
}

// TSP de 12 ciudades del ejercicio resuelto por la docente (optimo exacto = 72.21),
// usado en los ejercicios 1 a 3.
inline vector<Punto> instancia12() {
    return {{0, 0}, {3, 14}, {18, 5}, {8, 7}, {6, 2}, {10, 0},
            {4, 4}, {1, 13}, {19, 11}, {8, 14}, {2, 17}, {7, 18}};
}

inline Matriz matrizDist(const vector<Punto> &p) {
    int n = (int)p.size();
    Matriz d(n, vector<double>(n, 0.0));
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            d[i][j] = hypot(p[i].x - p[j].x, p[i].y - p[j].y);
    return d;
}

inline double costo(const Matriz &d, const Ruta &r) {
    int n = (int)r.size();
    double c = 0;
    for (int i = 0; i < n; i++) c += d[r[i]][r[(i + 1) % n]];
    return c;
}

// ---------------------------------------------------------------------------
// Constructivo y busqueda local
// ---------------------------------------------------------------------------

// Nearest Neighbor: desde "inicio", ir siempre a la ciudad no visitada mas cercana.
inline Ruta vecinoMasCercano(const Matriz &d, int inicio = 0) {
    int n = (int)d.size();
    vector<bool> vis(n, false);
    Ruta r;
    int act = inicio;
    vis[act] = true;
    r.push_back(act);
    for (int k = 1; k < n; k++) {
        int mejor = -1;
        double md = INF;
        for (int j = 0; j < n; j++)
            if (!vis[j] && d[act][j] < md) { md = d[act][j]; mejor = j; }
        vis[mejor] = true;
        r.push_back(mejor);
        act = mejor;
    }
    return r;
}

// 2-opt: invierte tramos mientras alguna inversion reduzca el costo.
// Calcula el cambio con solo 4 aristas (delta), sin recalcular toda la ruta.
inline void dosOpt(const Matriz &d, Ruta &r) {
    int n = (int)r.size();
    bool mejora = true;
    while (mejora) {
        mejora = false;
        for (int i = 0; i < n - 1; i++) {
            for (int j = i + 2; j < n; j++) {
                if (i == 0 && j == n - 1) continue; // son aristas adyacentes en el ciclo
                int a = r[i], b = r[i + 1], c = r[j], e = r[(j + 1) % n];
                double delta = d[a][c] + d[b][e] - d[a][b] - d[c][e];
                if (delta < -EPS) {
                    reverse(r.begin() + i + 1, r.begin() + j + 1);
                    mejora = true;
                }
            }
        }
    }
}

// ---------------------------------------------------------------------------
// Resultado comun de las metaheuristicas
// ---------------------------------------------------------------------------
struct Resultado {
    Ruta mejor;
    double costoInicial = 0;  // NN + 2-opt
    double costoMejor = 0;
    int iterMejor = 0;        // iteracion en que aparecio la mejor solucion (0 = la inicial)
};

// ---------------------------------------------------------------------------
// ILS: perturbacion double-bridge + 2-opt
// ---------------------------------------------------------------------------

// Corta la ruta en 3 puntos (4 segmentos A B C D) y la rearma como A C B D.
inline Ruta doubleBridge(const Ruta &r, mt19937 &rng) {
    int n = (int)r.size();
    int p[3];
    do {
        for (int k = 0; k < 3; k++) p[k] = 1 + (int)(rng() % (n - 1));
        sort(p, p + 3);
    } while (p[0] == p[1] || p[1] == p[2]);
    Ruta nueva;
    nueva.reserve(n);
    nueva.insert(nueva.end(), r.begin(), r.begin() + p[0]);        // A
    nueva.insert(nueva.end(), r.begin() + p[1], r.begin() + p[2]); // C
    nueva.insert(nueva.end(), r.begin() + p[0], r.begin() + p[1]); // B
    nueva.insert(nueva.end(), r.begin() + p[2], r.end());          // D
    return nueva;
}

// probPeor = 0   -> aceptacion estricta (solo si mejora la actual).
// probPeor > 0   -> ademas acepta una solucion peor con esa probabilidad.
// Siempre se guarda aparte la mejor solucion encontrada.
inline Resultado ils(const Matriz &d, int iteraciones, unsigned semilla, double probPeor = 0.0) {
    mt19937 rng(semilla);
    Ruta actual = vecinoMasCercano(d);
    dosOpt(d, actual);
    double cActual = costo(d, actual);

    Resultado res;
    res.mejor = actual;
    res.costoInicial = res.costoMejor = cActual;

    for (int it = 1; it <= iteraciones; it++) {
        Ruta cand = doubleBridge(actual, rng);
        dosOpt(d, cand);
        double cc = costo(d, cand);

        bool acepta = cc < cActual - EPS;
        if (!acepta && cc > cActual + EPS && probPeor > 0.0)
            acepta = (rng() % 1000000) / 1000000.0 < probPeor;
        if (acepta) { actual = cand; cActual = cc; }

        if (cActual < res.costoMejor - EPS) {
            res.mejor = actual;
            res.costoMejor = cActual;
            res.iterMejor = it;
        }
    }
    return res;
}

// ---------------------------------------------------------------------------
// IG: destruir "nDestruir" ciudades y reconstruir con insercion golosa
// ---------------------------------------------------------------------------
inline Resultado ig(const Matriz &d, int iteraciones, unsigned semilla, int nDestruir,
                    bool conBusquedaLocal = false) {
    mt19937 rng(semilla);
    Ruta actual = vecinoMasCercano(d);
    dosOpt(d, actual);
    double cActual = costo(d, actual);

    Resultado res;
    res.mejor = actual;
    res.costoInicial = res.costoMejor = cActual;

    for (int it = 1; it <= iteraciones; it++) {
        Ruta cand = actual;

        // Destruccion: sacar nDestruir ciudades elegidas al azar.
        vector<int> quitadas;
        for (int k = 0; k < nDestruir; k++) {
            int pos = (int)(rng() % cand.size());
            quitadas.push_back(cand[pos]);
            cand.erase(cand.begin() + pos);
        }

        // Reconstruccion golosa: cada ciudad va a la posicion que menos aumenta el costo.
        for (int c : quitadas) {
            int m = (int)cand.size();
            int mejorPos = 0;
            double mejorInc = INF;
            for (int pos = 0; pos < m; pos++) {
                int a = cand[pos], b = cand[(pos + 1) % m];
                double inc = d[a][c] + d[c][b] - d[a][b];
                if (inc < mejorInc - EPS) { mejorInc = inc; mejorPos = pos; }
            }
            cand.insert(cand.begin() + mejorPos + 1, c);
        }

        if (conBusquedaLocal) dosOpt(d, cand);

        double cc = costo(d, cand);
        if (cc < cActual - EPS) {          // aceptacion estricta
            actual = cand;
            cActual = cc;
            res.mejor = actual;
            res.costoMejor = cc;
            res.iterMejor = it;
        }
    }
    return res;
}

// ---------------------------------------------------------------------------
// Optimo exacto (Held-Karp, programacion dinamica). Solo para n pequeno (<= ~20):
// sirve para saber el optimo real de la instancia de 12 ciudades.
// ---------------------------------------------------------------------------
inline double optimoHeldKarp(const Matriz &d) {
    int n = (int)d.size(), m = n - 1;
    vector<double> dp((size_t)(1 << m) * m, INF);
    auto at = [&](int mask, int j) -> double & { return dp[(size_t)mask * m + j]; };
    for (int j = 0; j < m; j++) at(1 << j, j) = d[0][j + 1];
    for (int mask = 1; mask < (1 << m); mask++)
        for (int j = 0; j < m; j++) {
            if (!(mask & (1 << j)) || at(mask, j) == INF) continue;
            for (int k = 0; k < m; k++) {
                if (mask & (1 << k)) continue;
                double v = at(mask, j) + d[j + 1][k + 1];
                double &dest = at(mask | (1 << k), k);
                if (v < dest) dest = v;
            }
        }
    double mejor = INF;
    for (int j = 0; j < m; j++) mejor = min(mejor, at((1 << m) - 1, j) + d[j + 1][0]);
    return mejor;
}