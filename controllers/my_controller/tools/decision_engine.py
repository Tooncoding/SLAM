def compute_value_map(grid, game_status, risk, phi=0.9, iterations=20):
    WIDTH = 8
    value_map = [0.0] * (WIDTH * WIDTH)
    reward = [-1.0] * (WIDTH * WIDTH)

    for i in range(WIDTH * WIDTH):
        tile = grid.map[i // WIDTH][i % WIDTH]
        if tile == "B":
            reward[i] = -100.0
        elif tile == "W":
            reward[i] = 100.0
        elif tile == "L":
            reward[i] = -50.0
        elif any(risk[i]):
            reward[i] -= 5.0

    if game_status == "Lucky Enough!":
        reward[grid.locate(grid.robot_position)] += 10.0
    elif game_status == "Danger!":
        reward[grid.locate(grid.robot_position)] -= 10.0

    for _ in range(iterations):
        new_values = value_map[:]
        for s in range(WIDTH * WIDTH):
            neighbors = []
            if s % WIDTH > 0: neighbors.append(s - 1)
            if s % WIDTH < WIDTH - 1: neighbors.append(s + 1)
            if s // WIDTH > 0: neighbors.append(s - WIDTH)
            if s // WIDTH < WIDTH - 1: neighbors.append(s + WIDTH)
            best = max([reward[n] + phi * value_map[n] for n in neighbors], default=value_map[s])
            new_values[s] = best
        value_map = new_values
    return value_map


def decide_next_move(grid, risk, chance, pos, value_map):
    index = grid.locate(pos)
    cx, cy = index % 8, index // 8

    neighbors = {
        "UP": (cx, cy - 1),
        "DOWN": (cx, cy + 1),
        "LEFT": (cx - 1, cy),
        "RIGHT": (cx + 1, cy)
    }

    valid_moves = {}
    for direction, (nx, ny) in neighbors.items():
        if 0 <= nx < 8 and 0 <= ny < 8:
            if grid.map[ny][nx] != "B":
                idx = ny * 8 + nx
                valid_moves[direction] = value_map[idx]

    if not valid_moves:
        return "AVOID"

    best_direction = max(valid_moves, key=valid_moves.get)

    move_lookup = {
        "UP": "F",
        "DOWN": "B",
        "LEFT": "L",
        "RIGHT": "R"
    }

    return move_lookup.get(best_direction, "F")

