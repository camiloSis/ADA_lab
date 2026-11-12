#include <iostream>
#include <vector>

using namespace std;

const int N = 5;

int dist[N][N] = {
    { 0, 10, 15, 20, 25},
    {10,  0, 35, 25, 30},
    {15, 35,  0, 30,  5},
    {20, 25, 30,  0, 15},
    {25, 30,  5, 15,  0}
};

int main() {
    int inicio = 0;

    vector<bool> visitado(N, false);
    vector<int> ruta = { inicio };
    visitado[inicio] = true;

    for (int paso = 1; paso < N; paso++) {
        int actual = ruta.back();
        int masCercano = -1;
        int mejorDist = 1000000;

        for (int c = 0; c < N; c++) {
            if (!visitado[c] && dist[actual][c] < mejorDist) {
                mejorDist = dist[actual][c];
                masCercano = c;
            }
        }

        ruta.push_back(masCercano);
        visitado[masCercano] = true;
    }

    int costo = 0;
    for (int i = 0; i + 1 < N; i++) costo += dist[ruta[i]][ruta[i + 1]];
    costo += dist[ruta.back()][ruta[0]];

    cout << "Ruta (Nearest Neighbor): ";
    for (int c : ruta) cout << c << " -> ";
    cout << ruta[0] << endl;
    cout << "Costo total: " << costo << endl;

    return 0;
}
