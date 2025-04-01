def count_xmas_patterns(grid):
    rows = len(grid)
    cols = len(grid[0])
    count = 0
    
    # Check each possible center position
    for r in range(1, rows - 1):  # Skip first and last rows
        for c in range(1, cols - 1):  # Skip first and last columns
            # Check if center is 'A'
            if grid[r][c] != 'A':
                continue
                
            # Check all possible X patterns with 'M' and 'S'
            # Pattern 1: M.S (forward-forward)
            #            .A.
            #            M.S
            if (grid[r-1][c-1] == 'M' and grid[r-1][c+1] == 'S' and
                grid[r+1][c-1] == 'M' and grid[r+1][c+1] == 'S'):
                count += 1
                
            # Pattern 2: S.M (backward-backward)
            #            .A.
            #            S.M
            if (grid[r-1][c-1] == 'S' and grid[r-1][c+1] == 'M' and
                grid[r+1][c-1] == 'S' and grid[r+1][c+1] == 'M'):
                count += 1
                
            # Pattern 3: M.S (forward-backward)
            #            .A.
            #            S.M
            if (grid[r-1][c-1] == 'M' and grid[r-1][c+1] == 'S' and
                grid[r+1][c-1] == 'S' and grid[r+1][c+1] == 'M'):
                count += 1
                
            # Pattern 4: S.M (backward-forward)
            #            .A.
            #            M.S
            if (grid[r-1][c-1] == 'S' and grid[r-1][c+1] == 'M' and
                grid[r+1][c-1] == 'M' and grid[r+1][c+1] == 'S'):
                count += 1
                
            # New + patterns:
            # Pattern 5: .M. (vertical-horizontal)
            #            SAS
            #            .M.
            if (grid[r][c-1] == 'S' and grid[r][c+1] == 'S' and
                grid[r-1][c] == 'M' and grid[r+1][c] == 'M'):
                count += 1
                
            # Pattern 6: .S. (horizontal-vertical)
            #            MAM
            #            .S.
            if (grid[r][c-1] == 'M' and grid[r][c+1] == 'M' and
                grid[r-1][c] == 'S' and grid[r+1][c] == 'S'):
                count += 1
    
    return count

# Read input
grid = []
with open('lines.txt', 'r') as file:
    for line in file:
        grid.append(list(line.strip()))

result = count_xmas_patterns(grid)
print(f"Number of X-MAS patterns: {result}")
