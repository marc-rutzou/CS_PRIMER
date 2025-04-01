package programming.higher_order_func_and_recursion.trampoline;

import java.util.function.Function;

public class Trampoline {
    public static void main(String[] args) {
        System.out.printf("%d%n", fact_t(1, 4));
        System.out.printf("%nOK%n");
    }

    public static int fact_r(int n) {
        if (n <= 1) return 1;
        return n * fact_r(n - 1);
    }

    public static int fact_i(int n) {
        int total = 1;
        for (int i = 1; i < n + 1; i++) {
            total *= i;
        }
        return total;
    }

    public static int fact_t(int total, int n) {
        if (n < 1) return total;
        return fact_t(total * n, n -1);
    }

    public static Function<Integer, Integer> tramponline(Function<Integer, Integer> f) {
        int total = 1;
        return n -> {
            while(n > 0) {
                total *= n;
                n--;
            }
            return total;
        };
    }
}
