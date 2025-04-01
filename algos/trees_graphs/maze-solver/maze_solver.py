"""
Neighbours are always up, down, left, right except if the index in the maze is out of range.

Give solve start and end coordinates
"""
import subprocess

MOVES = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
COSTS = {" ": 1, ".": 3, "#": 10, "X": 0}


def print_maze(maze, path = []):
    subprocess.run(["clear"])
    for i, row in enumerate(maze):
        for j, c in enumerate(row):
            if (i, j) in path:
                print("*", end="")
            else:
                print(c, end="")
        print()


def load_maze(file):
    """
    Load the maze.txt file into a list of lists and find the start and end cells.
    The maze is not square, so find the longest row and extend all others to that length
    """
    #TODO: you are stripping the line, therefore deleting the spaces and then putting them back again ._.
    maze, start, end = [], (-1, -1), (-1, -1)
    with open('small.txt', 'r') as f:
        for i, line in enumerate(f):
            row = []
            for j, c in enumerate(line[:-1]):  
                if c == 'O':
                    start = (i, j)
                elif c == 'X':
                    end = (i, j)
                row.append(c)
            maze.append(row)
    return maze, start, end


def solve(maze, start, end):
    """
    how to keep track of cumulative costs and order the queue by it?
    """
    #TODO: insert neighbour in right position instead of re-sorting each time
    q = [(start, 0)]
    visited = {(start)}
    path = {start: []}
    while q:
        (i, j), cost = q.pop()
        if (i, j) == end:
            return path
        visited.add((i, j))
        
        print_maze(maze, path[(i, j)])
        print(cost)

        for n in [(i + di, j + dj)  for di, dj in MOVES if 0 <= i + di < len(maze) and 0 <= j + dj < len(maze[0])]:
            if n in visited:
                continue
            ni, nj = n
            path[n] = path[(i, j)] + [(ni, j)]
            new_cost = COSTS[maze[ni][nj]] + cost
            q.append((n, new_cost))
            q = sorted(q, key = lambda x: x[1], reverse=True)            


if __name__ == '__main__':
    maze, start, end = load_maze("small.txt")
    print_maze(maze)
    path = solve(maze, start, end)
    
