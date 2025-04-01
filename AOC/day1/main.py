import timeit
from cy1 import cp_one, cy_one
from extension import ce_one

def one(lines):
    xs, ys = [], []
    for line in lines:
        x, y = line.split()
        xs.append(int(x))
        ys.append(int(y))
    return sum(abs(x - y) for x, y in zip(sorted(xs), sorted(ys)))


def two(lines):
    xs, ys = [], {}
    for line in lines:
        x, y = line.split()
        y = int(y)
        xs.append(int(x))
        ys[y] = ys.get(y, 0) + 1
    return sum(x * ys.get(x, 0) for x in xs)


if __name__ == "__main__":
    with open("lines.txt", 'r') as file:
        lines = file.readlines()
        assert one(lines) == 1341714
        assert two(lines) == 27384707
        print(f"Basline:\t\t{timeit.timeit(lambda: one(lines), number=4000):.3f}")

        assert cp_one(lines) == 1341714
        print(f"Compiled Python:\t{timeit.timeit(lambda: cp_one(lines), number=4000):.3f}")

        assert cy_one(lines) == 1341714
        print(f"Cython:\t\t\t{timeit.timeit(lambda: cy_one(lines), number=4000):.3f}")

        assert ce_one(lines) == 1341714
        print(f"C++ Extension:\t\t{timeit.timeit(lambda: ce_one(lines), number=4000):.3f}")
