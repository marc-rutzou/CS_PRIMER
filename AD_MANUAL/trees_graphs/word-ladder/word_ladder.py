alphabet = 'abcdefghijklmnopqrstuvwxyxz'

            
class Node:
    def __init__(self, word):
        self.word = word
        self.neighbours = self._find_neighbours()
        self.depth = 0
        self.path = []

    def __repr__(self):
        return f"{self.word}"

    def _find_neighbours(self):
        """
        Find all words that the given word can be changed to by altering 1 letter.
        """
        ns = []
        for i in range(len(self.word)):
            for a in alphabet:
                c = self.word[:i] + a + self.word[i+1:]
                if c in words and c != self.word:
                    ns.append(c)
        return ns


def bfs(start, end):
    q = [start]
    visited = set()
    while q:
        n = q.pop(0)

        if n.word in visited:
            continue
        visited.add(n.word)

        if n.word == end.word:
            n.path = n.path[::-1]
            n.path.append(end.word)
            return n.depth, n.path

        for neighbour in n.neighbours:
            neighbour = Node(neighbour)
            neighbour.depth = n.depth + 1
            neighbour.path.append(n.word)
            for x in n.path:
                neighbour.path.append(x)
            q.append(neighbour)

        
if __name__ == '__main__':
    words = []
    with open('words.txt', 'r') as f:
        for word in f:
            words.append(word.rstrip())

    start = Node("four")
    end = Node("five")

    depth, path = bfs(start, end)
    print(depth)
    print(path)


