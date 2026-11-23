// Ejercicio 2: IG con d = 1, 2, 3, 5 y 8 ciudades destruidas, 10 semillas cada una.
// Se reporta el costo promedio (y algunas medidas extra) para cada valor de d.
#include <iostream>
#include <iomanip>
#include <cmath>
#include "tsp_meta.h"
using namespace std;

int main() {
    const int ITERACIONES = 100;
    const int SEMILLAS = 10;
    const int VALORES_D[] = {1, 2, 3, 5, 8};

    Matriz d = matrizDist(instancia12());
    double optimo = optimoHeldKarp(d);

    Ruta inicial = vecinoMasCercano(d);
    dosOpt(d, inicial);

    cout << fixed << setprecision(2);
    cout << "Optimo exacto: " << optimo << " | NN + 2-opt (inicio de IG): " << costo(d, inicial) << "\n";
    cout << "IG con " << ITERACIONES << " iteraciones, " << SEMILLAS << " semillas por valor de d\n\n";

    cout << left << setw(6) << "d" << setw(16) << "Costo promedio" << setw(10) << "Mejor"
         << setw(10) << "Peor" << setw(18) << "Veces optimo" << "Brecha prom.\n";
    cout << string(68, '-') << "\n";

    for (int dd : VALORES_D) {
        double suma = 0, mejor = INF, peor = 0;
        int aciertos = 0;
        for (int s = 1; s <= SEMILLAS; s++) {
            Resultado r = ig(d, ITERACIONES, s, dd);
            suma += r.costoMejor;
            mejor = min(mejor, r.costoMejor);
            peor = max(peor, r.costoMejor);
            if (fabs(r.costoMejor - optimo) < 1e-6) aciertos++;
        }
        double prom = suma / SEMILLAS;
        cout << left << setw(6) << dd << setw(16) << prom << setw(10) << mejor << setw(10) << peor
             << setw(18) << (to_string(aciertos) + "/" + to_string(SEMILLAS))
             << (prom - optimo) * 100.0 / optimo << "%\n";
    }
    return 0;
}