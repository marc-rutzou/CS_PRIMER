package programming.objects_and_classes.diy_objects;

import java.util.function.Function;

public class DiyObjects {

    public static Function<Integer, Integer> make_vec(int x, int y) {
        return m -> {
            if (m == 0) {
                return x;
            } else {
                return y;
            }
        }; 
    }

    public static int getX(Function<Integer, Integer> v) {
        return v.apply(0); 
    }

    public static int getY(Function<Integer, Integer> v) {
        return v.apply(1); 
    }

    public static Function<Integer, Integer> add_vec(Function<Integer, Integer> v1, Function<Integer, Integer> v2){
        return make_vec(getX(v1) + getX(v2), getY(v1) + getY(v2));
    }

    public static Function<Integer, Integer> make_dis(int x, int y) {
        return make_vec(x, y);
    }

    public static Function<Integer, Integer> move(Function<Integer, Integer> dis, int velocity, int time) {
        return make_dis(getX(dis) + velocity * time, getY(dis) + velocity * time);
    }

   //TODO: how can I make sure that move can not be called on a vec?
    
    public static void main(String[] args) {
        Function<Integer, Integer> v1 = make_vec(1, 2);
        Function<Integer, Integer> v2 = make_vec(3, 4);

        System.out.printf("%d %d%n", getX(v1), getY(v1));

        Function<Integer, Integer> v3 = add_vec(v1, v2);
        System.out.printf("%d %d%n", getX(v3), getY(v3));

        Function<Integer, Integer> dis = make_dis(3, 2);
        Function<Integer, Integer> moved_dis = move(dis, 1, 5);
        // assert moved_dis == make_vec(8,7);
        System.out.printf("%d %d%n", getX(moved_dis), getY(moved_dis));
        

        System.out.println("ok");
    }
}
