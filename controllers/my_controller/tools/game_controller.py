# tools/game_controller.py

from tools.decision_engine import decide_next_move

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
        self.win_tile = self.grid.get_tile_bounds(all_tiles[6])
        self.lose_tiles = self.grid.get_region_bounds(all_tiles[0:6])
        self.previous_index = None
        self.next_move = None
        self.game_status = None

    def is_within(self, pos, bounds):
        return bounds[0][0] <= pos[0] <= bounds[0][1] and bounds[1][0] <= pos[1] <= bounds[1][1]

    def check_game_state(self, pos):
        for bounds in self.lose_tiles:
            if self.is_within(pos, bounds):
                print("you lost")
                return "lose"
        if self.is_within(pos, self.win_tile):
            print("win")
            return "win"
        return "ongoing"
    
    def decide_next_move(self, pos):
        self.next_move = decide_next_move(
            self.grid,
            self.risk,
            self.chance,
            pos,
            self.all_tiles[6]  # win tile index
        )

    def execute_move(self):
        command = self.next_move
        print("Execute move:", command)
        self.agent.execute(command)

    def step(self, pos):
        current_index = self.grid.locate(pos)

        # Capture current camera frame
        self.camera.saveImage("test.jpg", 100)

        # Perception
        color = self.vision.get_center_pixel_color()
        label = self.vision.match_color(color)

        # Game status based on surroundings
        st = 0
        lose_set = set(self.all_tiles[0:6])
        win_tile = self.all_tiles[6]
        neighbors = [current_index + 8, current_index - 8, current_index + 1, current_index - 1]

        if any(n in lose_set for n in neighbors):
            st = -1
            self.game_status = "Danger!"
        elif any(n == win_tile for n in neighbors):
            st = 1
            self.game_status = "Lucky Enough!"
        else:
            self.game_status = "Still Safe"

        # Risk model update
        self.update_risk(pos, st, self.grid, self.risk, self.chance)

        # Decision + Action
        self.decide_next_move(pos)
        self.execute_move()

        # Visual feedback (only if moved to a new tile)
        if current_index != self.previous_index:
            self.grid.update_robot_position(pos)
            self.grid.print_map()
            self.previous_index = current_index
            print(f"Current game status: {self.game_status}")

        # Mark global risk and chance
        for i, state in enumerate(self.risk):
            if all(state):
                self.grid.mark_tile(i, "L")
        for i, state in enumerate(self.chance):
            if all(state):
                self.grid.mark_tile(i, "W")

        return self.check_game_state(pos)

