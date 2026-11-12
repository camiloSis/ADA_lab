// tsp.h — nucleo compartido por los todos ejercicios 
#pragma once
#include <bits/stdc++.h>
using namespace std;

using Mat  = vector<vector<double>>;
using Ruta = vector<int>;   // orden de visita; el ciclo se cierra solo (último -> primero)
const double EPS = 1e-9;    // tolerancia: los doubles nunca se comparan con ==

// ---------- Instancia ----------
struct Instancia { int n; vector<pair<double, double>> p; Mat d; };

// Semilla fija: los ejercicios encadenados trabajan con las MISMAS ciudades.
inline Instancia generar(int n, unsigned semilla = 42) {
    mt19937 gen(semilla);
    uniform_real_distribution<double> U(0, 100);
    Instancia I{n, vector<pair<double, double>>(n), Mat(n, vector<double>(n))};
    for (auto& c : I.p) c = {U(gen), U(gen)};
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)  // se precalcula: las heurísticas consultan d muchas veces
            I.d[i][j] = hypot(I.p[i].first - I.p[j].first, I.p[i].second - I.p[j].second);
    return I;
}

// Costo del ciclo cerrado.
inline double costo(const Ruta& r, const Mat& d) {
    double s = 0;
    for (size_t i = 0; i < r.size(); i++) s += d[r[i]][r[(i + 1) % r.size()]];
    return s;
}

// ---------- Heurísticas constructivas ----------
// Vecino más cercano: desde la ciudad actual, va a la no visitada más cercana.
inline Ruta vecinoCercano(int origen, const Mat& d) {
    int n = d.size();
    Ruta r{origen};
    vector<bool> vis(n, false);
    vis[origen] = true;
    while ((int)r.size() < n) {
        int act = r.back(), mejor = -1;
        for (int j = 0; j < n; j++)
            if (!vis[j] && (mejor < 0 || d[act][j] < d[act][mejor])) mejor = j;
        vis[mejor] = true;
        r.push_back(mejor);
    }
    return r;
}

// Inserción más barata: parte de {origen, su ciudad más cercana} e inserta, en cada paso,
// la ciudad k y la arista (a,b) que minimizan d[a][k] + d[k][b] - d[a][b].
inline Ruta insercionBarata(int origen, const Mat& d) {
    int n = d.size(), cerca = -1;
    for (int j = 0; j < n; j++)
        if (j != origen && (cerca < 0 || d[origen][j] < d[origen][cerca])) cerca = j;
    Ruta r{origen, cerca};
    vector<bool> vis(n, false);
    vis[origen] = vis[cerca] = true;
    while ((int)r.size() < n) {
        double mejorDelta = 1e18;
        int mejorK = -1, pos = -1;
        for (int k = 0; k < n; k++) {
            if (vis[k]) continue;
            for (size_t i = 0; i < r.size(); i++) {
                int a = r[i], b = r[(i + 1) % r.size()];
                double delta = d[a][k] + d[k][b] - d[a][b];  // solo el aumento, sin recalcular la ruta
                if (delta < mejorDelta) mejorDelta = delta, mejorK = k, pos = i + 1;
            }
        }
        r.insert(r.begin() + pos, mejorK);
        vis[mejorK] = true;
    }
    return r;
}

// ---------- Búsqueda local ----------
// 2-opt: invierte el tramo r[i+1..j] mientras reemplazar las aristas (a,b),(c,e) por (a,c),(b,e) acorte.
// Solo se evalúa el delta de las 2 aristas que cambian.
inline Ruta dosOpt(Ruta r, const Mat& d) {
    int n = r.size();
    bool mejora = true;
    while (mejora) {
        mejora = false;
        for (int i = 0; i < n - 1; i++)
            for (int j = i + 1; j < n; j++) {
                if (i == 0 && j == n - 1) continue;  // aristas contiguas: no hay cambio
                int a = r[i], b = r[i + 1], c = r[j], e = r[(j + 1) % n];
                if (d[a][c] + d[b][e] - d[a][b] - d[c][e] < -EPS) {
                    reverse(r.begin() + i + 1, r.begin() + j + 1);
                    mejora = true;
                }
            }
    }
    return r;
}

// ---------- Resumen de resultados ----------
struct Resumen { double mejor, peor, media; int idxMejor, enMejor, distintos; };

// "Que el programa cuente por ti": mejor, peor, media, cuántos casos alcanzan el mejor
// y cuántos costos distintos hay (distintos == 1 => todos los casos dan el mismo resultado).
inline Resumen resumir(const vector<double>& v) {
    double mejor = *min_element(v.begin(), v.end());
    // primer origen dentro de la tolerancia: evita que una diferencia de 1e-13 entre
    // rotaciones del mismo ciclo elija un "mejor" arbitrario
    int im = find_if(v.begin(), v.end(), [&](double x) { return x - mejor < EPS; }) - v.begin();
    vector<double> s = v;
    sort(s.begin(), s.end());
    int dist = 1;
    for (size_t i = 1; i < s.size(); i++) dist += s[i] - s[i - 1] > EPS;
    return {mejor, s.back(), accumulate(v.begin(), v.end(), 0.0) / v.size(), im,
            (int)count_if(v.begin(), v.end(), [&](double x) { return x - mejor < EPS; }), dist};
}