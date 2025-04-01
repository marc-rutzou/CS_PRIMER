"""
- go right if something in front of you
- otherwise continue
- leave map when reaching edge

-> count disinct positions including starting positions
"""

dummy = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""
 
# TODO: I am mutating the grid_str, so I get segmentation error when running one_cpp twices

import timeit
from aoc6cpp import one_cpp, one_cpp2, one_cpp3, one_cpp4


def find_start(grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == '^':
                return i, j

# print('\n'.join(''.join(x for x in row) for row in grid))
def print_grid(grid, i, j):
    for k, row in enumerate(grid):
        for l, char in enumerate(row):
            if (k, l) == (i, j):
                print('^', end="")
            else:
                print(char, end="")
        print()
    print()


# Python optimization did not do anything to the profiling or benchmarking
def one(grid_str):
    grid = grid_str.splitlines()
    delta = ((-1, 0), (0, 1), (1, 0), (0, -1)) # up, right, down, left
    i, j = find_start(grid)
    delta_idx = 0
    visited = {(i, j)}
    while (i != 0 and i != len(grid) - 1) and (j != 0 and j != len(grid[0]) - 1):
        nxt_i, nxt_j = tuple(map(sum, zip((i, j), delta[delta_idx])))
        if grid[nxt_i][nxt_j] == '#':
            delta_idx = delta_idx + 1 if delta_idx < len(delta) - 1 else 0
            i, j = tuple(map(sum, zip((i, j), delta[delta_idx])))
        else:
            i, j = nxt_i, nxt_j
        visited.add((i, j))
        # print_grid(grid, i, j)
    return len(visited)
    
if __name__ == '__main__':
    # assert one(dummy) == 41
    # assert one_cpp(dummy) == 41
    # assert one_cpp2(dummy) == 41
    # assert one_cpp3(dummy) == 41

    with open("lines.txt", 'r') as f:
        grid_str = f.read()
    
    # assert one(grid_str) == 4374
    # assert one_cpp(grid_str) == 4374
    # assert one_cpp2(grid_str) == 4374
    # assert one_cpp3(grid_str) == 4374
    # assert one_cpp4(grid_str) == 4374
    # print(one_cpp4(grid_str))

    runs = 100000
    # print(f"Python:\t\t\t{timeit.timeit(lambda: one(grid_str), number=runs):.3f}")
    # print(f"C++:\t\t\t{timeit.timeit(lambda: one_cpp(grid_str), number=runs):.3f}")
    # print(f"C++ + stack memory:\t{timeit.timeit(lambda: one_cpp2(grid_str), number=runs):.3f}")
    # print(f"Above + direct str:\t{timeit.timeit(lambda: one_cpp3(grid_str), number=runs):.3f}")
    print(f"Above + while condition:\t{timeit.timeit(lambda: one_cpp4(grid_str), number=runs):.3f}")
    print("ok")
