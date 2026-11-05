#include <iostream>
#include <vector>
#include <algorithm>
#include <climits>
#include <random>
#include <iomanip>
using namespace std;

const int NUM_TAREAS = 6;
const int NUM_LINEAS = 2;

int makespan(const vector<int> &duracion, const vector<int> &asignacion) {
    vector<int> carga(NUM_LINEAS, 0);
    for (int i = 0; i < NUM_TAREAS; i++)
        carga[asignacion[i]] += duracion[i];
    return *max_element(carga.begin(), carga.end());
}

void imprimirAsignacion(const vector<int> &duracion, const vector<int> &asignacion) {
    vector<int> carga(NUM_LINEAS, 0);
    for (int l = 0; l < NUM_LINEAS; l++) {
        cout << "  Linea " << l + 1 << ": ";
        for (int i = 0; i < NUM_TAREAS; i++)
            if (asignacion[i] == l) {
                cout << "T" << i + 1 << "(" << duracion[i] << "h) ";
                carga[l] += duracion[i];
            }
        cout << " -> termina a las " << carga[l] << " h\n";
    }
}

int main() {
    vector<int> duracion = {5, 3, 8, 2, 7, 4}; // horas de cada tarea
    int total = 0;
    for (int d : duracion) total += d;

    cout << "Tareas (horas): ";
    for (int i = 0; i < NUM_TAREAS; i++) cout << "T" << i + 1 << "=" << duracion[i] << " ";
    cout << "\nSuma total = " << total << " h  =>  cota inferior del makespan = "
         << (total + NUM_LINEAS - 1) / NUM_LINEAS << " h\n\n";

    // Busqueda aleatoria
    mt19937 rng(2026);
    uniform_int_distribution<int> lineaAlAzar(0, NUM_LINEAS - 1);

    const int ITERACIONES = 1000;
    int mejorMC = INT_MAX;
    vector<int> mejorAsignacion;

    cout << "Busqueda aleatoria (" << ITERACIONES << " iteraciones). Mejoras encontradas:\n";
    for (int it = 1; it <= ITERACIONES; it++) {
        vector<int> asignacion(NUM_TAREAS);
        for (int i = 0; i < NUM_TAREAS; i++)
            asignacion[i] = lineaAlAzar(rng);      // cada tarea va a una linea al azar

        int ms = makespan(duracion, asignacion);
        if (ms < mejorMC) {
            mejorMC = ms;
            mejorAsignacion = asignacion;
            cout << "  iteracion " << setw(4) << it << ": makespan = " << ms << " h\n";
        }
    }
    cout << "\nMejor asignacion encontrada (makespan " << mejorMC << " h):\n";
    imprimirAsignacion(duracion, mejorAsignacion);

        // Verificacion con fuerza bruta 
    int optimo = INT_MAX;
    long long total_asig = 1;
    for (int i = 0; i < NUM_TAREAS; i++) total_asig *= NUM_LINEAS;
    for (long long codigo = 0; codigo < total_asig; codigo++) {
        vector<int> asignacion(NUM_TAREAS);
        long long c = codigo;
        for (int i = 0; i < NUM_TAREAS; i++) { asignacion[i] = c % NUM_LINEAS; c /= NUM_LINEAS; }
        optimo = min(optimo, makespan(duracion, asignacion));
    }
    cout << "\nVerificacion por fuerza bruta (" << total_asig << " asignaciones): makespan optimo = "
         << optimo << " h\n";
    cout << (mejorMC == optimo ? "Monte Carlo encontro el optimo.\n"
                               : "Monte Carlo NO llego al optimo en esta corrida.\n");
    return 0;
}