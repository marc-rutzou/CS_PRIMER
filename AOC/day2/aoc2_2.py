def valid(levels, d=0):
    if d > 1:
        return False

    deltas = [levels[i+1] - levels[i] for i in range(len(levels)-1)]

    sign_sum = 0
    for i, delta in enumerate(deltas):
        if abs(delta) > 3 or delta == 0:
            if valid(levels[:i] + levels[i+1:], d=d+1) or valid(levels[:i+1] + levels[i+2:], d=d+1):
                return True
            return False
        sign_sum += delta // abs(delta)
    else:
        sign_okay = 1 if abs(sign_sum) == len(deltas) else 0
        if sign_okay:
            return True
        else:
            if len(deltas) == sign_sum + 2: 
                i = [j for j in range(len(deltas)) if deltas[j] < 0][0]
                if valid(levels[:i] + levels[i+1:], d=d+1) or valid(levels[:i+1] + levels[i+2:], d=d+1):
                    return True
            if -len(deltas) == sign_sum - 2:
                i = [j for j in range(len(deltas)) if deltas[j] > 0][0]
                if valid(levels[:i] + levels[i+1:], d=d+1) or valid(levels[:i+1] + levels[i+2:], d=d+1):
                    return True
            return False        


def two(lines):
    num_safe = 0
    for report in lines:
        levels = [int(x) for x in report.split(" ")]
        if valid(levels):
            num_safe += 1
    return num_safe
