def cp_one(lines): # compiled python
    xs, ys = [], []
    for line in lines:
        x, y = line.split()
        xs.append(int(x))
        ys.append(int(y))
    return sum(abs(x - y) for x, y in zip(sorted(xs), sorted(ys)))

from libc.stdlib cimport qsort

cdef int compare(const void* a, const void* b) noexcept nogil:
    cdef int* x = <int*>a
    cdef int* y = <int*>b
    return x[0] - y[0]

def cy_one(lines): #cython
    cdef int[1000] xs
    cdef int[1000] ys
    for i in range(1000): # does not have to translate range
        x, y = lines[i].split("   ")
        xs[i] = int(x)
        ys[i] = int(y)

    qsort(<void*>xs, 1000, sizeof(int), compare)
    qsort(<void*>ys, 1000, sizeof(int), compare)

    total = 0
    for i in range(1000):
        total += abs(xs[i] - ys[i])
    return total
