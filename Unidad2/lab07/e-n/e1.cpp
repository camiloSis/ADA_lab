#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
int main() {
    int n, W;
    do {
        cout << "Cantidad de objetos (minimo 8): ";
        cin >> n;
    } while (n < 8);
    do {
        cout << "Capacidad de la mochila (W >= 0): ";
        cin >> W;
    } while (W < 0);
    vector<int> peso(n), valor(n);
    for (int i = 0; i < n; i++) {
        cout << "Objeto " << (i + 1) << " -> peso y valor: ";
        cin >> peso[i] >> valor[i];
    }
    vector<vector<int> > dp(n + 1, vector<int>(W + 1, 0));
    for (int i = 1; i <= n; i++) {
        for (int w = 0; w <= W; w++) {
            dp[i][w] = dp[i - 1][w];
            if (peso[i - 1] <= w) {
                dp[i][w] = max(dp[i][w], valor[i - 1] + dp[i - 1][w - peso[i - 1]]);
            }
        }
    }
    cout << "\nValor maximo (0/1): " << dp[n][W] << endl;
    vector<int> elegidos;
    int w = W;
    for (int i = n; i >= 1; i--) {
        if (dp[i][w] != dp[i - 1][w]) {
            elegidos.push_back(i);
            w -= peso[i - 1];
        }
    }
    reverse(elegidos.begin(), elegidos.end());
    cout << "Objetos elegidos:" << endl;
    int pesoTotal = 0, valorTotal = 0;
    for (size_t k = 0; k < elegidos.size(); k++) {
        int id = elegidos[k];
        cout << "  Objeto " << id << " (peso " << peso[id - 1]
             << ", valor " << valor[id - 1] << ")" << endl;
        pesoTotal += peso[id - 1];
        valorTotal += valor[id - 1];
    }
    cout << "Peso total: " << pesoTotal << " / " << W
         << "   Valor total: " << valorTotal << endl;
    return 0;
}
