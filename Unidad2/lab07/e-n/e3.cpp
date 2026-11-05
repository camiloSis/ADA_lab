#include <iostream>
#include <iomanip>
#include <vector>
#include <algorithm>
using namespace std;
void imprimirTabla(const vector<vector<int> >& dp, int n, int W) {
    cout << "\nTabla dp[i][w]  (fila i = \"puedo usar los objetos 1..i\")\n";
    cout << "        ";
    for (int w = 0; w <= W; w++) cout << setw(4) << ("w=" + to_string(w));
    cout << "\n";
    for (int i = 0; i <= n; i++) {
        if (i == 0) cout << "i=0 (-) ";
        else        cout << "i=" << i << " obj" << i << " ";
        for (int w = 0; w <= W; w++) cout << setw(4) << dp[i][w];
        cout << "\n";
    }
}
int main() {
    int n, W;
    cout << "Cantidad de objetos: ";
    cin >> n;
    cout << "Capacidad de la mochila: ";
    cin >> W;
    vector<int> peso(n), valor(n);
    for (int i = 0; i < n; i++) {
        cout << "Objeto " << (i + 1) << " -> peso y valor: ";
        cin >> peso[i] >> valor[i];
    }
    vector<vector<int> > dp(n + 1, vector<int>(W + 1, 0));
    for (int i = 1; i <= n; i++) {
        for (int w = 0; w <= W; w++) {
            dp[i][w] = dp[i - 1][w];
            if (peso[i - 1] <= w)
                dp[i][w] = max(dp[i][w],
                               valor[i - 1] + dp[i - 1][w - peso[i - 1]]);
        }
    }
    imprimirTabla(dp, n, W);
    cout << "\nValor maximo = dp[" << n << "][" << W << "] = " << dp[n][W] << "\n";
    cout << "\nReconstruccion (se parte de la esquina dp[" << n << "][" << W << "] y se sube):\n";
    int w = W;
    vector<int> elegidos;
    for (int i = n; i >= 1; i--) {
        cout << "  dp[" << i << "][" << w << "] = " << dp[i][w]
             << "  vs  dp[" << (i - 1) << "][" << w << "] = " << dp[i - 1][w];
        if (dp[i][w] != dp[i - 1][w]) {
            cout << "  -> son DISTINTOS: se llevo el objeto " << i
                 << " (peso " << peso[i - 1] << "), capacidad pasa de "
                 << w << " a " << (w - peso[i - 1]) << "\n";
            elegidos.push_back(i);
            w -= peso[i - 1];
        } else {
            cout << "  -> son IGUALES: NO se llevo el objeto " << i << "\n";
        }
    }
    reverse(elegidos.begin(), elegidos.end());
    cout << "\nObjetos elegidos: ";
    if (elegidos.empty()) cout << "(ninguno)";
    for (size_t k = 0; k < elegidos.size(); k++) cout << elegidos[k] << " ";
    cout << endl;
    return 0;
}
