# tools/game_controller.py

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

    def step(self, pos):
        current_index = self.grid.locate(pos)

        # Save current camera view
        self.camera.saveImage("test.jpg", 100)

        # Check color
        color = self.vision.get_center_pixel_color()
        label = self.vision.match_color(color)
        #nprint("Color Label:", label)

        # Check proximity to lose/win tiles
        st = 0
        lose_set = set(self.all_tiles[0:6])
        win_tile = self.all_tiles[6]
        neighbors = [current_index + 8, current_index - 8, current_index + 1, current_index - 1]

        if any(n in lose_set for n in neighbors):
            st = -1
            game_message = "Danger!"
        elif any(n == win_tile for n in neighbors):
            st = 1
            game_message = "Lucky Enough!"
        else:
            game_message = "Still Safe"

        self.update_risk(pos, st, self.grid, self.risk, self.chance)

        if current_index != self.previous_index:
            self.grid.update_robot_position(pos)
            self.grid.print_map()
            self.previous_index = current_index
            print(game_message)

        # Mark risk/chance on the grid
        for i, state in enumerate(self.risk):
            if all(state):
                self.grid.mark_tile(i, "L")
        for i, state in enumerate(self.chance):
            if all(state):
                self.grid.mark_tile(i, "W")

        return self.check_game_state(pos)
