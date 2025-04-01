package programming.introduction.luhn;

public class Luhn {

    public static boolean verify(long x) {
        int check_digit = (int) (x % 10);
        long p = x / 10;
        int sum = 0;
        int mult = 2;
        int delta = -1;

        while (p != 0) {
            int n = ((int) p % 10) * mult;  
            p = p / 10;

            mult = mult + delta;
            delta *= -1;
            sum += n / 10 + n % 10; // this also works for single digits
        }
        return check_digit == 10 - (sum % 10);
    }

    public static void main(String[] args) {
        long input = 17893729974L;
        System.out.printf("%b%n", verify(input)); 
    }    
}
