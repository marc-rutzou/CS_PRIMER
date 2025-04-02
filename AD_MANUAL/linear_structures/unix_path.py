
def shorten(p):
    stack = []
    ls = p.split(sep="/")[1:] # this is already O(n)
    for elem in ls:
        if elem == "..":
            try:
                stack.pop()
                continue
            except IndexError:
                pass
        if elem == "." or elem == "":
            continue
        stack.append(elem)
    return "/" + "/".join(stack) # also O(n) 

test = "/../etc//foo/../bar/./baz.txt"
print(shorten2(test))


