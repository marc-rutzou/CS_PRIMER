package programming.objects_and_classes.vector;

public class Vector {
    // initialized instance variables as zeros
    private int x;
    private int y;
    
    // constructor b/c no return type basically a enforcing setter
    public Vector(int x, int y) {
        this.x = x;
        this.y = y;
    }

    // instance method
    public int getX() {
        return this.x; // instance variable
    }

    public int getY() {
        return this.y;
    }

    // accessor method
    public static Vector add(Vector v1, Vector v2) {
        return new Vector(v1.x + v2.x, v1.y + v2.y);
    }

    // mutator method
    public void add(Vector v) {
        this.x += v.x;
        this.y += v.y;
    }

    public static boolean equal(Vector v1, Vector v2) {
        return v1.x == v2.x && v1.y == v2.y;
    }

    public boolean equals(Vector v) {
        return this.x == v.x && this.y == v.y;
    }

    public static void main(String[] args) {
        Vector v1 = new Vector(1, 2);
        Vector v2 = new Vector(3, 4);

        Vector v3 = Vector.add(v1, v2); 
        System.out.printf("%d %d%n", v3.getX(), v3.getY());

        v1.add(v2); // mutate v1
        System.out.printf("%d %d%n", v1.getX(), v1.getY());

        Vector v4 = new Vector(4, 6);
        System.out.printf("%b%n", Vector.equal(v1, v4));

        System.out.printf("%b%n", v1.equals(v4));

        System.out.println("ok");
    }
}

/*
- pass in object to method, so you can alter its instance variables, not the variable itself
- you can create a second constructor with only 1 parameter that calls the first constructor with a default 
    for the missing parameter
- v1.x = 2; I can set x as I like because main is in the class;
*/
