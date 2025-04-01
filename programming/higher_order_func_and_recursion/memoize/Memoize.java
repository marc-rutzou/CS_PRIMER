package programming.higher_order_func_and_recursion.memoize;

import java.util.ArrayList;
import java.util.List;
import java.util.function.Function;
import java.util.HashMap;
import java.util.Map;

public class Memoize {
    private static ArrayList<Integer> cache_list = new ArrayList<Integer>();


    public static void main(String[] args) {
        Function<Integer, Integer>[] memoizedFib = new Function[1];

        memoizedFib[0] = memoize(n -> {
            if (n <= 1) return n;
            return memoizedFib[0].apply(n - 1) + memoizedFib[0].apply(n - 2);
        });

        int result = memoizedFib[0].apply(35);
        System.out.println("Fibonacci of 35 is: " + result);
    }


    public static <T, R> Function<T, R> memoize(Function<T, R> fn) {
        Map<T, R> cache = new HashMap<>();
        return arg -> {
            if (cache.containsKey(arg)) {
                return cache.get(arg);
            } else {
                R result = fn.apply(arg);
                cache.put(arg, result);
                return result;
            }
        };
    }
}
