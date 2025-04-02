package algos.divide_conquer.merge_sort;

import java.util.Arrays;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class MergeSort {

    public static void merge(int[] xs, int[] out, int[] idx_store, int left_l, int left_r, int right_l, int right_r) {
        int idx = idx_store[0];
        while (left_l < left_r && right_l < right_r) {
            if (xs[left_l] < xs[right_l]) {
                out[idx++] = xs[left_l++];
            } else if (xs[right_l] < xs[left_l]) {
                out[idx++] = xs[right_l++];
            } else {
                out[idx++] = xs[left_l++];
                out[idx++] = xs[right_l++];
            }
        }
        while (left_l < left_r) { out[idx++] = xs[left_l++]; }
        while (right_l < right_r) { out[idx++] = xs[right_l++]; }
        idx_store[0] = idx;
    }

    public static int[] merge_sort(int[] xs) {
        int[] out = new int[xs.length]; // only 1 copy
        int right_l = 0, right_r = 0, left_l = 0, left_r = 0;

        int[] idx_store = {0}; // cannot change int from inside function, b/c passed by value
        for (int i = 1; i < xs.length; i *= 2) {
        // loop over levels of tree
            boolean y = false;
            for (int j = 0; j < xs.length; j += i) {
            // loop over nodes at level
                if (y) { 
                    right_l = j;
                    right_r = Math.min(i + j, xs.length);
                    merge(xs, out, idx_store, left_l, left_r, right_l, right_r);
                } else {
                    left_l = j;
                    left_r = Math.min(i + j, xs.length);
                }
                y = !y;
            }
            idx_store[0] = 0;
            // dont let out point to new array (out = new int[]) b/c then you leave unused space for whatever xs pointed to
            int[] temp = xs; // new pointer to xs
            xs = out; // xs points to the old out
            out = temp; // out points to old xs
            }
        return xs;
    }

    public static void main(String[] args) {
        int[] in = {4, 8, 2, 1, 3, 9, 7, 5};
        int[] out = merge_sort(in);

        for (int elem : out) {
            System.out.printf("%d ", elem);
        }

        System.out.printf("%nok%n");
    }
}
