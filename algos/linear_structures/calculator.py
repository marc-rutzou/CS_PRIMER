"""
Extensions:
    - check valid
"""

OPERATORS = {
        "-": lambda a, b: a - b,
        "+": lambda a, b: a + b,
        "/": lambda a, b: a / b, 
        "*": lambda a, b: a * b
}

def eval(s): 
    stack = []
    for c in s:
        print(stack)
        if c == ")":
            b, f, a = stack.pop(), stack.pop(), stack.pop()
            print(f"\nf(a, b) = {f.__name__}({a}, {b}) = {f(a, b)}\n")
            stack.append(f(a, b))
        if c.isnumeric():
            if len(stack) != 0 and isinstance(stack[-1], int):
                stack.append(stack.pop() * 10 + int(c))
            else:
                stack.append(int(c))
        if c in OPERATORS.keys():
            stack.append(OPERATORS[c])
        prev = c
    return stack.pop()


if __name__ == "__main__":
    s = "(((150 - 10) / (3 - 2)) - 4)"
    print(eval(s))

            

