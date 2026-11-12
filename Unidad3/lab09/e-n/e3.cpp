#include "tsp.h"

// Tiempo medio de ejecutar la heurística desde los N orígenes; se repite porque una sola corrida dura casi 0.
template <class F> double tiempoMs(F heuristica, const Mat& d, int reps = 2000) {
    auto t0 = chrono::steady_clock::now();
    double sumidero = 0;  // evita que el compilador elimine las llamadas
    for (int k = 0; k < reps; k++)
        for (int o = 0; o < (int)d.size(); o++) sumidero += heuristica(o, d)[0];
    auto t1 = chrono::steady_clock::now();
    return chrono::duration<double, milli>(t1 - t0).count() / reps + 0 * sumidero;
}

int main() {
    const int N = 15;
    Instancia I = generar(N);

    vector<double> nn(N), ci(N);
    int gCI = 0, gNN = 0, emp = 0;
    printf("%-7s %10s %12s %8s\n", "Origen", "NN", "Ins. barata", "Gana");
    for (int o = 0; o < N; o++) {
        nn[o] = costo(vecinoCercano(o, I.d), I.d);
        ci[o] = costo(insercionBarata(o, I.d), I.d);
        bool empate = fabs(nn[o] - ci[o]) < EPS;
        (empate ? emp : ci[o] < nn[o] ? gCI : gNN)++;
        printf("%-7d %10.3f %12.3f %8s\n", o, nn[o], ci[o], empate ? "empate" : ci[o] < nn[o] ? "CI" : "NN");
    }

    Resumen a = resumir(nn), b = resumir(ci);
    double tNN = tiempoMs(vecinoCercano, I.d), tCI = tiempoMs(insercionBarata, I.d);
    printf("\n%-12s %9s %9s %9s %12s %10s %11s\n", "", "Mejor", "Peor", "Media", "Casos mejor", "Distintos", "Tiempo(ms)");
    printf("%-12s %9.3f %9.3f %9.3f %9d/%d %10d %11.4f\n", "NN", a.mejor, a.peor, a.media, a.enMejor, N, a.distintos, tNN);
    printf("%-12s %9.3f %9.3f %9.3f %9d/%d %10d %11.4f\n", "Ins. barata", b.mejor, b.peor, b.media, b.enMejor, N, b.distintos, tCI);

    printf("\nPor origen: CI gana %d, NN gana %d, empates %d\n", gCI, gNN, emp);
    printf("Mejora media de CI sobre NN: %.2f%% | Mejor global: %s\n", 100 * (a.media - b.media) / a.media,
           fabs(a.mejor - b.mejor) < EPS ? "empate" : a.mejor < b.mejor ? "NN" : "CI");
    printf("Costo de tiempo: CI es %.1f veces más lenta que NN\n", tCI / tNN);
}