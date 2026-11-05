#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
int mochila2D(const vector<int>& peso, const vector<int>& valor, int W) {
    int n = peso.size();
    vector<vector<int> > dp(n + 1, vector<int>(W + 1, 0));
    for (int i = 1; i <= n; i++)
        for (int w = 0; w <= W; w++) {
            dp[i][w] = dp[i - 1][w];
            if (peso[i - 1] <= w)
                dp[i][w] = max(dp[i][w], valor[i - 1] + dp[i - 1][w - peso[i - 1]]);
        }
    return dp[n][W];
}
int mochila1D(const vector<int>& peso, const vector<int>& valor, int W) {
    int n = peso.size();
    vector<int> dp(W + 1, 0);
    for (int i = 0; i < n; i++) {
        for (int w = W; w >= peso[i]; w--)
            dp[w] = max(dp[w], valor[i] + dp[w - peso[i]]);
    }
    return dp[W];
}
int mochila1D_alReves(const vector<int>& peso, const vector<int>& valor, int W) {
    int n = peso.size();
    vector<int> dp(W + 1, 0);
    for (int i = 0; i < n; i++)
        for (int w = peso[i]; w <= W; w++)
            dp[w] = max(dp[w], valor[i] + dp[w - peso[i]]);
    return dp[W];
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
    int r2 = mochila2D(peso, valor, W);
    int r1 = mochila1D(peso, valor, W);
    int rMal = mochila1D_alReves(peso, valor, W);
    cout << "\nValor maximo con tabla 2D          : " << r2 << endl;
    cout << "Valor maximo con arreglo 1D (der->izq): " << r1 << endl;
    cout << "Valor con arreglo 1D (izq->der, MAL)   : " << rMal
         << (rMal != r1 ? "   <- distinto: reutiliza objetos" : "   (coincide en este caso)") << endl;
    cout << (r1 == r2 ? "Las versiones correctas coinciden.\n" : "ERROR: no coinciden.\n");
    long long mem2D = (long long)(n + 1) * (W + 1) * sizeof(int);
    long long mem1D = (long long)(W + 1) * sizeof(int);
    cout << "\nMemoria tabla 2D: (n+1)*(W+1) = " << (n + 1) << "*" << (W + 1)
         << " enteros = " << mem2D << " bytes" << endl;
    cout << "Memoria arreglo 1D: (W+1) = " << (W + 1)
         << " enteros = " << mem1D << " bytes" << endl;
    cout << "Ahorro: " << (n + 1) << " veces menos memoria (O(n*W) -> O(W))." << endl;
    cout << "Nota: con 1D se pierde la tabla completa, por lo que ya no se puede\n"
            "reconstruir facilmente que objetos se eligieron.\n";
    return 0;
}
