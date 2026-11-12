#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

const int N = 5;

int dist[N][N] = {
    { 0, 10, 15, 20, 25},
    {10,  0, 35, 25, 30},
    {15, 35,  0, 30,  5},
    {20, 25, 30,  0, 15},
    {25, 30,  5, 15,  0}
};

int costoRuta(const vector<int>& ruta) {
    int c = 0;

    for (int i = 0; i + 1 < N; i++) c += dist[ruta[i]][ruta[i + 1]];
    c += dist[ruta[N - 1]][ruta[0]];

    return c;
}

int main() {
    vector<int> ruta = { 0, 1, 2, 4, 3 };

    cout << "Ruta inicial: ";
    for (int c : ruta) cout << c << " -> ";
    cout << ruta[0] << "  (costo " << costoRuta(ruta) << ")" << endl;

    bool mejora = true;
    while (mejora) {
        mejora = false;

        for (int i = 1; i < N - 1; i++) {
            for (int j = i + 1; j < N; j++) {
                vector<int> nueva = ruta;
                reverse(nueva.begin() + i, nueva.begin() + j + 1);

                if (costoRuta(nueva) < costoRuta(ruta)) {
                    ruta = nueva;
                    mejora = true;
                }
            }
        }
    }

    cout << "Ruta (2-opt): ";
    for (int c : ruta) cout << c << " -> ";
    cout << ruta[0] << endl;
    cout << "Costo total: " << costoRuta(ruta) << endl;

    return 0;
}
