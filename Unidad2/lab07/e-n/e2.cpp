#include <iostream>
#include <vector>
#include <algorithm>
#include <climits>
using namespace std;
int main() {
    int n, M;
    cout << "Cantidad de denominaciones: ";
    cin >> n;
    vector<int> monedas(n);
    cout << "Ingrese las denominaciones (enteros positivos): ";
    for (int i = 0; i < n; i++) cin >> monedas[i];
    cout << "Monto objetivo: ";
    cin >> M;
    const int INF = INT_MAX / 2;
    vector<int> dp(M + 1, INF);
    dp[0] = 0;
    vector<int> eleccion(M + 1, -1);
    for (int m = 1; m <= M; m++) {
        for (int i = 0; i < n; i++) {
            int c = monedas[i];
            if (c <= m && dp[m - c] != INF) {
                if (1 + dp[m - c] < dp[m]) {
                    dp[m] = 1 + dp[m - c];
                    eleccion[m] = c;
                }
            }
        }
    }
    if (dp[M] == INF) {
        cout << "No es posible formar el monto " << M << " con esas monedas." << endl;
        return 0;
    }
    cout << "\nMinimo de monedas: " << dp[M] << endl;
    cout << "Combinacion: ";
    vector<int> usadas;
    int m = M;
    while (m > 0) {
        usadas.push_back(eleccion[m]);
        m -= eleccion[m];
    }
    sort(usadas.begin(), usadas.end(), greater<int>());
    for (size_t k = 0; k < usadas.size(); k++) {
        cout << usadas[k];
        if (k + 1 < usadas.size()) cout << " + ";
    }
    cout << " = " << M << endl;
    return 0;
}
