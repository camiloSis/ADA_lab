#include <iostream>
#include <iomanip>
#include <vector>
#include <string>
#include <algorithm>
using namespace std;
int main() {
    int n, presupuesto;
    cout << "Presupuesto disponible (entero, ej. soles): ";
    cin >> presupuesto;
    cout << "Cantidad de compras posibles: ";
    cin >> n;
    vector<string> nombre(n);
    vector<int> costo(n), beneficio(n);
    cin.ignore();
    for (int i = 0; i < n; i++) {
        cout << "Compra " << (i + 1) << " - nombre: ";
        getline(cin, nombre[i]);
        cout << "           costo y beneficio estimado (ej. 1200 8): ";
        cin >> costo[i] >> beneficio[i];
        cin.ignore();
    }
    vector<vector<int> > dp(n + 1, vector<int>(presupuesto + 1, 0));
    for (int i = 1; i <= n; i++) {
        for (int p = 0; p <= presupuesto; p++) {
            dp[i][p] = dp[i - 1][p];
            if (costo[i - 1] <= p)
                dp[i][p] = max(dp[i][p],
                               beneficio[i - 1] + dp[i - 1][p - costo[i - 1]]);
        }
    }
    vector<int> elegidas;
    int p = presupuesto;
    for (int i = n; i >= 1; i--) {
        if (dp[i][p] != dp[i - 1][p]) {
            elegidas.push_back(i - 1);
            p -= costo[i - 1];
        }
    }
    reverse(elegidas.begin(), elegidas.end());
    cout << "\n=== Plan de compras optimo ===\n";
    int gasto = 0;
    for (size_t k = 0; k < elegidas.size(); k++) {
        int j = elegidas[k];
        cout << " - " << left << setw(22) << nombre[j]
             << " costo " << setw(6) << costo[j]
             << " beneficio " << beneficio[j] << "\n";
        gasto += costo[j];
    }
    if (elegidas.empty()) cout << " (ninguna compra cabe en el presupuesto)\n";
    cout << "Gasto total: " << gasto << " de " << presupuesto
         << "   Sobrante: " << (presupuesto - gasto) << "\n";
    cout << "Beneficio total maximo: " << dp[n][presupuesto] << endl;
    return 0;
}
