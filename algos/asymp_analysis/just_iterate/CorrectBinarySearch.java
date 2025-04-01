package algos.asymp_analysis.just_iterate;

import java.util.Arrays;
import java.util.Random;
import java.lang.Math;
import org.knowm.xchart.XYChart;
import org.knowm.xchart.XYChartBuilder;
import org.knowm.xchart.SwingWrapper;
import org.knowm.xchart.style.markers.SeriesMarkers;


public class CorrectBinarySearch {
    
    public static int bs(int x, int[] a, int i) {
        int  m = a.length / 2;
        // if all the way down to 1 value and it's not x, then return not found 
        if ((m == 0) || (a.length == 1 && a[m] != x)) return -1;

        if (x == a[m]) {
            return m + i; 
        } else if (x < a[m]) {
            return bs(x, Arrays.copyOfRange(a, 0, m), i);
        } else {
            return bs(x, Arrays.copyOfRange(a, m+1, a.length), i + m + 1);
        }
    }

    public static int bs2(int x, int[] a, int left, int right) {
        if (left > right) {
            return -1;
        }
        int m = left + (right - left) / 2;

        if (x == a[m]) {
            return m;
        } else if (x < a[m]) {
            return bs2(x, a, left, m - 1);
        } else {
            return bs2(x, a, m + 1, right);
        }
    }

    public static int is(int x, int[] a) {
        for (int i = 0; i < a.length; i++) {
            if (x == a[i]) return i;
        }
        return -1;
    }

    public static int[] generate_random_array(int n) {
        Random random = new Random();
        random.setSeed(1);
        
        int[] arr = new int[n];
        for (int i = 0; i < n; i++) {
            arr[i] = random.nextInt();
        }
        Arrays.sort(arr);
        return arr;
    }

    public static void main(String[] args) {
        
        int l = 200; // number of input lengths
        double[] xs = new double[l - 1]; //values on x axes
        double[] ys_bs = new double[l - 1]; // values on y axes
        double[] ys_is = new double[l - 1]; // values on y axes

        for (int i = 1; i < l; i++) {
            //double x = (double) Math.pow(10, i);
            double x = (double) i;
            int[] arr = generate_random_array((int) x);

            double startTime = System.nanoTime();
            bs2(4, arr, 0, arr.length-1);
            double endTime = System.nanoTime();
            double duration_bs = (endTime - startTime);

            startTime = System.nanoTime();
            is(4, arr);
            endTime = System.nanoTime();
            double duration_is = (endTime - startTime);

            System.out.printf("%.0f: bs: %.0f is: %.0f%n", x, duration_bs, duration_is);
            xs[i - 1] = x;
            ys_bs[i - 1] = duration_bs;
            ys_is[i - 1] = duration_is;
        }

        XYChart chart = new XYChartBuilder()
            .width(800)
            .height(600)
            .title("Iterative vs Binary Search")
            .xAxisTitle("Input size (n)")
            .yAxisTitle("Time (nanoseconds)")
            .build();
        
        chart.addSeries("Binary Search", xs, ys_bs)
            .setMarker(SeriesMarkers.CIRCLE);

        chart.addSeries("Iterative Search", xs, ys_is)
            .setMarker(SeriesMarkers.DIAMOND);


        // chart.getStyler().setXAxisLogarithmic(true);

        SwingWrapper<XYChart> swingWrapper = new SwingWrapper<>(chart);
        swingWrapper.displayChart();
      
        System.out.printf("%nok%n");
    }
}
