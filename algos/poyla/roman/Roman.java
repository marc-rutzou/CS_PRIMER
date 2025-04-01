package algos.poyla.roman;

public class Roman {
    private static String[][] m = {
        {"I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"},
        {"X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"},
        {"C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM"},
        {"M", "MM", "MMM"},
    };  

    public static String f(int n) {
        //TODO: have problems if order > 3
        //TODO: have problems if order = 3 and i > 3

        String out = "";
        int order = 0; // order = 0 -> *10^0
        while (n > 0) {
            int i = n % 10;
            n /= 10;
            order++;
            if (i == 0) continue;
            out = m[order - 1][i - 1] + out;
        }
        return out; 
    }

    public static void main(String[] args) {
        assert f(39).equals("XXXIX");
        assert f(246).equals("CCXLVI");
        assert f(2421).equals("MMCDXXI");

        assert f(207).equals("CCVII");
        assert f(1066).equals("MLXVI");

        // f(4000);

        System.out.println("ok!");
    }
}

