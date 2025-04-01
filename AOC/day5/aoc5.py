"""
47|53 -> 47 must be printed SOMEWHERE before 53, if they are botch in an update
update example: 75, 47, 61, 53, 29

return the sum of the middle page of the CORRECTLY-ordered updates
"""

DUMMY = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
""".splitlines()

import timeit
from aoc5cpp import one_cpp, one_cpp2, one_cpp3, one_cpp4, one_cpp5, one_cpp6, one_cpp7

def one_op(lines):
    i = 0
    rules = {}
    # Pre-process rules into a more efficient structure
    while lines[i] != "":
        x, y = lines[i].split("|")
        if x not in rules:
            rules[x] = set()  # Use set instead of list for O(1) lookups
        rules[x].add(y)
        i += 1
    
    ans = 0
    updates = [line.split(",") for line in lines[i + 1:]]  # More readable than map
    for update in updates:
        for j in range(len(update)):
            curr_rules = rules.get(update[j], set())  # Cache the lookup
            for k in range(j + 1, len(update)):
                if update[k] not in curr_rules:
                    break
            else:
                continue
            break
        else:
            mid = (len(update) - 1) // 2  # Simplified middle calculation
            ans += int(update[mid])
    return ans


def one(lines):
    i = 0
    rules = {} # what needs to come behind it
    while lines[i] != "":
        x, y = lines[i].split("|")
        rules[x] = rules.get(x, []) + [y]
        i += 1
    
    ans = 0
    updates = list(map(lambda x: x.split(","), lines[i + 1:])) # +1 b/c skip empty line
    for update in updates:
        for j in range(len(update)):
            for k in range(j + 1, len(update)):
                if not (update[k] in rules.get(update[j], [])):
                    break # if you do not break you get into else and continue
            else:
                continue
            break # if I do break, break out of update entirely
        else:
            mid = len(update) // 2 + 1 if len(update) % 2 == 1 else len(update) // 2
            ans += int(update[mid - 1])
    return ans


if __name__ == "__main__":
    # assert one(DUMMY) == 143
    # assert one_cpp(DUMMY) == 143

    with open("lines.txt", 'r') as file:
        lines = [line.strip() for line in file.readlines()]

    assert one_op(lines) == 4135
    # assert one_cpp6(lines) == 4135

    runs = 10000
    # print(f"Python:\t\t\t\t{timeit.timeit(lambda: one(lines), number=runs):.4f}")
    # print(f"Python optimized:\t\t{timeit.timeit(lambda: one_op(lines), number=runs):.4f}")
    # print(f"C++:\t\t\t\t{timeit.timeit(lambda: one_cpp(lines), number=runs):.4f}")
    # print(f"above + unordered map:\t\t{timeit.timeit(lambda: one_cpp2(lines), number=runs):.4f}")
    # print(f"above + early breaks:\t\t{timeit.timeit(lambda: one_cpp3(lines), number=runs):.4f}")
    # print(f"above + map lookup caching:\t{timeit.timeit(lambda: one_cpp4(lines), number=runs):.4f}")
    # print(f"above + array of array:\t\t{timeit.timeit(lambda: one_cpp5(lines), number=runs):.4f}")
    print(f"above + replace sscanf:\t\t{timeit.timeit(lambda: one_cpp6(lines), number=runs):.4f}")
    print(f"above + two digit rules:\t{timeit.timeit(lambda: one_cpp7(lines), number=runs):.4f}")

    print("ok")