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
                        break  # break inner loop when invalid pair found
                else:
                    continue  # if inner loop completed without break, continue outer loop
                break  # if inner loop broke, break outer loop too
            else:
                # if outer loop completed without break, update is valid
                total += int(update[len(update) // 2])
    return total
