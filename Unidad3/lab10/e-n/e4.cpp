#include <iostream>
#include <iomanip>
#include <chrono>
#include <string>
#include <sstream>
#include "tsp_meta.h"
using namespace std;
using Reloj = chrono::steady_clock;

string f(double v, int prec) {
    ostringstream o;
    o << fixed << setprecision(prec) << v;
    return o.str();
}

double ms(Reloj::time_point a, Reloj::time_point b) {
    return chrono::duration<double, milli>(b - a).count();
}

int main() {
    const int N = 50, ITER = 500, D_IG = 3, SEMILLAS = 10;
    Matriz d = matrizDist(generarPuntos(N, 2026, 100.0));

    auto t0 = Reloj::now();
    Ruta nn = vecinoMasCercano(d);
    auto t1 = Reloj::now();
    double cNN = costo(d, nn), tNN = ms(t0, t1);

    t0 = Reloj::now();
    Ruta nn2 = vecinoMasCercano(d);
    dosOpt(d, nn2);
    t1 = Reloj::now();
    double cNN2 = costo(d, nn2), tNN2 = ms(t0, t1);

    t0 = Reloj::now();
    Resultado rils = ils(d, ITER, 1);
    t1 = Reloj::now();
    double tILS = ms(t0, t1);

    t0 = Reloj::now();
    Resultado rig = ig(d, ITER, 1, D_IG);
    t1 = Reloj::now();
    double tIG = ms(t0, t1);

    cout << fixed << setprecision(2);
    cout << "TSP aleatorio de " << N << " ciudades (semilla 2026). ILS e IG: " << ITER
         << " iteraciones, semilla 1, IG con d = " << D_IG << "\n\n";
    cout << left << setw(14) << "Metodo" << setw(11) << "Costo" << setw(14) << "Tiempo (ms)"
         << setw(20) << "Mejora vs NN+2opt" << "Tiempo vs NN+2opt\n";
    cout << string(75, '-') << "\n";

    auto fila = [&](const string &n, double c, double t) {
        cout << left << setw(14) << n << setw(11) << f(c, 2) << setw(14) << f(t, 3)
             << setw(20) << (f((cNN2 - c) * 100.0 / cNN2, 2) + " %")
             << "x" << f(t / tNN2, 1) << "\n";
    };
    fila("NN", cNN, tNN);
    fila("NN + 2-opt", cNN2, tNN2);
    fila("ILS", rils.costoMejor, tILS);
    fila("IG", rig.costoMejor, tIG);

    double sIls = 0, sIg = 0, tIls = 0, tIg = 0;
    for (int s = 1; s <= SEMILLAS; s++) {
        t0 = Reloj::now();
        sIls += ils(d, ITER, s).costoMejor;
        tIls += ms(t0, Reloj::now());
        t0 = Reloj::now();
        sIg += ig(d, ITER, s, D_IG).costoMejor;
        tIg += ms(t0, Reloj::now());
    }
    cout << "\nPromedio de " << SEMILLAS << " semillas (1 a " << SEMILLAS << "):\n";
    cout << left << setw(14) << "Metodo" << setw(14) << "Costo prom." << setw(20) << "Tiempo prom. (ms)"
         << "Mejora vs NN+2opt\n";
    cout << string(66, '-') << "\n";
    cout << left << setw(14) << "ILS" << setw(14) << f(sIls / SEMILLAS, 2) << setw(20) << f(tIls / SEMILLAS, 3)
         << f((cNN2 - sIls / SEMILLAS) * 100.0 / cNN2, 2) << " %\n";
    cout << left << setw(14) << "IG" << setw(14) << f(sIg / SEMILLAS, 2) << setw(20) << f(tIg / SEMILLAS, 3)
         << f((cNN2 - sIg / SEMILLAS) * 100.0 / cNN2, 2) << " %\n";
    return 0;
}