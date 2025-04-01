# cython: profile=True
# cython: linetrace=True
# cython: binding=True

def one_cp(lines):
    num_safe = 0
    for report in lines:
        levels = [int(x) for x in report.split(" ")]
        deltas = [levels[i+1] - levels[i] for i in range(len(levels)-1)]

        sign_sum = 0
        for delta in deltas:
            if not (1 <= abs(delta) <= 3):
                break
            sign_sum += delta // abs(delta)
        else:
            if abs(sign_sum) == len(deltas):
                num_safe += 1
    return num_safe


def one_cy(lines):
    cdef int num_safe = 0
    cdef int i, j, n, sign_sum, delta
    cdef str report
    cdef list tokens
    cdef int[100] levels

    for i in range(len(lines)):
        report = lines[i]
        tokens = report.split(" ")
        n = len(tokens)

        for j in range(n):
            levels[j] = int(tokens[j])

        sign_sum = 0
        for i in range(n - 1):
            delta = levels[i+1] - levels[i]

            if not (1 <= abs(delta) <= 3):
                break
            if delta > 0:
                sign_sum += 1
            else:
                sign_sum -= 1
        else:
            if abs(sign_sum) == n - 1:
                num_safe += 1
    return num_safe
