#include <bits/stdc++.h>
using namespace std;

const int N = 15;
double X[N], Y[N], D[N][N];

double longitud(const vector<int>& r) {
    double t = 0;
    for (int i = 0; i < N; i++) t += D[r[i]][r[(i + 1) % N]];
    return t;
}

vector<int> vecinoMasCercano(int inicio) {
    vector<int> ruta = {inicio};
    vector<bool> visitada(N, false);
    visitada[inicio] = true;
    int actual = inicio;
    for (int paso = 1; paso < N; paso++) {
        int mejor = -1;
        for (int j = 0; j < N; j++)
            if (!visitada[j] && (mejor == -1 || D[actual][j] < D[actual][mejor]))
                mejor = j;
        visitada[mejor] = true;
        ruta.push_back(mejor);
        actual = mejor;
    }
    return ruta;
}

// 2-opt: invierte tramos mientras eso acorte el ciclo. Devuelve cuantas mejoras hizo.
int dosOpt(vector<int>& r) {
    int mejoras = 0;
    bool mejoro = true;
    while (mejoro) {
        mejoro = false;
        for (int i = 1; i < N - 1; i++)
            for (int j = i + 1; j < N; j++) {
                int a = r[i - 1], b = r[i], c = r[j], d = r[(j + 1) % N];
                double delta = D[a][c] + D[b][d] - D[a][b] - D[c][d];
                if (delta < -1e-9) {
                    reverse(r.begin() + i, r.begin() + j + 1);
                    mejoro = true;
                    mejoras++;
                }
            }
    }
    return mejoras;
}

int main() {
    mt19937 gen(42);  // misma semilla que el ejercicio anterior -> mismas ciudades
    uniform_real_distribution<double> U(0, 100);
    for (int i = 0; i < N; i++) { X[i] = U(gen); Y[i] = U(gen); }
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++) D[i][j] = hypot(X[i] - X[j], Y[i] - Y[j]);

    vector<double> antes(N), despues(N);
    vector<vector<int>> rutas(N);

    cout << "Origen | NN        | NN + 2-opt | Mejora   | Intercambios\n";
    for (int s = 0; s < N; s++) {
        rutas[s] = vecinoMasCercano(s);
        antes[s] = longitud(rutas[s]);
        int m = dosOpt(rutas[s]);
        despues[s] = longitud(rutas[s]);
        printf("  %2d   | %9.3f | %10.3f | %7.2f%% | %d\n", s, antes[s], despues[s],
               100.0 * (antes[s] - despues[s]) / antes[s], m);
    }

    int mejorNN = min_element(antes.begin(), antes.end()) - antes.begin();
    int mejorFin = min_element(despues.begin(), despues.end()) - despues.begin();
    double minFin = despues[mejorFin];
    double maxFin = *max_element(despues.begin(), despues.end());

    int alcanzan = 0;
    set<long long> distintas;
    mejorFin = -1;  // primer origen que llega al minimo (con tolerancia por redondeo)
    for (int s = 0; s < N; s++) {
        if (despues[s] - minFin < 1e-6) {
            alcanzan++;
            if (mejorFin == -1) mejorFin = s;
        }
        distintas.insert(llround(despues[s] * 1e6));
    }

    printf("\nSolo NN:        mejor %.3f (origen %d), peor %.3f\n", antes[mejorNN], mejorNN,
           *max_element(antes.begin(), antes.end()));
    printf("NN + 2-opt:     mejor %.3f (origen %d), peor %.3f\n", minFin, mejorFin, maxFin);
    printf("Dispersion final (peor-mejor): %.3f (%.2f%%)\n", maxFin - minFin,
           100.0 * (maxFin - minFin) / minFin);
    printf("Longitudes finales distintas: %zu de %d\n", distintas.size(), N);
    printf("Origenes que alcanzan el mejor final: %d de %d\n", alcanzan, N);

    cout << "\nMejor ruta final (origen " << mejorFin << "): ";
    for (int c : rutas[mejorFin]) cout << c << " -> ";
    cout << mejorFin << "\n";
    cout << (maxFin - minFin > 1e-6
        ? "El resultado final sigue dependiendo del origen.\n"
        : "El resultado final ya no depende del origen.\n");
}