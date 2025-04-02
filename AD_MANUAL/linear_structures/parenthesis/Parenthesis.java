package algos.linear_structures.parenthesis;

   

public class Parenthesis {
    private static String open = "([{";
    private static String close = ")]}";

    public static void main(String[] args) {
        String test = "[{()(( ))}]";
        String test_error = "([{ })]";
        String test_error2 = "(()";
        String test_error3 = "())";
        System.out.printf("%b%n", linter(test));

        System.out.printf("%nok%n");
    }

    public static boolean linter(String s) {
        Stack parentheses = new Stack();
        for (int i = 0; i < s.length(); i++) {
            parentheses.print();
            if (open.indexOf(s.charAt(i)) != -1) { // its an opening parenthesis
                parentheses.push(String.valueOf(s.charAt(i))); 
            } else if (close.indexOf(s.charAt(i)) != -1) {
                if (!parentheses.isEmpty() && String.valueOf(open.charAt(close.indexOf(s.charAt(i)))).equals(parentheses.top())) {
                    parentheses.pop();
                } else {
                    return false;
                }
            } else { // not a bracket -> skip
                continue;
            }
        }

        // if done iterating through and the stack is empty -> success
        if (parentheses.isEmpty()) { 
            return true;
        } else {
            return false;
        }
    }
}

class Stack {
    private static final int DEFAULT_CAPACITY = 100;
    private String[] data;
    private int top = -1;

    public Stack() { this(DEFAULT_CAPACITY); } // if nothing passed in, construct with default
    public Stack(int capacity) {
        data = new String[capacity];
    }
    
    public int size() { return (this.top + 1); }

    public boolean isEmpty() { return (this.top == -1); }

    public void push(String x) {
        if (this.size() == data.length) { throw new IllegalStateException("Stack is full"); }
        this.data[++this.top] = x;
    }

    public String pop() {
        // note that the value is not actually deleted (or set to 0) from the stack
        if (this.isEmpty()) { throw new IllegalStateException("Stack is empty"); }
        return this.data[this.top--];
    }

    public void print() {
        System.out.printf("%n");
        if (this.isEmpty()) { System.out.printf("Empty"); }
        for(int i = this.top; i >= 0; i--) {
            System.out.printf("%s%n", this.data[i]);
        }
        System.out.printf("%n");
    }

    public String top() {
        return this.data[this.top];
    }
}
