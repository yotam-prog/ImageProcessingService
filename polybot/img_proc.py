import random
from pathlib import Path
from matplotlib.image import imread, imsave


def rgb2gray(rgb):
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return gray


class Img:

    def __init__(self, path):
        """
        Do not change the constructor implementation
        """
        self.path = Path(path)
        self.data = rgb2gray(imread(path)).tolist()

    def save_img(self):
        """
        Do not change the below implementation
        """
        new_path = self.path.with_name(self.path.stem + '_filtered' + self.path.suffix)
        imsave(new_path, self.data, cmap='gray')
        return new_path

    def blur(self, blur_level=16):

        height = len(self.data)
        width = len(self.data[0])
        filter_sum = blur_level ** 2

        result = []
        for i in range(height - blur_level + 1):
            row_result = []
            for j in range(width - blur_level + 1):
                sub_matrix = [row[j:j + blur_level] for row in self.data[i:i + blur_level]]
                average = sum(sum(sub_row) for sub_row in sub_matrix) // filter_sum
                row_result.append(average)
            result.append(row_result)

        self.data = result

    def contour(self):
        for i, row in enumerate(self.data):
            res = []
            for j in range(1, len(row)):
                res.append(abs(row[j-1] - row[j]))

            self.data[i] = res

    def rotate(self):
        height = len(self.data)
        width = len(self.data[0])
        rotated_data = [[0] * height for _ in range(width)]
        for y in range(height):
            for x in range(width):
                rotated_data[x][y] = self.data[y][width - x - 1]
        self.data = rotated_data

    def salt_n_pepper(self):
        height = len(self.data)
        width = len(self.data[0])
        for y in range(height):
            for x in range(width):
                random_value = random.random()
                if random_value < 0.2:
                    self.data[y][x] = 255  # Salt
                elif random_value > 0.8:
                    self.data[y][x] = 0    # Pepper

    def concat(self, other_img):
        # TODO remove the `raise` below, and write your implementation
        raise NotImplementedError()

    def segment(self):
        height = len(self.data)
        width = len(self.data[0])

        for y in range(height):
            for x in range(width):
                if self.data[y][x] > 100:
                    self.data[y][x] = 255
                else:
                    self.data[y][x] = 0
