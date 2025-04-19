# vision.py (class-based, requires robot input)

class VisionProcessor:
    def __init__(self, robot):
        self.camera = robot.getDevice("camera")
        self.camera.enable(int(robot.getBasicTimeStep()))
        self.color_ranges = {
            1: ([253, 236, 253], [253, 240, 253]),
            2: ([226, 0, 0],     [228, 255, 255]),
            3: ([222, 253, 253], [225, 255, 255]),
            4: ([238, 255, 250], [243, 255, 250]),
            5: ([253, 250, 0],   [253, 255, 255]),
            6: ([231, 120, 120], [233, 255, 255]),
            7: ([253, 170, 200], [253, 200, 255]),
            8: ([213, 195, 200], [220, 199, 202])
        }

    def match_color(self, rgb):
        for label, (low, high) in self.color_ranges.items():
            if all(low[i] < rgb[i] < high[i] for i in range(3)):
                return label
        return 0

    def pixel_area(self, label):
        if label not in self.color_ranges:
            return 0
        low, high = self.color_ranges[label]
        image = self.camera.getImageArray()
        return sum(
            1 for row in image for px in row
            if all(low[i] < px[i] < high[i] for i in range(3))
        )

    def get_center_pixel_color(self):
        img = self.camera.getImageArray()
        w, h = self.camera.getWidth(), self.camera.getHeight()
        return img[h // 2][w // 2]

    def row_match(self, area_count):
        thresholds = [
            (38000, "row1"),
            (20000, "row2"),
            (10000, "row3"),
            (7000,  "row4"),
            (4000,  "row5"),
            (2700,  "row6"),
            (2000,  "row7"),
            (0,     "row8")
        ]
        for threshold, label in thresholds:
            if area_count > threshold:
                return label
        return "row8"
