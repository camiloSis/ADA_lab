// Ejercicio 5: ruta de visita cerrada por 18 puntos emblemáticos de Arequipa con NN + 2-opt.
// Distancias Haversine (línea recta, en km), no por calles. Se valida contra el óptimo exacto (Held-Karp).
#include "tsp.h"

struct Lugar { const char* nombre; double lat, lon; };

// Coordenadas aproximadas (Wikipedia, Wikivoyage, Sygic). El índice 0 es el punto de partida de la presentación.
const vector<Lugar> LUGARES = {
    {"Plaza de Armas",                    -16.39880, -71.53690},
    {"Basílica Catedral",                 -16.39810, -71.53640},
    {"Monasterio de Santa Catalina",      -16.39500, -71.53667},
    {"Basílica y Convento de San Francisco", -16.39528, -71.53472},
    {"Iglesia de la Compañía",            -16.39992, -71.53657},
    {"Museo Santuarios Andinos",          -16.39982, -71.53779},
    {"Casa del Moral",                    -16.39694, -71.53778},
    {"Convento de Santo Domingo",         -16.40080, -71.53440},
    {"Iglesia de la Merced",              -16.40140, -71.53890},
    {"Mercado San Camilo",                -16.40304, -71.53495},
    {"Puente Bolognesi",                  -16.39779, -71.54137},
    {"Monasterio de la Recoleta",         -16.39419, -71.54167},
    {"Mirador de Yanahuara",              -16.38748, -71.54175},
    {"Cayma (plaza e iglesia)",           -16.38153, -71.54556},
    {"Puente de Fierro",                  -16.41041, -71.54810},
    {"Mirador de Sachaca",                -16.42533, -71.56695},
    {"Mansión del Fundador",              -16.45504, -71.56368},
    {"Molino de Sabandía",                -16.45654, -71.49963},
};

// Óptimo exacto por programación dinámica (Held-Karp): O(n² 2ⁿ), viable con n = 18; con la ciudad 0 fija.
double optimo(const Mat& d) {
    int m = d.size() - 1, N = 1 << m;
    vector<vector<double>> dp(N, vector<double>(m, 1e18));  // dp[S][j]: mínimo para visitar S terminando en j
    for (int j = 0; j < m; j++) dp[1 << j][j] = d[0][j + 1];
    for (int S = 1; S < N; S++)
        for (int j = 0; j < m; j++) {
            if (!((S >> j) & 1) || dp[S][j] > 1e17) continue;
            for (int k = 0; k < m; k++)
                if (!((S >> k) & 1)) dp[S | (1 << k)][k] = min(dp[S | (1 << k)][k], dp[S][j] + d[j + 1][k + 1]);
        }
    double mejor = 1e18;
    for (int j = 0; j < m; j++) mejor = min(mejor, dp[N - 1][j] + d[j + 1][0]);
    return mejor;
}

int main() {
    vector<pair<double, double>> pts;
    for (auto& l : LUGARES) pts.push_back({l.lat, l.lon});
    Instancia I = desdeCoordenadas(pts);
    int N = I.n;

    vector<Ruta> rutas(N);
    vector<double> despues(N);
    printf("%-3s %-38s %10s %12s\n", "#", "Origen de NN", "NN (km)", "NN+2opt (km)");
    for (int o = 0; o < N; o++) {
        Ruta nn = vecinoCercano(o, I.d);
        rutas[o] = dosOpt(nn, I.d);
        despues[o] = costo(rutas[o], I.d);
        printf("%-3d %-38s %10.3f %12.3f\n", o, LUGARES[o].nombre, costo(nn, I.d), despues[o]);
    }

    Resumen r = resumir(despues);
    printf("\nNN+2opt: mejor %.3f km | peor %.3f km | media %.3f km | mejor alcanzado desde %d/%d orígenes\n",
           r.mejor, r.peor, r.media, r.enMejor, N);

    // Ruta ganadora, rotada para que parta (y regrese) en la Plaza de Armas: en un ciclo cerrado rotar no cambia el costo.
    Ruta g = rutas[r.idxMejor];
    rotate(g.begin(), find(g.begin(), g.end(), 0), g.end());
    printf("\nRuta cerrada más corta encontrada (inicio y fin: %s):\n", LUGARES[0].nombre);
    double acum = 0;
    for (int i = 0; i < N; i++) {
        double tramo = I.d[g[i]][g[(i + 1) % N]];
        acum += tramo;
        printf("%2d. %-38s -> %-38s %6.3f km (acum. %6.3f)\n", i + 1, LUGARES[g[i]].nombre, LUGARES[g[(i + 1) % N]].nombre, tramo, acum);
    }

    vector<int> lista(N);
    iota(lista.begin(), lista.end(), 0);
    double base = costo(lista, I.d), opt = optimo(I.d);
    printf("\nOrden original de la lista: %.3f km | NN+2opt: %.3f km (%.1f%% menos)\n", base, r.mejor, 100 * (base - r.mejor) / base);
    printf("Óptimo exacto (Held-Karp): %.3f km | NN+2opt queda %.2f%% sobre el óptimo -> %s\n", opt, 100 * (r.mejor - opt) / opt,
           r.mejor - opt < 1e-6 ? "es óptima" : "no es óptima");
}