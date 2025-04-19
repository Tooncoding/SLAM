def update_risk(position, stat, grid, risk, chance):
    grid_id = grid.locate(position)

    # Edge-sensitive tile adjustments
    edge_tiles = {
        "topleft": 0, "topright": 7, "bottomleft": 56, "bottomright": 63,
        "top": list(range(1, 7)), "left": [8,16,24,32,40,48],
        "right": [15,23,31,39,47,55], "bottom": [57,58,59,60,61,62]
    }

    def mark(matrix, idx, dirs):
        if 0 <= idx < 64:
            for d in dirs:
                matrix[idx][d] = True

    if stat == -1:
        target = risk
    elif stat == 1:
        target = chance
    else:
        return

    if grid_id == edge_tiles["topleft"]:
        mark(target, grid_id + 1, [0])
        mark(target, grid_id + 8, [3])
    elif grid_id == edge_tiles["topright"]:
        mark(target, grid_id - 1, [1])
        mark(target, grid_id + 8, [3])
    elif grid_id == edge_tiles["bottomleft"]:
        mark(target, grid_id + 1, [0])
        mark(target, grid_id - 8, [2])
    elif grid_id == edge_tiles["bottomright"]:
        mark(target, grid_id - 1, [1])
        mark(target, grid_id - 8, [2])
        mark(target, grid_id + 8, [3])
    elif grid_id in edge_tiles["top"]:
        mark(target, grid_id + 1, [0])
        mark(target, grid_id - 1, [1])
        mark(target, grid_id + 8, [3])
    elif grid_id in edge_tiles["left"]:
        mark(target, grid_id + 1, [0])
        mark(target, grid_id + 8, [3])
        mark(target, grid_id - 8, [2])
    elif grid_id in edge_tiles["right"]:
        mark(target, grid_id - 1, [1])
        mark(target, grid_id + 8, [3])
        mark(target, grid_id - 8, [2])
    elif grid_id in edge_tiles["bottom"]:
        mark(target, grid_id - 1, [1])
        mark(target, grid_id + 1, [0])
        mark(target, grid_id - 8, [2])
    else:
        # center tiles
        mark(target, grid_id + 1, [0])
        mark(target, grid_id - 1, [1])
        mark(target, grid_id - 8, [2])
        mark(target, grid_id + 8, [3])
