#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>
#include <iomanip>
#include <string>
using namespace std;

int main() {
    const int N_MIN = 4, N_MAX = 25;

    vector<long double> fact(N_MAX + 1, 1.0L);
    for (int k = 1; k <= N_MAX; k++) fact[k] = fact[k - 1] * k;

    cout << left << setw(6) << "n" << setw(16) << "TSP (n-1)!/2" << setw(16) << "Asig. n!"
         << "Cociente (n!)/((n-1)!/2)\n";
    cout << string(64, '-') << "\n";

    vector<double> logTSP, logASIG;
    for (int n = N_MIN; n <= N_MAX; n++) {
        long double tsp = fact[n - 1] / 2.0L;
        long double asig = fact[n];
        logTSP.push_back((double)log10l(tsp));
        logASIG.push_back((double)log10l(asig));
        cout << left << setw(6) << n << setw(16) << scientific << setprecision(3) << (double)tsp
             << setw(16) << (double)asig << fixed << setprecision(0) << (double)(asig / tsp) << "\n";
    }

    // Grafica SVG 
    const int W = 900, H = 540, L = 90, R = 40, T = 60, B = 80;
    const int YMAX = 26;
    auto X = [&](int n) { return L + (double)(n - N_MIN) * (W - L - R) / (N_MAX - N_MIN); };
    auto Y = [&](double v) { return T + (H - T - B) * (1.0 - v / YMAX); };

    ofstream svg("crecimiento.svg");
    svg << "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 " << W << " " << H
        << "' font-family='sans-serif' font-size='13'>\n";
    svg << "<rect width='100%' height='100%' fill='white'/>\n";
    svg << "<text x='" << W / 2 << "' y='30' text-anchor='middle' font-size='18' font-weight='bold'>"
        << "Crecimiento del espacio de soluciones (escala logaritmica)</text>\n";

    // rejilla horizontal: cada 2 decadas
    for (int k = 0; k <= YMAX; k += 2) {
        double y = Y(k);
        svg << "<line x1='" << L << "' y1='" << y << "' x2='" << W - R << "' y2='" << y
            << "' stroke='#dddddd'/>\n";
        svg << "<text x='" << L - 8 << "' y='" << y + 4 << "' text-anchor='end'>10^" << k << "</text>\n";
    }
    // marcas del eje X
    for (int n = N_MIN; n <= N_MAX; n++) {
        svg << "<text x='" << X(n) << "' y='" << H - B + 22 << "' text-anchor='middle'>" << n << "</text>\n";
        svg << "<line x1='" << X(n) << "' y1='" << H - B << "' x2='" << X(n) << "' y2='" << H - B + 5
            << "' stroke='black'/>\n";
    }
    svg << "<line x1='" << L << "' y1='" << H - B << "' x2='" << W - R << "' y2='" << H - B << "' stroke='black'/>\n";
    svg << "<line x1='" << L << "' y1='" << T << "' x2='" << L << "' y2='" << H - B << "' stroke='black'/>\n";
    svg << "<text x='" << (L + W - R) / 2 << "' y='" << H - 25
        << "' text-anchor='middle'>n (ciudades o tareas)</text>\n";
    svg << "<text transform='translate(25," << (T + H - B) / 2
        << ") rotate(-90)' text-anchor='middle'>Numero de soluciones posibles</text>\n";

    auto polilinea = [&](const vector<double> &v, const string &color) {
        svg << "<polyline fill='none' stroke='" << color << "' stroke-width='2.5' points='";
        for (int i = 0; i < (int)v.size(); i++) svg << X(N_MIN + i) << "," << Y(v[i]) << " ";
        svg << "'/>\n";
        for (int i = 0; i < (int)v.size(); i++)
            svg << "<circle cx='" << X(N_MIN + i) << "' cy='" << Y(v[i]) << "' r='3.5' fill='" << color << "'/>\n";
    };
    polilinea(logTSP, "#1f77b4");
    polilinea(logASIG, "#e8710a");

    // leyenda
    svg << "<rect x='" << L + 15 << "' y='" << T + 8 << "' width='250' height='54' fill='white' stroke='#999'/>\n";
    svg << "<line x1='" << L + 25 << "' y1='" << T + 26 << "' x2='" << L + 55 << "' y2='" << T + 26
        << "' stroke='#1f77b4' stroke-width='3'/><text x='" << L + 62 << "' y='" << T + 30
        << "'>TSP: (n-1)!/2</text>\n";
    svg << "<line x1='" << L + 25 << "' y1='" << T + 48 << "' x2='" << L + 55 << "' y2='" << T + 48
        << "' stroke='#e8710a' stroke-width='3'/><text x='" << L + 62 << "' y='" << T + 52
        << "'>Asignacion de tareas: n!</text>\n";
    svg << "</svg>\n";
    svg.close();

    cout << "\nGrafica guardada en crecimiento.svg\n";
    return 0;
}