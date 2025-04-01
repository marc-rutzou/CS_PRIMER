package algos.poyla.correct_bs;

import java.util.Arrays;

public class CorrectBinarySearch {
    
    public static int bs(int x, int[] a, int i) {
        int  m = a.length / 2;
        // if all the way down to 1 value and it's not x, then return not found 
        if (a.length == 1 && a[m] != x) return -1;

        if (x == a[m]) {
            return m + i; 
        } else if (x < a[m]) {
            return bs(x, Arrays.copyOfRange(a, 0, m), i);
        } else {
            return bs(x, Arrays.copyOfRange(a, m+1, a.length), i + m + 1);
        }
    }

    public static void main(String[] args) {
        
        int[] a = {-6, -5, -3, 0, 4, 20, 27, 10001};
        assert bs(-3, a, 0) == 2;
        assert bs(-2, a, 0) == -1;
        assert bs(27, a, 0) == 6;
        assert bs(1000, a, 0) == -1;
       
        System.out.println("ok");
    }
}
