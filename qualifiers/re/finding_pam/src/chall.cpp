#include <bits/stdc++.h>
using namespace std;

const int mapping[] = { // 33 to 126
    4238, 5582, 5612, 8108, 4354, 7281, 7639, 2195, 8047, 4234,
    7354, 4783, 6308, 6192, 1978, 1861, 5404, 9029, 9328, 3400,
    9749, 2680, 7004, 2763, 9859, 2487, 1959, 5739, 7276, 6843,
    6210, 3363, 3807, 2172, 2255, 7310, 9559, 7998, 9340, 6895,
    6312, 6851, 1769, 3600, 1637, 5260, 9764, 9451, 6332, 7953,
    3732, 5529, 3171, 7674, 3377, 5904, 7090, 6747, 3349, 6816,
    3503, 1417, 7149, 6561, 5373, 9670, 3602, 2847, 8164, 7985,
    2203, 9046, 6894, 7513, 1452, 4759, 9263, 5134, 7334, 2651,
    6427, 6725, 1012, 1497, 9920, 1250, 8918, 6796, 6819, 4426,
    5115, 7109, 7653, 1019
};

const int password[] = {
    1012, 3602, 1497, 7985, 5115, 9749, 1861, 9263, 9328, 1861, 5134,
    9328, 7149, 2203, 5404, 1250, 9328, 7149, 7004, 9046, 5404, 9749,
    7149, 2203, 9920, 6819, 7149, 3400, 7149, 9263, 3400, 2651, 7653
};

int main() {
    cout << "Enter password: ";

    string input;
    getline(cin, input);

    // map
    vector<int> mapped;
    for (char c : input) {
        if (c < 33 || c > 126) {
            cout << "Illegal character detected\n";
            return 0;
        }
        mapped.push_back(mapping[c - 33]);
    }

    bool correct = ((int) mapped.size() == 33);
    for (size_t i = 0; i < mapped.size(); i++) {
        if (i < 33 && mapped[i] != password[i]) {
            correct = false;
        }
    }
    cout << "\n";

    if (!correct) {
        cout << "Wrong password lil bro\n";
    } else {
        cout << "Oh shi u got it congrats lil bro\n";
    }
    return 0;
}
