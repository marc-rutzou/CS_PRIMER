def qsort(xs, start, end):
    def swap(i, j):
        temp = xs[i]
        xs[i] = xs[j]
        xs[j] = temp
        return

    if start >= end - 1:
        return

    m = start
    for i in range(start + 1, end):
        if xs[i] < xs[start]:
            m += 1
            swap(i, m)
    swap(start, m)
    qsort(xs, start=start, end=m)
    qsort(xs, start=m+1, end=end)


if __name__ == "__main__":
    xs = [4, 3, 6, 2, 5]
    qsort(xs, 0, len(xs))
    assert(xs == sorted(xs))
    print("ok")
