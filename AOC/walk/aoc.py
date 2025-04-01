"""
TODO: SALES_TARGETS USECASE??

- [x] use a set for O(1) lookup, and queue for popping
- [x] break early
- [x] cache map lookup
- [x] watch out with creating new lists
    - list comprehension
    - concatenating lists
    - slicing
- [x] enumerate instead of double lookup with range

- [ ] access global variable in loop    
- [ ] join is way faster than concatenating strings


- set lookup
- break early
- cache map lookup

Spending a lot of time in the comparison could also mean I am spending

spending a lot of time comparing -> break early
memcmp -> compare the actual contents of strings, sets use hash comparison first, which can avoid the full string comparison. In addition, it has O(1) lookup
c

"""



def solve1(page):
    total = 0
    rules = {} 
    parsing_rules = True # the start of the page contains the rules
    for line in page.splitlines():                                          

        if line == "":
            parsing_rules = False
            continue # skip the whiteline

        if parsing_rules:
            x, y = line.split("|")
            rules[x] = rules.get(x, []) + [y]                               # TODO: do I create a new list here every time?
                                                                            # TODO: make the values into a set for O(1) lookup
        else: 
            update = line.split(",")
            valid_update = True
            for i in range(len(update)):                                    # TODO: enumerate so you dont have to get update[i]
                for j in range(i + 1, len(update)):
                    if update[j] not in rules.get(update[i]):           # TODO: don't get rule[update[i]] on every j loop
                        valid_update = False                                # TODO: instead of switching bool, break early
                                                                            # TODO: extract is_valid into own function after early breaking to see its performance 
            if valid_update:
                total += int(update[len(update) // 2])                     
    return total

# break early, b/c richcompare
def solve2(page):
    total = 0
    rules = {} 
    parsing_rules = True # the start of the page contains the rules
    for line in page.splitlines():                                          

        if line == "":
            parsing_rules = False
            continue # skip the whiteline

        if parsing_rules:
            x, y = line.split("|")
            rules[x] = rules.get(x, []) + [y]
        else: 
            update = line.split(",")
            for i in range(len(update)):
                for j in range(i + 1, len(update)):
                    if update[j] not in rules.get(update[i]):
                        break  # break inner loop when invalid pair found
                else:
                    continue  # if inner loop completed without break, continue outer loop
                break  # if inner loop broke, break outer loop too
            else:
                # if outer loop completed without break, update is valid
                total += int(update[len(update) // 2])
    return total

# set instead of list
def solve3(page):
    total = 0
    rules = {} 
    parsing_rules = True # the start of the page contains the rules
    for line in page.splitlines():                                          

        if line == "":
            parsing_rules = False
            continue # skip the whiteline

        if parsing_rules:
            x, y = line.split("|")
            if x not in rules:
                rules[x] = set()
            rules[x].add(y)
        else: 
            update = line.split(",")
            for i in range(len(update)):
                for j in range(i + 1, len(update)):
                    if update[j] not in rules.get(update[i]):
                        break
                else:
                    continue
                break
            else:
                total += int(update[len(update) // 2])
    return total


# Caching map lookup
def solve(page):
    total = 0
    rules = {} 
    parsing_rules = True # the start of the page contains the rules
    for line in page.splitlines():                                          

        if line == "":
            parsing_rules = False
            continue # skip the whiteline

        if parsing_rules:
            x, y = line.split("|")
            if x not in rules:
                rules[x] = set()
            rules[x].add(y)
        else: 
            update = line.split(",")
            for i in range(len(update)):
                rule_i = rules.get(update[i])
                for j in range(i + 1, len(update)):
                    if update[j] not in rule_i:
                        break
                else:
                    continue
                break
            else:
                total += int(update[len(update) // 2])
    return total
    