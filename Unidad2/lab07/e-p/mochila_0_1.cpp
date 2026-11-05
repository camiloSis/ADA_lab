#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    vector<int> peso  = { 1, 2, 3 };
    vector<int> valor = { 2, 3, 4 };
    int n = peso.size();
    int W = 4;

    vector<vector<int>> dp(n + 1, vector<int>(W + 1, 0)); // B: casos base en 0

    for (int i = 1; i <= n; i++) {
        for (int w = 0; w <= W; w++) {
            dp[i][w] = dp[i - 1][w]; // no se lleva el objeto i
            if (peso[i - 1] <= w) {
                // R: relación de recurrencia
                dp[i][w] = max(dp[i][w], valor[i - 1] + dp[i - 1][w - peso[i - 1]]);
            }
        }
    }

    cout << "Valor maximo (0/1): " << dp[n][W] << endl;

    // Reconstruir los objetos elegidos
    cout << "Objetos elegidos: ";
    int w = W;
    for (int i = n; i >= 1; i--) {
        if (dp[i][w] != dp[i - 1][w]) {
            cout << i << " ";
            w -= peso[i - 1];
        }
    }
    cout << endl;

    return 0;
}
