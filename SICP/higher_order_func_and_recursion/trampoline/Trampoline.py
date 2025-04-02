def fact(n):
    if n <= 1:
        return 1
    return n * fact(n - 1)

def fact_i(n):
    total = 1
    for i in range(1, n + 1):
        total *= i
    return total

def fact_lr_desc(total, n):
    if n < 1:
        return total
    return lambda: fact_lr_desc(total * n, n - 1) 

def trampoline(f):
    while callable(f):
        f = f()
    return f


f_tramped = trampoline(lambda: fact_lr_desc(1, 5))
print(f_tramped)
