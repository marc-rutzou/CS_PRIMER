DUMMY = """....XXMAS.
.SAMXMS...
...S..A...
..A.A.MS.X
XMASAMX.MM
X.....XA.A
S.S.S.S.SS
.A.A.A.A.A
..M.M.M.MM
.X.X.XMASX
"""

DUMMY2 = """..X...
.SAMX.
.A..A.
XMAS.S
.X....
"""

KEY = "XMAS"

#TODO: improve find candidates to only return candidates with the correct letter
#TODO: only add potential solution if it is in a straight line instead of saving them all and checking later
#TODO: dont start by looping through the entire file to find the X's, just start by while going through the file and if it is an x append it
#TODO: dont need the path if I know solution is correct, just need to count++

from aoc4cpp import one_cpp
import timeit

def find_candidates(i, j, lines):
    cs = []
    for di, dj in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
        if 0 <= i + di < len(lines) and 0 <= j + dj < len(lines[0]):
            cs.append((i + di, j + dj, lines[i + di][j + dj]))
    return cs


def check_pss(pss):
    directions = [  (1, 1), (-1, -1), (-1, 1), (1, -1),  #diagonal
                    (0, 1), (0, -1),  #horizontal
                    (1, 0), (-1, 0)   #vertical
                 ]
    solutions = []
    for ps in pss:
        deltas = [(a - x, b - y) for (x, y), (a, b) in zip(ps, ps[1:])]
        if len(set(deltas)) == 1 and deltas[0] in directions:
            solutions.append(ps)
    return solutions
        

def build_q_of_xs(lines):
    q = []
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            if c == 'X':
                q.append((i, j, c, [(i, j)]))
    return q


def one(lines):
    q = build_q_of_xs(lines)
    pss = []
    while q:
        i, j, c, path = q.pop()
        for x, y, c_next in find_candidates(i, j, lines):
            if KEY.find(c_next) == KEY.find(c) + 1:
                new_path = path + [(x, y)]
                if c_next == 'S':
                    pss.append(new_path)
                else:
                    q.append((x, y, c_next, new_path))
    return len(check_pss(pss))


if __name__ == "__main__":
    print()

    functions = {"Python": one, "C++": one_cpp}

    for name, f in functions.items():
        assert f(DUMMY.splitlines()) == 18

        with open("lines.txt", 'r') as file:
            lines = file.readlines()

        assert f(lines) == 2613

        number = 20
        print(f"{name}:\t{timeit.timeit(lambda: f(lines), number=number):.3f}")

    print("ok")
    
