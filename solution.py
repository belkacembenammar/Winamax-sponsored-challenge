WIDTH, HEIGHT = [int(i) for i in input().split()]
FIELD = [['' for _ in range(WIDTH)] for _ in range(HEIGHT)]
HOLES = set()
BALLS = set()
paths = {}
path = []

BALL_POWER = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]

for i in range(HEIGHT):
    for j, c in enumerate(input()):
        FIELD[i][j] = c
        if c == 'H': HOLES.add((i, j))
        elif c.isdigit(): 
            BALLS.add((i, j))
            BALL_POWER[i][j] = int(c)

def is_hole(cell):
    return FIELD[cell[0]][cell[1]] == 'H'

def is_water(cell):
    return FIELD[cell[0]][cell[1]] == 'X'

def is_ball(cell):
    return (FIELD[cell[0]][cell[1]]).isdigit()

def get_neighbors(cell):
    a, b = cell[0], cell[1]
    neighbors = [(a - 1, b), (a + 1, b), (a, b + 1), (a, b - 1)]
    return [(x, y) for x, y in neighbors if 0 <= x < HEIGHT and 0 <= y < WIDTH and (x, y) not in path]

def is_changing_direction(path, n):
    return len(path) > 1 and (path[-1][0] - path[-2][0], path[-1][1] - path[-2][1]) != (n[0] - path[-1][0], n[1] - path[-1][1])

def ball_can_go_through_path(path, ball_power, is_complete = False):
    remaining_power = ball_power
    remaining_kicks = ball_power

    for i, c in enumerate(path[:-1]):
        changes_direction = is_changing_direction(path[0:i+1], path[i+1])

        if changes_direction and remaining_power > 0:
            return False
        
        if remaining_power == 0 or changes_direction:
            remaining_kicks -= 1
            remaining_power = remaining_kicks

        if remaining_power == 0 or remaining_kicks == 0:
            return False

        remaining_power -= 1
    
    if is_complete and remaining_power > 0:
        return False

    return True

def are_paths_overlapping(path1, path2):
    return not set(path1).isdisjoint(path2)
    
def are_overlapping(solution):
    for i, path1 in enumerate(solution):
        for path2 in solution[i+1:]:
            if are_paths_overlapping(path1, path2):
                return True
    return False

def is_correct_solution(solution): # APPROVED
    if len(solution) != len(BALLS):
        return False

    if are_overlapping(solution):
        return False
    
    return True

def produit(*lists):
    def has_overlap(product):
        for i, path1 in enumerate(product):
            for path2 in product[i+1:]:
                if are_paths_overlapping(path1, path2):
                    return True
        return False

    if lists:
        L, rest = lists[0], lists[1:]
        for x in L:
            for y in produit(*rest):
                product = tuple([x] + list(y))
                if not has_overlap(product):
                    yield product
    else:
        yield []

def find_valid_solution(paths_dict, solution = []):

    if len(solution) == len(BALLS):
        return solution
    
    filtering_completed = False

    while not filtering_completed:
        unique_ball_paths = {key: value[0] for key, value in paths_dict.items() if len(value) == 1}

        for ball_path in unique_ball_paths:
            unique_path = paths_dict[ball_path][0]
            solution.append(unique_path)

            for ball_key in paths_dict:
                ball_paths = paths_dict[ball_key]
                paths_dict[ball_key] = [p for p in ball_paths if not are_paths_overlapping(p, unique_path)]

            del paths_dict[ball_path]

        filtering_completed = len(unique_ball_paths) == 0

    counter = 0
    if (len(unique_ball_paths) == 0):
        all_possibilities = produit(*paths_dict.values())
        for s in all_possibilities:
            counter += 1
            if is_correct_solution(solution + list(s)):
                solution = solution + list(s)
                return solution
            
    return solution
            
def dfs(ball, ball_power):
    neighbors = get_neighbors(ball)
    for n in neighbors:
        if (len(path) > 0 and is_water(path[-1]) and is_changing_direction(path, n)):
            continue

        elif n in BALLS:
            continue

        elif not ball_can_go_through_path(path, ball_power):
            continue

        elif n in HOLES:
            path.append(n)
            if ball_can_go_through_path(path, ball_power, True):
                if path[0] not in paths:
                    paths[path[0]] = []

                paths[path[0]].append(path.copy())

        else :
            path.append(n)
            dfs(n, ball_power)

        path.remove(n)

def get_direction_char(start, target):
    dx = target[0] - start[0]
    dy = target[1] - start[1]

    if dx > 0:
        return "v"
    elif dx < 0:
        return "^"
    elif dy > 0:
        return ">"
    elif dy < 0:
        return "<"
    else:
        return '.'

for ball in BALLS:
    path.append(ball)
    ball_power = BALL_POWER[ball[0]][ball[1]]
    dfs(ball, ball_power)
    path.pop()

result = [['.' for _ in range(WIDTH)] for _ in range(HEIGHT)]
for p in find_valid_solution(paths):
    for j, cell in enumerate(p[:-1]):
        result[cell[0]][cell[1]] = get_direction_char(cell, p[j+1])

for row in result:
    print(''.join(row))