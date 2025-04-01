package programming.higher_order_func_and_recursion.recursion;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;
import java.util.stream.Stream;

interface Function {
    boolean apply(int x);
}

public class Recursion {
    public static void main(String[] args) {
        System.out.printf("%d%n", fact(5)); 
        System.out.printf("%b%n", palindrome("dadad")); 
        System.out.printf("%d%n", gcd(1071, 462)); 
        System.out.println(filter(x -> x > 0, new ArrayList<Integer>(Arrays.asList(-1, 1, -2, 2, 3))));
        System.out.println("ok"); 
    }

    public static int fact(int n) {
        if (n <= 1) return 1;
        return n * fact(n - 1);
    }

    public static boolean palindrome(String s) {
        if (s.length() <= 1) return true;
        return (s.charAt(0) == s.charAt(s.length() - 1) && palindrome(s.substring(1, s.length() - 1)));  
    }

    public static int gcd(int a, int b) {
        if (b == 0) return a;
        return gcd(b, a % b);
    }

    public static List<Integer> filter(Function func, List<Integer> xs) {
        if (xs.isEmpty()) return new ArrayList<>();
        if (func.apply(xs.get(0))) {
            return Stream.concat(Stream.of(xs.get(0)), filter(func, xs.subList(1, xs.size())).stream()).collect(Collectors.toList());
        } else {
            return filter(func, xs.subList(1, xs.size()));
        }
    }
}
