"""
produce test value by combining numbers on the right
always evaluated left to right
numbers can not be rearranged
only + and * 
"""

import timeit

dummy = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""

from aoc7cpp import one_cpp

# TODO: can I determine early if a branch in the tree won't make it?
# e.g. when left num in numbers > ans, you passed it

# TODO: dont slice
# e.g. replace the "first" number you are at in the array and pass a length to the next call

# TODO: multiply first, to get to target faster

def is_valid(ans, numbers, start=0, length=None):
    """
    combine the first two numbers with + or *
    call is_valid with combi replacing first number and reduced length
    returns True if any combination works
    """
    if length < 2:
        return numbers[start] == ans
    
    # early break
    if numbers[start] > ans:
        return False
    
    a, b = numbers[start], numbers[start + 1]
    
    # Try multiplication
    numbers[start+1] = a * b
    if is_valid(ans, numbers, start+1, length - 1):
        return True
    
    # Try addition
    numbers[start+1] = a + b
    if is_valid(ans, numbers, start+1, length - 1):
        return True

    numbers[start+1] = b 
    return False


def one(lines):
    total = 0
    lines = lines.splitlines()
    for line in lines:
        ans, numbers = line.split(": ")
        numbers = [int(x) for x in numbers.split(" ")]
        if is_valid(int(ans), numbers, 0, len(numbers)):
            total += int(ans)
    return total


if __name__ == "__main__":
    # assert one(dummy) == 3749
    # assert one_cpp(dummy) == 3749

    with open("lines.txt", "r") as file:
        lines = file.read()
    
    # assert one(lines) == 538191549061
    # assert one_cpp(lines) == 538191549061

    runs = 1000
    # print(f"Python:\t\t{timeit.timeit(lambda: one(lines), number=runs)}")
    print(f"C++:\t\t{timeit.timeit(lambda: one_cpp(lines), number=runs)}")

    print("ok")

    