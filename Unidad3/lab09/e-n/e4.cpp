// Ejercicio 4: tiempo de Nearest Neighbor + 2-opt para 20, 50 y 100 ciudades,
// contra el tiempo ESTIMADO (no ejecutado) de la fuerza bruta: (n-1)!/2 rutas.
#include "tsp.h"

// Tiempo medio (ms) de una corrida de NN + 2-opt desde la ciudad 0 (solo el algoritmo: sin generar datos ni imprimir).
// Se repite porque una sola corrida es muy corta; devuelve también el costo de la ruta obtenida.
double tiempoHeuristica(const Mat& d, int reps, double& costoFinal) {
    auto t0 = chrono::steady_clock::now();
    for (int k = 0; k < reps; k++) costoFinal = costo(dosOpt(vecinoCercano(0, d), d), d);
    return chrono::duration<double, milli>(chrono::steady_clock::now() - t0).count() / reps;
}

// Segundos que tarda la fuerza bruta en procesar UNA ruta: se mide enumerando permutaciones reales
// (next_permutation + costo) y se extrapola al total (n-1)!/2, sin ejecutar la enumeración completa.
double segundosPorRuta(const Mat& d, long muestra = 1000000) {
    int n = d.size();
    Ruta r(n);
    iota(r.begin(), r.end(), 0);  // la ciudad 0 queda fija: ahí se evitan las n rotaciones del mismo ciclo
    double sumidero = 0;
    auto t0 = chrono::steady_clock::now();
    for (long k = 0; k < muestra; k++) {
        sumidero += costo(r, d);
        next_permutation(r.begin() + 1, r.end());
    }
    double s = chrono::duration<double>(chrono::steady_clock::now() - t0).count();
    return s / muestra + 0 * sumidero;  // sumidero evita que el compilador elimine el bucle
}

int main() {
    const double SEG_ANIO = 365.25 * 24 * 3600, EDAD_UNIVERSO = 1.38e10;  // años
    printf("%-5s %12s %14s %14s %14s %14s %12s\n", "n", "Costo", "NN+2opt (ms)", "s/ruta (BF)", "Rutas (n-1)!/2", "BF (años)", "BF/NN+2opt");
    for (int n : {20, 50, 100}) {
        Instancia I = generar(n);  // misma semilla: las primeras ciudades coinciden con las de los otros ejercicios
        double c = 0, msH = tiempoHeuristica(I.d, 20000 / n, c);
        double spr = segundosPorRuta(I.d);
        double rutas = exp(lgamma(n)) / 2;  // lgamma(n) = ln((n-1)!); evita desbordar un entero
        double segBF = rutas * spr;
        printf("%-5d %12.3f %14.4f %14.2e %14.2e %14.2e %12.2e\n", n, c, msH, spr, rutas, segBF / SEG_ANIO, segBF / (msH / 1000));
    }
    printf("\nPara comparar: la edad del universo es ~%.2e años.\n", EDAD_UNIVERSO);
    printf("(BF = fuerza bruta, estimada: tiempo medido por ruta x número de rutas; no se ejecutó.)\n");
}