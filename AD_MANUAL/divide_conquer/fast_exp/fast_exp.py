def exp(x, a):
    total = 1
    for _ in range(a):
        total *= x
    return total

def fast_exp(x, a):
    """
    x^(a) = x^(a/2) * x^(a/2)
    x^1 = x
    """
    print(x,a)
    if a == 0:
        return 1
    if a == 1:
        return x
    new_a = a//2 if (a%2==0) else a//2 + 1
    return fast_exp(x, new_a) * fast_exp(x, a//2) 
 
if __name__ == "__main__":
    x = 2
    a = 5
    ans_exp = exp(x, a)
    ans_fast_exp = fast_exp(x, a)
    print(ans_exp, ans_fast_exp)
