#include <bits/stdc++.h>
using namespace std;
#define int long long
int32_t main() {
    int q, k;
    cin >> q >> k;
    vector<pair<int, int>> tasks;
    while (q--) {
        int qt; cin >> qt;
        if (qt == 1) {
            int t, v; cin >> t >> v;
            tasks.push_back({t, v});
        } else {
            int t;
            cin >> t;
            int ans = 0;
            for (auto [tt, v] : tasks) {
                if (tt < t - k) continue;
                ans += v;
            }
            cout << ans << "\n";
        }
    }
    return 0;
}