import sys

#TODO: create a tree data structure based on input

class Node:
    def __init__(self, ppid, pid, comm):
        self.parent = None
        self.children = []
        self.ppid = ppid
        self.pid = pid
        self.comm = comm
    
    def print(self):
        print(f"{self.ppid} - {self.pid} {self.comm}")


class Tree:
    def __init__(self):
        self.tree = []

    def add_node(self, ppid, pid, comm):
        n = Node(ppid, pid, comm)
        for o in self.tree:
            if o.pid == n.ppid:
                n.parent = o
                o.children.append(n)
            elif o.ppid == n.pid:
                o.parent = n
                n.children.append(o)
        self.tree.append(n)

    def print(self):
        for node in self.tree:
            if not node.parent:
                self._print_from_node(node)


    def _print_from_node(self, node, indent=0):
        if indent == 0:
            print()
            print("root")
            print("|", end="")
        else:
            print(" \\", end="")
            
        print("___" * indent, end = "") 
        node.print()
        for child in node.children:
            self._print_from_node(child, indent+1)


if __name__ == '__main__':
    #for line in sys.stdin:
    #    print(line)

    data = [[0, 1, 'a'], 
            [1, 2, 'b'], [1, 3, 'c'], [1, 8, 'h'], 
            [2, 4, 'd'], [2, 5, 'd'], [3, 6, 'f'], [3, 7, 'g'],
            [6, 9, 'k'],

            [20, 21, 'p'],
            [21, 22, 'l'], [21, 23, 'k'],
            [22, 24, 'm'],

            [30, 31, 'x']]


    t = Tree()
    for ppid, pid, comm in data:
        t.add_node(ppid, pid, comm)

    t.print() 



    
