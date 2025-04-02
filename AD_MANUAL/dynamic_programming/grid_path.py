#TODO: also solve as a graph problem

MEMO = {}
PATH = []

def find(grid):
    if not grid:
        return 0

    curr = grid[0][0]

    shape = (len(grid), len(grid[0]))
    if MEMO.get(shape, 0):
        return MEMO[shape]

    if shape == (1, 1):
        return curr
    
    r = [row[1:] for row in grid if row[1:]]
    d = grid[1:]
    
    ans = None
    if not r:
        ans = curr + find(d)
        PATH.append("d")
    elif not d:
        ans =  curr + find(r)
        PATH.append("r")
    else:
        cost_right = find(r)
        cost_down = find(d)
        if cost_right < cost_down:
            PATH.append("r")
        else:
            PATH.append("d")
        ans = curr + min(cost_right, cost_down) 
    MEMO[shape] = ans 
    return ans


def get_neighbours(shape, i, j):
    neighbours = []
    if i + 1 < shape[0]:
        neighbours.append((i + 1, j))
    if j + 1 < shape[1]:
        neighbours.append((i, j + 1))
    return neighbours

def bfs(grid, start = (0, 0)):
    q = [(start, grid[start[0]][start[1]])]
    path = {start: [start]}
    shape = (len(grid), len(grid[0]))
    end = (len(grid) - 1, len(grid[0]) - 1)
    while q:
        print()
        print(f"q: {q}")
        print(path)
        curr = q.pop()
        i, j = curr[0]
        cost = curr[1]
        print(f"i: {i}, j: {j}, cost: {cost}")
        if (i, j) == end:
            return path[(i, j)], cost
        for n in get_neighbours(shape, i, j):
            print("neighbour: ", n)
            n_costs = cost + grid[n[0]][n[1]]
            q.append((n, n_costs))
            q = sorted(q, key= lambda x: x[1], reverse=True) 
            path[n] = path[(i, j)] + [n]
        


if __name__ == '__main__':
    grid = [[1, 3, 2, 4], [2, 1, 6, 5], [2, 2, 4, 3]]
    assert find(grid) == 13
    path, cost = bfs(grid)
    print()
    print(path)
    print(cost)
    print()
    print("ok")

