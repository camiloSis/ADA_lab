#include "tsp.h"
 
int main() {
    const int N = 15;
    Instancia I = generar(N);
 
    vector<double> costos(N);
    printf("%-7s %10s\n", "Origen", "Costo NN");
    for (int o = 0; o < N; o++) {
        costos[o] = costo(vecinoCercano(o, I.d), I.d);
        printf("%-7d %10.3f\n", o, costos[o]);
    }
 
    Resumen r = resumir(costos);
    printf("\nMejor: %.3f (origen %d) | Peor: %.3f | Media: %.3f\n", r.mejor, r.idxMejor, r.peor, r.media);
    printf("Orígenes que alcanzan el mejor: %d/%d | Costos distintos: %d\n", r.enMejor, N, r.distintos);
    printf("¿Cambia según el origen? %s (peor excede al mejor en %.2f%%)\n",
           r.distintos > 1 ? "SÍ" : "NO", 100 * (r.peor - r.mejor) / r.mejor);
}