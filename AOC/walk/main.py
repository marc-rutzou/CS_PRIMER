import timeit

from aoc import solve # solve1, solve2, solve3, solve4
# from aoc_cpp import solve_cpp

if __name__ == "__main__":
    with open("large_case.txt") as f:
        page = f.read()

    # assert solve(page) == 4135
    # assert solve_cpp(page) == 4135

    # assert solve(page) == 143
    # print(solve(page))

    runs = 1000
    print(f"Python:\t\t{timeit.timeit(lambda: solve(page), number=runs):.4f}")
    """
    print(f"Python:\t\t{timeit.timeit(lambda: solve2(page), number=runs):.4f}")
    print(f"Python:\t\t{timeit.timeit(lambda: solve3(page), number=runs):.4f}")
    print(f"Python:\t\t{timeit.timeit(lambda: solve4(page), number=runs):.4f}")
    # print(f"C++:\t\t{timeit.timeit(lambda: solve_cpp(page), number=runs):.4f}")
    """