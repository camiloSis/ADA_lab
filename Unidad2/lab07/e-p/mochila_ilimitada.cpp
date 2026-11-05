#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    vector<int> peso  = { 1, 2, 3 };
    vector<int> valor = { 2, 3, 4 };
    int n = peso.size();
    int W = 4;

    vector<int> dp(W + 1, 0); // B: dp[0] = 0

    for (int w = 1; w <= W; w++) {
        for (int i = 0; i < n; i++) {
            if (peso[i] <= w) {
                // R: se permite reutilizar el objeto i
                dp[w] = max(dp[w], valor[i] + dp[w - peso[i]]);
            }
        }
    }

    cout << "Valor maximo (ilimitada): " << dp[W] << endl;

    return 0;
}
