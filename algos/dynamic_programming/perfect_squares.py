
def get_squares(n):
    squares, i = [], 1
    while i ** 2 <= n:
        squares.append(i ** 2)
        i += 1
    return squares

CACHE = {}

def f(x):
    if CACHE.get(x):
        return CACHE[x]

    if x == 0:
        return 0
   
    children = {}
    for s in get_squares(x):
        children[x - s] = 1 + f(x - s)
    CACHE[x] = min(children.values())
    return CACHE[x]
        
def f2(x):
    fxs = [0]
    for i in range(1, x + 1):
        min_amount = min(fxs[i - square] for square in get_squares(i))
        fxs.append(1 + min_amount)
    return fxs[-1]
         
    
if __name__ == "__main__":
    assert f2(23) == 4
    print("ok")
