#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>
#include <random>

using namespace std;

vector<vector<double>> dist;

double costoRuta(const vector<int>& ruta) {
    double c = 0;
    int n = ruta.size();

    for (int i = 0; i < n; i++) {
        c += dist[ruta[i]][ruta[(i + 1) % n]];
    }

    return c;
}

// Heurística constructiva: Nearest Neighbor desde la ciudad 0
vector<int> vecinoMasCercano(int n) {
    vector<bool> visitado(n, false);
    vector<int> ruta;

    ruta.push_back(0);
    visitado[0] = true;

    for (int paso = 1; paso < n; paso++) {
        int actual = ruta.back();
        int mejor = -1;

        for (int c = 0; c < n; c++) {
            if (!visitado[c] && (mejor == -1 || dist[actual][c] < dist[actual][mejor])) {
                mejor = c;
            }
        }

        ruta.push_back(mejor);
        visitado[mejor] = true;
    }

    return ruta;
}

// Inserción golosa: coloca la ciudad c en la posición donde MENOS aumenta el costo
void insertarGoloso(vector<int>& ruta, int c) {
    int n = ruta.size();
    int mejorPos = 1;
    double mejorAumento = 1e18;

    for (int pos = 1; pos <= n; pos++) {
        int a = ruta[pos - 1];
        int b = ruta[pos % n];
        double aumento = dist[a][c] + dist[c][b] - dist[a][b];

        if (aumento < mejorAumento) {
            mejorAumento = aumento;
            mejorPos = pos;
        }
    }

    ruta.insert(ruta.begin() + mejorPos, c);
}

int main() {
    vector<pair<double, double>> ciudad = {
        {0, 0}, {3, 14}, {18, 5}, {8, 7}, {6, 2}, {10, 0},
        {4, 4}, {1, 13}, {19, 11}, {8, 14}, {2, 17}, {7, 18}
    };

    int n = ciudad.size();
    dist.assign(n, vector<double>(n));

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            dist[i][j] = hypot(ciudad[i].first - ciudad[j].first,
                               ciudad[i].second - ciudad[j].second);
        }
    }

    mt19937 rng(42); // semilla fija: el resultado se puede reproducir

    const int D = 3; // cuántas ciudades se destruyen en cada iteración

    vector<int> actual = vecinoMasCercano(n); // solución inicial (constructiva)
    double costoActual = costoRuta(actual);

    vector<int> mejor = actual;
    double costoMejor = costoActual;

    cout << "Solución inicial (Nearest Neighbor): " << costoActual << endl;

    for (int it = 1; it <= 200; it++) {
        // DESTRUCCIÓN: quitar D ciudades al azar (la ciudad 0 se conserva como origen)
        vector<int> candidata = actual;
        vector<int> quitadas;

        for (int k = 0; k < D; k++) {
            int pos = 1 + rng() % (candidata.size() - 1);
            quitadas.push_back(candidata[pos]);
            candidata.erase(candidata.begin() + pos);
        }

        // CONSTRUCCIÓN: reinsertar cada ciudad quitada de forma golosa
        for (size_t k = 0; k < quitadas.size(); k++) {
            insertarGoloso(candidata, quitadas[k]);
        }

        double costoCand = costoRuta(candidata);

        if (costoCand < costoActual - 1e-9) { // criterio de aceptación
            actual = candidata;
            costoActual = costoCand;

            if (costoActual < costoMejor) {
                mejor = actual;
                costoMejor = costoActual;
                cout << "Iteración " << it << ": nuevo mejor costo = " << costoMejor << endl;
            }
        }
    }

    cout << "Ruta final (IG): ";
    for (size_t i = 0; i < mejor.size(); i++) {
        cout << mejor[i] << " -> ";
    }
    cout << mejor[0] << endl;

    cout << "Costo final: " << costoMejor << endl;

    return 0;
}
