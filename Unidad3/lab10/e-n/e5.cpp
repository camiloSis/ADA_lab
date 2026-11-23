// Ejercicio 5: ILS e IG sobre las 18 ubicaciones de Arequipa del laboratorio anterior
// (coordenadas reales, distancias Haversine en km). Usa el tsp.h del laboratorio 9, sin cambios.
// Las funciones de ILS e IG se escriben aqui, con el mismo estilo (Mat, Ruta, costo(r, d), dosOpt).
#include "tsp.h"

struct Lugar { const char* nombre; double lat, lon; };

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
    // --- Puntos adicionales (parte B). [V] = coordenada de una fuente en línea; [A] = aproximada, verificar ---
    {"Convento de Santa Teresa",              -16.39654, -71.53158},  // [V]
    {"Plaza de Chiguata",                     -16.40245, -71.39195},  // [V]
    {"Casa Tristan del Pozo",                 -16.39620, -71.53550},  // [A]
    {"Parque Selva Alegre",                   -16.39210, -71.52520},  // [A]
    {"Plaza de Miraflores",                   -16.39390, -71.52880},  // [A]
    {"Plaza de Mariano Melgar",               -16.40480, -71.51850},  // [A]
    {"Plaza de Jose Luis Bustamante y Rivero",-16.41950, -71.53200},  // [A]
    {"Plaza de Alto Selva Alegre",            -16.38300, -71.51600},  // [A]
    {"Plaza de Cerro Colorado",               -16.36400, -71.57400},  // [A]
    {"Plaza de Jacobo Hunter",                -16.44300, -71.52900},  // [A]
    {"Plaza de Paucarpata",                   -16.42100, -71.51300},  // [A]
    {"Plaza de Socabaya",                     -16.45500, -71.53400},  // [A]
    {"Plaza de Tiabaya",                      -16.44400, -71.58700},  // [A]
    {"Plaza de Sachaca",                      -16.42090, -71.56390},  // [A]
    {"Plaza de Characato",                    -16.46750, -71.48620},  // [A]
    {"Plaza de Yura",                         -16.24670, -71.68380},  // [A]
    {"Plaza de Uchumayo",                     -16.43720, -71.66480},  // [A]
    {"Plaza de Quequeña",                     -16.56010, -71.44530},  // [A]
    {"Plaza de Yarabamba",                    -16.55090, -71.48330},  // [A]
    {"Aeropuerto Rodriguez Ballon",           -16.34110, -71.58310},  // [A]
};

// Cantidad de lugares originales: la parte A usa solo los primeros N_BASE (Held-Karp no soporta más).
const int N_BASE = 18;

