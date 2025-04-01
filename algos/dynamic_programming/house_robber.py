"""
[3, 10, 1, 2, 20]

base case: if only 2 left, pick the highest, if only 1 left pick that one
recursion: if picking a number continue with the list without that number and surrounding numbers

"""

CACHE = {}

def solve(xs):
    l = len(xs)

    if l == 2:
        return max(xs)
    elif l == 1:
        return xs[0]
    elif l == 0:
        return 0
    
    totals = []
    for i in range(l):
        
        rest = []
        if i == 0:
            rest = xs[i+2:]
        elif i == l - 1:
            rest = xs[:i-1]
        else:
            rest = xs[:i-1] + xs[i+2:]

        if not CACHE.get(str(rest)):
            CACHE[str(rest)] = solve(rest)

        totals.append(xs[i] + CACHE[str(rest)])
    return max(totals)

def bottom_up(xs):
    prev, prevprev = 0, 0
    for x in xs:
        prev, prevprev = max(prev, x + prevprev),prev
    return prev
        
    

if __name__ == "__main__":
    xs = [3, 10, 1, 2, 20, 5, 23, 1, 3, 14, 13, 1]
    ans = bottom_up(xs)
    print(f"ans: {ans}")
