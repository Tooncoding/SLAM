# tools/game_controller.py

from tools.decision_engine import decide_next_move, compute_value_map

class GameController:
    def __init__(self, grid, vision, agent, all_tiles, update_risk_fn, risk_map, chance_map, camera):
        self.grid = grid
        self.vision = vision
        self.agent = agent
        self.all_tiles = all_tiles
        self.update_risk = update_risk_fn
        self.risk = risk_map
        self.chance = chance_map
        self.camera = camera
        self.previous_index = None
        self.next_move = None
        self.game_status = None
        self.value_map = [0.0] * 64  # initialize with neutral values

    def is_within(self, pos, bounds):
        return bounds[0][0] <= pos[0] <= bounds[0][1] and bounds[1][0] <= pos[1] <= bounds[1][1]

    def check_game_state(self, pos):
        for bounds in self.grid.get_region_bounds(self.all_tiles[0:6]):
            if self.is_within(pos, bounds):
                print("you lost")
                return "lose"
        win_bounds = self.grid.get_tile_bounds(self.all_tiles[6])
        if self.is_within(pos, win_bounds):
            print("win")
            return "win"
        return "ongoing"
    
    def decide_next_move(self, pos):
        self.grid.robot_position = pos  # attach for compute_value_map
        self.value_map, self.reward_map = compute_value_map(
            grid=self.grid,
            game_status=self.game_status,
        )
        self.next_move = decide_next_move(
            grid=self.grid,
            chance=self.chance,
            pos=pos,
            value_map=self.value_map,
            reward=self.reward_map
        )


    def execute_move(self):
        command = self.next_move
        print("Execute move:", command)

        # Get current tile
        index = self.grid.locate(self.grid.robot_position)
        x, y = index % 8, index // 8

        # Absolute map movement interpretation
        delta = {
            "L": (-1, 0),  # move left on map
            "R": (1, 0),   # move right on map
            "F": (0, 1),  # move up on map
            "B": (0, -1)    # move down on map
        }

        if command in delta:
            dx, dy = delta[command]
            nx, ny = x + dx, y + dy

            print(f"Robot at ({x},{y}) wants to go {command} → ({nx},{ny})")

            if not (0 <= nx < 8 and 0 <= ny < 8):
                print("⚠️ Blocked: off-grid.")
                return

            print(f"Tile content: {self.grid.map[ny][nx]}")

            if self.grid.map[ny][nx] == "B":
                print("⚠️ Blocked: wall at destination.")
                return

        self.agent.execute(command)


    def step(self, pos):
        index = self.grid.locate(pos)

        # Perception
        self.camera.saveImage("test.jpg", 100)
        color = self.vision.get_center_pixel_color()
        label = self.vision.match_color(color)

        # Local proximity awareness (robot doesn't know goal or lose globally)
        neighbors = [index + 8, index - 8, index + 1, index - 1]
        lose_set = set(self.all_tiles[0:6])
        win_tile = self.all_tiles[6]

        st = 0
        if any(n in lose_set for n in neighbors):
            st = -1
            self.game_status = "Danger!"
        elif any(n == win_tile for n in neighbors):
            st = 1
            self.game_status = "Lucky Enough!"
        else:
            self.game_status = "Still Safe"

        # Map update and printing if tile changed
        if index != self.previous_index:
            self.grid.update_robot_position(pos, self.game_status)
            self.grid.print_map()
            self.previous_index = index
            print(self.game_status)
            
        # Risk update (pass `st`)
        self.update_risk(pos, st, self.grid, self.risk, self.chance)

        # Value-based decision and action
        self.decide_next_move(pos)
        self.execute_move()

        # Mark L and W zones based on learned state
        for i, state in enumerate(self.risk):
            if all(state):
                self.grid.mark_tile(i, "L")
        for i, state in enumerate(self.chance):
            if all(state):
                self.grid.mark_tile(i, "W")

        return self.check_game_state(pos)
