// Ejercicio 2: 2-opt sobre las 15 soluciones de Nearest Neighbor (Ejercicio 1).
// Pregunta: ¿el mejor resultado final sigue dependiendo de la ciudad de origen?
#include "tsp.h"

int main() {
    const int N = 15;
    Instancia I = generar(N);  // misma semilla que el Ejercicio 1: mismas ciudades

    vector<double> antes(N), despues(N);
    printf("%-7s %10s %12s %9s\n", "Origen", "NN", "NN + 2-opt", "Mejora");
    for (int o = 0; o < N; o++) {
        Ruta nn = vecinoCercano(o, I.d);
        antes[o] = costo(nn, I.d);
        despues[o] = costo(dosOpt(nn, I.d), I.d);
        printf("%-7d %10.3f %12.3f %8.2f%%\n", o, antes[o], despues[o], 100 * (antes[o] - despues[o]) / antes[o]);
    }

    Resumen a = resumir(antes), d = resumir(despues);
    printf("\n%-11s %9s %9s %9s %12s %10s\n", "", "Mejor", "Peor", "Media", "Casos mejor", "Distintos");
    printf("%-11s %9.3f %9.3f %9.3f %9d/%d %10d\n", "NN", a.mejor, a.peor, a.media, a.enMejor, N, a.distintos);
    printf("%-11s %9.3f %9.3f %9.3f %9d/%d %10d\n", "NN + 2-opt", d.mejor, d.peor, d.media, d.enMejor, N, d.distintos);

    printf("\nDispersión (peor vs mejor): NN %.2f%% -> NN + 2-opt %.2f%%\n",
           100 * (a.peor - a.mejor) / a.mejor, 100 * (d.peor - d.mejor) / d.mejor);
    printf("Origen del mejor: NN = %d, NN + 2-opt = %d\n", a.idxMejor, d.idxMejor);
    printf("¿El resultado final depende del origen? %s (%d costos distintos; el mejor se alcanza desde %d de %d orígenes)\n",
           d.distintos > 1 ? "SÍ" : "NO", d.distintos, d.enMejor, N);
}