# tools/decision_engine.py

def decide_next_move(grid, risk, chance, pos, goal_index):
    """
    Placeholder for pathfinding or strategic logic.
    Returns a command: e.g. "FORWARD", "AVOID", etc.
    """
    # Example logic (dumb): if in danger zone, avoid
    index = grid.locate(pos)
    if any(risk[index]):
        return "AVOID"
    return "FORWARD"
