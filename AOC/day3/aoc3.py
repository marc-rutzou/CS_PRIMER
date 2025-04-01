"""
mul(X, Y) where X and Y are each 1-3 digit numbers
"""

import re
import timeit

from aoc3cpp import one_cpp

DUMMY = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
DUMMY2 = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

def one(text):
    pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
    return sum(int(x) * int(y) for x, y in re.findall(pattern, text))

if __name__ == "__main__":
    assert one(DUMMY) == 161
    assert one_cpp(DUMMY) == 161
    print(one_cpp(DUMMY2))

    with open("lines.txt", 'r') as f:
        text = f.read()

    assert one(text) == 192767529
    assert one_cpp(text) == 104083373


    print(f"Python:\t{timeit.timeit(lambda: one(text), number=5000):.3f}")
    print(f"C++:\t{timeit.timeit(lambda: one_cpp(text), number=5000):.3f}")
    print("ok")
    

