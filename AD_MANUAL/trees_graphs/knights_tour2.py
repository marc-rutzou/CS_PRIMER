import time

STATES = [(letter, int(number)) for letter in "abcde" for number in "12345"]
MOVES  = [(-2, 1), (-2, -1), (-1, 2), (-1, -2), (1, 2), (1, -2), (2, 1), (2, -1)]

class Vertex:
    def __init__(self, position):
        self.position = position
        self.path = [position]

    def __repr__(self):
        return f"{self.position}"

    def candidates(self):
        """
        Return the possible next positions for a knight given its current position
        and its previous path.
        """
        cs = []
        for move in MOVES:
            c = (chr(ord(self.position[0]) + move[0]), self.position[1] + move[1])
            if ord(c[0]) < ord('a') or ord(c[0]) > ord('e') or c[1] < 1 or c[1] > 5:
                continue
            if not c in self.path:
                cs.append(c)
        return cs

def print_board(path):
    board = [["[  ]" for _ in range(5)] for _ in range(5)]

    for i, position in enumerate(path):
        x = 5 - position[1]
        y = ord(position[0]) - ord('a')
        space = "" if i > 9 else " " 
        board[x][y] = f"[{i}{space}]"

    for row in board:
        print("".join(row))  
    print()

def tour(start=('a', 1)):
    v = Vertex(start)
    q = [v]
    while q:
        current = q.pop()
        print_board(current.path)
        if len(current.path) == 25:
            return current.path
        for c in current.candidates():
            c = Vertex(c)
            c.path = current.path + [c.position]
            q.append(c)

if __name__ == '__main__':
    tour()
