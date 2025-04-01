from aoc2cy import one_cp, one_cy
from aoc2cpp import one_cpp, one_cpp2

import timeit
import cProfile
import pstats


DUMMY = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""


def one(lines):
    num_safe = 0
    for report in lines:
        levels = [int(x) for x in report.split(" ")]
        deltas = [levels[i+1] - levels[i] for i in range(len(levels)-1)]

        sign_sum = 0
        for delta in deltas:
            if not (1 <= abs(delta) <= 3):
                break
            sign_sum += delta // abs(delta)
        else:
            if abs(sign_sum) == len(deltas):
                num_safe += 1
    return num_safe
    

if __name__ == "__main__":
    assert one(DUMMY.splitlines()) == 2
    assert one_cy(DUMMY.splitlines()) == 2
    assert one_cpp(DUMMY.splitlines()) == 2
    # assert one_cpp2(DUMMY.splitlines()) == 2

    with open("lines.txt", 'r') as f:
        lines = f.readlines()

    assert one(lines) == 549
    assert one_cy(lines) == 549
    assert one_cpp(lines) == 549
    assert one_cpp2(lines) == 549

    print()
    print(f"Basline:\t\t\t\t{timeit.timeit(lambda: one(lines), number=1000):.3f}")
    print(f"Compiled Python:\t\t\t{timeit.timeit(lambda: one_cp(lines), number=1000):.3f}")
    print(f"Cython:\t\t\t\t\t{timeit.timeit(lambda: one_cy(lines), number=1000):.3f}")
    print(f"C++:\t\t\t\t\t{timeit.timeit(lambda: one_cpp(lines), number=1000):.3f}")
    print(f"C++ (w/o dynamic memory allocation):\t{timeit.timeit(lambda: one_cpp2(lines), number=1000):.3f}")
    
    """
    cProfile.run('one(lines)', 'one.prof')
    cProfile.run('one_cy(lines)', 'one_cy.prof')
    cProfile.run('one_cpp(lines)', 'one_cpp.prof')

    p_one = pstats.Stats('one.prof')
    p_one_cy = pstats.Stats('one_cy.prof')
    p_one_cpp = pstats.Stats('one_cpp.prof')

    p_one.sort_stats(pstats.SortKey.CUMULATIVE).print_stats()
    p_one_cy.sort_stats(pstats.SortKey.CUMULATIVE).print_stats()
    p_one_cpp.sort_stats(pstats.SortKey.CUMULATIVE).print_stats()
    """
    print()
    print("ok")

    
