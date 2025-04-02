ACTIONS = {
    "a_into_b" : lambda a, b: (max(0, a+b-5), min(5, a+b)),
    "b_into_a" : lambda a, b: (min(3, a+b), max(0, a+b-3)),
    "fill_a"   : lambda a, b: (3, b),
    "fill_b"   : lambda a, b: (a, 5),
    "empty_a"  : lambda a, b: (0, b),
    "empty_b"  : lambda a, b: (a, 0)
}

    

class Node:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.ns = self._find_neighbours()
        self.path = []

    def _find_neighbours(self):
        ns = []
        for action in ACTIONS.values():
            c = action(self.a, self.b)
            if (self.a <= 3 and self.b <= 5) and (c != (self.a, self.b)):
                ns.append(c)
        return ns

    def __repr__(self):
        return f"({self.a}, {self.b})"
    
def bfs():
    q = [Node(0, 0)]
    visited = set()
    while q:
        node = q.pop(0)
        if node.b == 4:
            node.path = node.path[::-1]
            node.path.append(node)
            return node.path
        for n in node.ns:
            a, b = n
            n = Node(a, b)
            n.path.append((node.a, node.b))
            for p in node.path:
                n.path.append(p)
            if not n in visited:
                q.append(n)
                visited.add(n)

if __name__ == '__main__':
    path = bfs()
    print("path: ", path)
