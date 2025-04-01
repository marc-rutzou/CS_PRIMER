package programming.higher_order_func_and_recursion.pretty_print;

import java.util.Arrays;
import java.util.List;

class PrettyPrint {
    public static void main(String[] args) {
        // Object is the root class
        List<Object> in = Arrays.asList(1, 2, 3, Arrays.asList(4, 5, Arrays.asList(6), 7), 8);
        pp(in, 0);
        System.out.printf("%nok%n");
    }

    public static void pp(List<Object> in, int indent) {
        for(Object elem : in){
            if (elem instanceof List) {
                // indent++;
                pp((List<Object>) elem, indent+1);
                // indent--;
            } else {
                System.out.print(".....".repeat(indent));
                System.out.print(elem);
                System.out.printf("%n");
            }
        }
    }
}
