#include <iostream>
#include <cassert>

int exp(int x, int a) {
    if (a == 1) return x;
    int ans = exp(x, a/2);
    if (a % 2 == 0) return ans * ans;
    return x * ans * ans;
}

int i_exp(int x, int a) {
    /*
    3^8 
    */
    for (int i = 0; i < log(a); i++
}

int main() {
    int x = 5;
    int a = 10;
    assert(exp(x, a) == 9765625);
    std::cout << "\nok\n";
}
