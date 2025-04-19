# grid_manager.py

class GridManager:
    def __init__(self, width, height, start_x, start_y, tile_w, tile_h):
        self.width = width
        self.height = height
        self.start_x = start_x
        self.start_y = start_y
        self.tile_w = tile_w
        self.tile_h = tile_h
        self.total_tiles = width * height

        self.map = [[0 for _ in range(width)] for _ in range(height)]
        self.tiles = self._generate_tile_list()

    def _generate_tile_list(self):
        tile_list = []
        for y1 in range(-120, 100, 25):
            for x1 in range(-100, 100, 25):
                tile_list.append([[x1 / 100, x1 / 100 + 0.25], [y1 / 100, y1 / 100 + 0.25]])
        return tile_list

    def locate(self, pos):
        for idx, tile in enumerate(self.tiles):
            if tile[0][0] <= pos[0] <= tile[0][1] and tile[1][0] <= pos[1] <= tile[1][1]:
                return idx
        return None

    def get_tile_bounds(self, index):
        return self.tiles[index] if 0 <= index < self.total_tiles else None

    def update_robot_position(self, pos):
        grid = self.locate(pos)
        if grid is None:
            return
        self._clear_previous_robot()
        self.map[grid // self.width][grid % self.width] = "R"

    def mark_tile(self, index, symbol):
        if 0 <= index < self.total_tiles:
            self.map[index // self.width][index % self.width] = symbol

    def _clear_previous_robot(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.map[y][x] == "R":
                    self.map[y][x] = 1

    def print_map(self):
        for row in reversed(self.map):
            print(*row)
