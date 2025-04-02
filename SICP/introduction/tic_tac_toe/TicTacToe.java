package programming.introduction.tic_tac_toe;

import java.util.Scanner;

public class TicTacToe {
    private static char[][] m = {{' ',' ',' '},{' ',' ',' '},{' ',' ',' '}};

    public static void main(String[] args) {
        var s = new Scanner(System.in);

        boolean p1_turn = true;
        while (true) {
            char sign = p1_turn ? 'X' : 'O';

            System.out.printf("\nx y:");
            int x = s.nextInt();
            int y = s.nextInt();
            
            if (m[x][y] == ' ') {
                m[x][y] = sign;
                print_grid();           
                if (check_win(sign)) {
                    System.out.printf("\n%s won!\n", p1_turn ? "Player 1" : "Player 2");
                }
                p1_turn = !p1_turn;
            } else {
                System.out.println("Place already taken.");
            }
        }
    }

    public static boolean check_win(char sign) {
        for (int i = 0; i < 3; i++) {
            int count_row = 0;
            int count_col = 0;
            for (int j = 0; j < 3; j++) {
                if (m[i][j] == sign) {
                    count_row++;
                } 
                if (m[j][i] == sign) {
                    count_col++;
                }
            }
            if (count_row == 3 || count_col == 3) {
                return true;
            }
        }
        return false;
    }

    public static boolean is_valid_input(int x) {
        if (x < 3 && x >= 0) {
            return true;
        } else {
            System.out.println("input must be 2 ints between 0 and 3, separated by a space");
            return false;
        }
    }

    public static void print_grid() {
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                System.out.printf("%c", m[i][j]);
                if (j != 2) {
                    System.out.printf("|");
                }
            }
            if (i != 2) {
                System.out.printf("\n------\n");
            }
        }
    }
}
