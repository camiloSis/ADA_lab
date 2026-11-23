// Ejercicio 1: ILS con 10 semillas (1 a 10) sobre el TSP de 12 ciudades.
// Para cada semilla: costo final e iteracion en que se encontro la mejor ruta.
#include <iostream>
#include <iomanip>
#include <cmath>
#include "tsp_meta.h"
using namespace std;

int main() {
    const int ITERACIONES = 100;
    const int SEMILLAS = 10;

    Matriz d = matrizDist(instancia12());
    double optimo = optimoHeldKarp(d);

    Ruta nn = vecinoMasCercano(d);
    Ruta nn2 = nn;
    dosOpt(d, nn2);

    cout << fixed << setprecision(2);
    cout << "Optimo exacto (Held-Karp): " << optimo << "\n";
    cout << "Nearest Neighbor:          " << costo(d, nn) << "\n";
    cout << "NN + 2-opt (inicio ILS):   " << costo(d, nn2) << "\n\n";

    cout << "ILS con " << ITERACIONES << " iteraciones, aceptacion estricta\n";
    cout << left << setw(9) << "Semilla" << setw(13) << "Costo final"
         << setw(20) << "Iteracion hallada" << "Llego al optimo\n";
    cout << string(60, '-') << "\n";

    int aciertos = 0;
    for (int s = 1; s <= SEMILLAS; s++) {
        Resultado r = ils(d, ITERACIONES, s);
        bool opt = fabs(r.costoMejor - optimo) < 1e-6;
        if (opt) aciertos++;
        cout << left << setw(9) << s << setw(13) << r.costoMejor
             << setw(20) << r.iterMejor << (opt ? "SI" : "no") << "\n";
    }
    cout << "\nSemillas que llegan al optimo: " << aciertos << " de " << SEMILLAS << "\n";
    return 0;
}