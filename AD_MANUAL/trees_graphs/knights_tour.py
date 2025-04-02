"""
- create graph with connections
- while knight is going through vertices delete connections
- if any vertex is disconnected go back and try something else

- just start at node
- find neighbours
- if the knight goes to a state then add it to visited
- in the find neighbours function the visited are not considered anymore

NOTE: it is solved when all states is equal to visited
"""
MOVES  = [(-2, 1), (-2, -1), (-1, 2), (-1, -2), (1, 2), (1, -2), (2, 1), (2, -1)]

class Node:
    def __init__(self, state):
        self.state = state
        self.neighbours = self._find_neighbours()
        self.considered = []
        self.path = []

    def _find_neighbours(self):
        ns = []
        for move in MOVES:
            c = (chr(ord(self.state[0]) + move[0]), self.state[1] + move[1])
            if ord(c[0]) < ord('a') or ord(c[0]) > ord('e') or c[1] < 1 or c[1] > 5:
                continue
            ns.append(c)
        return ns

    def __repr__(self):
        return f"<{self.state}>"

def solve(starting_state, states):
    q = [starting_state]
    visited = [starting_state]
    while q and visited:
        print(f"q: {q}")
        curr_state = q.pop(0)

        # if I already considered this state for my last state in the path then I have nothing to consider anymore
        if curr_state.state in [node.state for node in visited[-1].considered]:
            visited.pop()

        if not visited:
            break

        if curr_state not in visited and visited[-1].state in curr_state.neighbours:
            visited.append(curr_state)
        else:
            visited[-1].considered.append(curr_state)
        print(f"visited: {visited}\n")

        if states == [node.state for node in visited]:
            return visited 

        for n in curr_state.neighbours:
            for node in states:
                if node.state == n:
                    n = node
                    break
            else:
                raise Exception("neighbour not in STATES")
            if n.state not in [node.state for node in visited]: # and n.state not in [node.state for node in q]:
                q.insert(0, n)
    return 0


if __name__ == '__main__':
    states = [Node((letter, int(number))) for letter in "abcde" for number in "12345"]
    for start in states:
        path = solve(start, states)
        print(path)
        break