// Optimo exacto (Held-Karp), igual que en el laboratorio 9.
double optimo(const Mat& d) {
    int m = d.size() - 1, N = 1 << m;
    vector<vector<double>> dp(N, vector<double>(m, 1e18));
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

struct Res { Ruta ruta; double c; int iter; };  // mejor ruta, su costo e iteracion en que aparecio (0 = inicial)

// ---- ILS: perturbacion double-bridge + 2-opt, aceptacion estricta ----
Ruta doubleBridge(const Ruta& r, mt19937& g) {
    int n = r.size(), p[3];
    do {
        for (int k = 0; k < 3; k++) p[k] = 1 + g() % (n - 1);
        sort(p, p + 3);
    } while (p[0] == p[1] || p[1] == p[2]);
    Ruta s(r.begin(), r.begin() + p[0]);                 // A
    s.insert(s.end(), r.begin() + p[1], r.begin() + p[2]); // C
    s.insert(s.end(), r.begin() + p[0], r.begin() + p[1]); // B
    s.insert(s.end(), r.begin() + p[2], r.end());          // D
    return s;
}

Res ils(const Mat& d, Ruta act, int iters, unsigned semilla) {
    mt19937 g(semilla);
    double ca = costo(act, d);
    Res R{act, ca, 0};
    for (int it = 1; it <= iters; it++) {
        Ruta c = dosOpt(doubleBridge(act, g), d);
        double cc = costo(c, d);
        if (cc < ca - EPS) { act = c; ca = cc; R = {act, ca, it}; }  // solo si mejora
    }
    return R;
}

// ---- IG: destruir k ciudades y reinsertarlas en la posicion que menos aumenta el costo ----
Res ig(const Mat& d, Ruta act, int iters, unsigned semilla, int k) {
    mt19937 g(semilla);
    double ca = costo(act, d);
    Res R{act, ca, 0};
    for (int it = 1; it <= iters; it++) {
        Ruta c = act;
        vector<int> quitadas;
        for (int t = 0; t < k; t++) {
            int pos = g() % c.size();
            quitadas.push_back(c[pos]);
            c.erase(c.begin() + pos);
        }
        for (int x : quitadas) {
            int m = c.size(), pos = 0;
            double mejor = 1e18;
            for (int i = 0; i < m; i++) {
                int a = c[i], b = c[(i + 1) % m];
                double delta = d[a][x] + d[x][b] - d[a][b];
                if (delta < mejor) mejor = delta, pos = i + 1;
            }
            c.insert(c.begin() + pos, x);
        }
        double cc = costo(c, d);
        if (cc < ca - EPS) { act = c; ca = cc; R = {act, ca, it}; }
    }
    return R;
}

void imprimirRuta(const Ruta& r0, const Mat& d) {
    Ruta g = r0;
    rotate(g.begin(), find(g.begin(), g.end(), 0), g.end());  // parte y regresa en la Plaza de Armas
    int N = g.size();
    double acum = 0;
    for (int i = 0; i < N; i++) {
        double tramo = d[g[i]][g[(i + 1) % N]];
        acum += tramo;
        printf("%2d. %-38s -> %-38s %6.3f km (acum. %6.3f)\n", i + 1, LUGARES[g[i]].nombre,
               LUGARES[g[(i + 1) % N]].nombre, tramo, acum);
    }
}


// ---------------- PARTE B: mas nodos (todo LUGARES) ----------------
// Con tantos puntos ya no se puede calcular el optimo exacto (Held-Karp), asi que se compara
// entre metodos: NN, NN + 2-opt, ILS e IG (con varios k), en costo y tiempo.
double msDesde(chrono::steady_clock::time_point t0) {
    return chrono::duration<double, milli>(chrono::steady_clock::now() - t0).count();
}

void parteB() {
    const int ITER = 500, SEMILLAS = 10;
    const int VALORES_K[] = {2, 3, 5, 8};

    vector<pair<double, double>> pts;
    for (auto& l : LUGARES) pts.push_back({l.lat, l.lon});
    Instancia I = desdeCoordenadas(pts);
    int N = I.n;

    printf("\n\n==================== PARTE B: %d ubicaciones (%d originales + %d adicionales) ====================\n",
           N, N_BASE, N - N_BASE);
    printf("Sin optimo exacto (N demasiado grande para Held-Karp). %d iteraciones, %d semillas.\n\n", ITER, SEMILLAS);

    auto t0 = chrono::steady_clock::now();
    Ruta nn0 = vecinoCercano(0, I.d);
    double tNN = msDesde(t0), cNN = costo(nn0, I.d);

    t0 = chrono::steady_clock::now();
    Ruta ini = dosOpt(vecinoCercano(0, I.d), I.d);
    double t2 = msDesde(t0), c2 = costo(ini, I.d);

    vector<double> nn2(N);
    for (int o = 0; o < N; o++) nn2[o] = costo(dosOpt(vecinoCercano(o, I.d), I.d), I.d);
    Resumen rn = resumir(nn2);

    printf("%-26s %12s %14s %14s\n", "Metodo", "Costo medio", "Mejor (km)", "Tiempo (ms)");
    printf("%-26s %12.3f %14.3f %14.3f\n", "NN (desde Plaza de Armas)", cNN, cNN, tNN);
    printf("%-26s %12.3f %14.3f %14.3f\n", "NN+2opt (Plaza de Armas)", c2, c2, t2);
    printf("%-26s %12.3f %14.3f %14s\n", "NN+2opt (mejor de N orig.)", rn.media, rn.mejor, "-");

    auto correr = [&](const char* nombre, auto&& f) {
        vector<double> c;
        double tms = 0;
        for (int s = 1; s <= SEMILLAS; s++) {
            auto t = chrono::steady_clock::now();
            c.push_back(f(s).c);
            tms += msDesde(t);
        }
        Resumen r = resumir(c);
        printf("%-26s %12.3f %14.3f %14.3f   (peor %.3f)\n", nombre, r.media, r.mejor, tms / SEMILLAS, r.peor);
        return r;
    };

    correr("ILS", [&](int s) { return ils(I.d, ini, ITER, s); });
    for (int k : VALORES_K) {
        char nombre[40];
        snprintf(nombre, sizeof nombre, "IG (k = %d)", k);
        correr(nombre, [&](int s) { return ig(I.d, ini, ITER, s, k); });
    }
}

int main() {
    const int ITER = 200, SEMILLAS = 10, K_IG = 3;

    vector<pair<double, double>> pts;
    for (int i = 0; i < N_BASE; i++) pts.push_back({LUGARES[i].lat, LUGARES[i].lon});
    Instancia I = desdeCoordenadas(pts);
    int N = I.n;
    double opt = optimo(I.d);

    // --- Referencias: solo Nearest Neighbor y NN + 2-opt (como en el laboratorio 9) ---
    Ruta nn0 = vecinoCercano(0, I.d);
    double cNN0 = costo(nn0, I.d);
    Ruta ini = dosOpt(nn0, I.d);               // punto de partida de ILS e IG: NN(0) + 2-opt
    double cIni = costo(ini, I.d);
    vector<double> nn2(N);
    for (int o = 0; o < N; o++) nn2[o] = costo(dosOpt(vecinoCercano(o, I.d), I.d), I.d);
    Resumen rn = resumir(nn2);

    printf("%d ubicaciones de Arequipa | distancias Haversine (km)\n", N);
    printf("Optimo exacto (Held-Karp):                  %.3f km\n", opt);
    printf("Solo Nearest Neighbor (desde Plaza de Armas): %.3f km\n", cNN0);
    printf("NN + 2-opt (desde Plaza de Armas):            %.3f km\n", cIni);
    printf("NN + 2-opt (mejor de los %d origenes):        %.3f km\n\n", N, rn.mejor);

    // --- ILS e IG con varias semillas ---
    vector<double> cI, cG;
    Res mejorI{ini, 1e18, 0}, mejorG{ini, 1e18, 0};
    int optI = 0, optG = 0;
    printf("ILS e IG (%d iteraciones, IG con k = %d), %d semillas\n", ITER, K_IG, SEMILLAS);
    printf("%-8s %12s %10s   %12s %10s\n", "Semilla", "ILS (km)", "iter.", "IG (km)", "iter.");
    for (int s = 1; s <= SEMILLAS; s++) {
        Res a = ils(I.d, ini, ITER, s), b = ig(I.d, ini, ITER, s, K_IG);
        cI.push_back(a.c); cG.push_back(b.c);
        if (a.c < mejorI.c) mejorI = a;
        if (b.c < mejorG.c) mejorG = b;
        optI += a.c - opt < 1e-6;
        optG += b.c - opt < 1e-6;
        printf("%-8d %12.3f %10d   %12.3f %10d\n", s, a.c, a.iter, b.c, b.iter);
    }
    Resumen ri = resumir(cI), rg = resumir(cG);
    printf("\n%-6s mejor %.3f | media %.3f | peor %.3f | llega al optimo en %d/%d semillas\n", "ILS", ri.mejor, ri.media, ri.peor, optI, SEMILLAS);
    printf("%-6s mejor %.3f | media %.3f | peor %.3f | llega al optimo en %d/%d semillas\n", "IG", rg.mejor, rg.media, rg.peor, optG, SEMILLAS);

    // --- Ruta final: la mejor encontrada entre ILS e IG (empate -> ILS) ---
    bool daILS = mejorI.c <= mejorG.c + EPS;
    const Res& M = daILS ? mejorI : mejorG;
    printf("\nRuta cerrada mas corta encontrada (%s, inicio y fin: %s):\n", daILS ? "ILS" : "IG", LUGARES[0].nombre);
    imprimirRuta(M.ruta, I.d);
    printf("\nCosto: %.3f km | Solo NN: %.3f km (%.1f%% menos) | NN+2opt: %.3f km (%.1f%% menos) | optimo: %.3f km\n",
           M.c, cNN0, 100 * (cNN0 - M.c) / cNN0, cIni, 100 * (cIni - M.c) / cIni, opt);
    parteB();
    return 0;
}