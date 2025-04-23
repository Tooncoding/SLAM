def compute_value_map(grid, game_status, phi=0.9, iterations=100):
    WIDTH = 8
    value_map = [0.0] * (WIDTH * WIDTH)
    reward = [-1.0] * (WIDTH * WIDTH)

    for i in range(WIDTH * WIDTH):
        tile = grid.map[i // WIDTH][i % WIDTH]
        if tile == 'B':
            reward[i] = -100.0
        elif tile == 'W':
            reward[i] = 10.0
        elif tile == 'L':
            reward[i] = -30.0
        elif tile == '1':
            reward[i] = -30.0

    index = grid.locate(grid.robot_position)

    if index is not None:
        x = index % 8
        y = index // 8
        neighbors = [
            (x - 1, y), (x + 1, y),
            (x, y - 1), (x, y + 1)
        ]
        for nx, ny in neighbors:
            if 0 <= nx < 8 and 0 <= ny < 8:
                n_index = ny * 8 + nx
                if game_status == "Lucky Enough!":
                    reward[n_index] += 40.0
                elif game_status == "Danger!":
                    reward[n_index] -= 50.0
                    grid.mark_tile(n_index, "L")

    for _ in range(iterations):
        new_values = value_map[:]
        for s in range(WIDTH * WIDTH):
            neighbors = []
            if s % WIDTH > 0:
                n = s - 1
                if grid.map[n // WIDTH][n % WIDTH] != "B":
                    neighbors.append(n)
            if s % WIDTH < WIDTH - 1:
                n = s + 1
                if grid.map[n // WIDTH][n % WIDTH] != "B":
                    neighbors.append(n)
            if s // WIDTH > 0:
                n = s - WIDTH
                if grid.map[n // WIDTH][n % WIDTH] != "B":
                    neighbors.append(n)
            if s // WIDTH < WIDTH - 1:
                n = s + WIDTH
                if grid.map[n // WIDTH][n % WIDTH] != "B":
                    neighbors.append(n)

            if neighbors:
                best = max([reward[n] + phi * value_map[n] for n in neighbors])
                new_values[s] = best
            else:
                new_values[s] = reward[s]
        value_map = new_values
    # Debug highest value
    best_index = max(range(WIDTH * WIDTH), key=lambda i: value_map[i])
    print(f"🔍 Highest value tile: ({best_index % WIDTH}, {best_index // WIDTH}) → Value: {value_map[best_index]:.2f}")
    # print(value_map)
    return value_map, reward


def decide_next_move(grid, chance, pos, value_map, reward):
    index = grid.locate(pos)
    if index is None:
        print("❌ Robot position not found on grid. Defaulting to AVOID.")
        return "AVOID"

    policy_map = extract_policy(grid, value_map, reward)
    direction = policy_map[index]

    move_lookup = {
        "UP": "F",
        "DOWN": "B",
        "LEFT": "L",
        "RIGHT": "R"
    }

    move = move_lookup.get(direction, "AVOID")
    print(f"🔍 Chosen direction: {direction} → Command: {move}")
    return move

def extract_policy(grid, value_map, reward, gamma=0.9):
    WIDTH = 8
    policy_map = ["NONE"] * (WIDTH * WIDTH)

    for s in range(WIDTH * WIDTH):
        x, y = s % WIDTH, s // WIDTH
        best_dir = None
        best_val = float('-inf')

        neighbors = {
            "UP": (x, y + 1),
            "DOWN": (x, y - 1),
            "LEFT": (x - 1, y),
            "RIGHT": (x + 1, y)
        }

        for direction, (nx, ny) in neighbors.items():
            if 0 <= nx < WIDTH and 0 <= ny < WIDTH:
                n = ny * WIDTH + nx
                if grid.map[ny][nx] != "B":
                    val = reward[n] + gamma * value_map[n]
                    if val > best_val:
                        best_val = val
                        best_dir = direction

        policy_map[s] = best_dir if best_dir else "NONE"
    print(policy_map)
    return policy_map
