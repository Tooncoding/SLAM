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

        self.map = [['0' for _ in range(width)] for _ in range(height)]
        self.tiles = self._generate_tile_list()

    def _generate_tile_list(self):
        tile_list = []
        for y in range(-120, 100, 25):
            for x in range(-100, 100, 25):
                x_min = x / 100
                x_max = x_min + 0.25
                y_min = y / 100
                y_max = y_min + 0.25
                tile_list.append([[x_min, x_max], [y_min, y_max]])
        return tile_list

    def locate(self, pos):
        for idx, tile in enumerate(self.tiles):
            x_min, x_max = tile[0]
            y_min, y_max = tile[1]

            # Flip X: mirror horizontally
            flipped_x_min = -x_max
            flipped_x_max = -x_min

            # Y flip: keep tile bounds but invert coordinate check
            if flipped_x_min <= -pos[0] <= flipped_x_max and y_min <= pos[1] <= y_max:
                return idx
        return None

    def get_tile_bounds(self, index):
        return self.tiles[index] if 0 <= index < self.total_tiles else None

    def update_robot_position(self, pos, game_status):
        grid = self.locate(pos)
        if grid is None:
            return

        self._clear_previous_robot()

        x = grid % self.width
        y = grid // self.width
        self.map[y][x] = "R"

        # Check and mark neighboring tiles based on game status
        neighbors = [
            (x - 1, y), (x + 1, y),
            (x, y - 1), (x, y + 1)
        ]

        for nx, ny in neighbors:
            if 0 <= nx < self.width and 0 <= ny < self.height:
                current = self.map[ny][nx]
                if current == '0':  # Only mark unvisited tiles
                    if game_status == "Danger!":
                        self.map[ny][nx] = "D"
                    elif game_status == "Lucky Enough!":
                        self.map[ny][nx] = "C"


    def mark_tile(self, index, symbol):
        if 0 <= index < self.total_tiles:
            self.map[index // self.width][index % self.width] = symbol

    def _clear_previous_robot(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.map[y][x] == "R":
                    self.map[y][x] = '1'

    def print_map(self):
        for row in reversed(self.map):
            print(*row)

    def mark_batch(self, indices, symbol):
        for idx in indices:
            self.mark_tile(idx, symbol)

    def get_region_bounds(self, indices):
        return [self.get_tile_bounds(i) for i in indices]

    def get_tile_center(self, index):
        tile = self.get_tile_bounds(index)
        if tile:
            x = (tile[0][0] + tile[0][1]) / 2
            y = (tile[1][0] + tile[1][1]) / 2
            return [x, y]
        return None
