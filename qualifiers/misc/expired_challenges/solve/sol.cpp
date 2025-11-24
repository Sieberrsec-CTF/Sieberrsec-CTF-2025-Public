#include <bits/stdc++.h>

using namespace std;

int main() {
    ios_base::sync_with_stdio(0);
    cin.tie(0);

    int q, k;
    cin >> q >> k;

    long long ans = 0;
    queue<pair<int, int>> qu;

    while (q--) {
        int qt;
        cin >> qt;

        if (qt == 1) {
            int t, v;
            cin >> t >> v;

            ans += (long long) v;
            qu.push({t, v});
        } else if (qt == 2) {
            int t;
            cin >> t;

            while (!qu.empty() && qu.front().first < t - k) {
                ans -= (long long) qu.front().second;
                qu.pop();
            }

            cout << ans << "\n";
        }
    }

    return 0;
}
