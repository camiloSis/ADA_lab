// Ejercicio 3: ILS con aceptación estricta y aceptación probabilística del 5 %.
#include <iostream>
#include <iomanip>
#include <cmath>
#include <string>
#include "tsp_meta.h"
using namespace std;

void comparar(const string &nombre, const Matriz &d, int iteraciones, int semillas, double optimo) {
    cout << "== " << nombre << " | " << iteraciones << " iteraciones, " << semillas << " semillas ==\n";
    if (optimo > 0) cout << "Optimo exacto: " << optimo << "\n";
    cout << left << setw(26) << "Criterio" << setw(12) << "Promedio" << setw(10) << "Mejor"
         << setw(10) << "Peor" << "Veces optimo\n";
    cout << string(66, '-') << "\n";

    double probs[] = {0.0, 0.05};
    const char *nombres[] = {"Solo si mejora", "Acepta peor con 5 %"};
    for (int k = 0; k < 2; k++) {
        double suma = 0, mejor = INF, peor = 0;
        int aciertos = 0;
        for (int s = 1; s <= semillas; s++) {
            Resultado r = ils(d, iteraciones, s, probs[k]);
            suma += r.costoMejor;
            mejor = min(mejor, r.costoMejor);
            peor = max(peor, r.costoMejor);
            if (optimo > 0 && fabs(r.costoMejor - optimo) < 1e-6) aciertos++;
        }
        cout << left << setw(26) << nombres[k] << setw(12) << suma / semillas << setw(10) << mejor
             << setw(10) << peor;
        if (optimo > 0) cout << aciertos << "/" << semillas;
        else cout << "-";
        cout << "\n";
    }
    cout << "\n";
}

int main() {
    cout << fixed << setprecision(2);

    Matriz d12 = matrizDist(instancia12());
    comparar("TSP de 12 ciudades", d12, 20, 30, optimoHeldKarp(d12));

    Matriz d50 = matrizDist(generarPuntos(50, 2026, 100.0));
    comparar("TSP de 50 ciudades", d50, 200, 30, -1);
    return 0;
}