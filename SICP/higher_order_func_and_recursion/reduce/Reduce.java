package programming.higher_order_func_and_recursion.reduce;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Reduce {
    public static void main(String args[]) {
        List<Integer> xs = new ArrayList<Integer>(Arrays.asList(1, 2, 3, 4));
        int result = Reduce((x, y) -> x + y, xs, 0);
        System.out.printf("result: %d%n", result);
        System.out.println("ok");
    }

    public static int Reduce(Accumulate accumulator, List<Integer> xs, int initial) {
        if (xs.isEmpty()) {
            return initial;
        } else {
            return accumulator.operation(xs.get(0), Reduce(accumulator, xs.subList(1, xs.size()), initial));
        }
    }
}

