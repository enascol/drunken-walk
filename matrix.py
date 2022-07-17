""" Module to generate and process matrix of characteres """

import os
import os.path
import sys
import random
import time

from PIL import Image
import numpy as np

import paths


class Matrix:
    """ Generates a matrix that can be converted to a .png file.

    The matrix will be  generated with the dimensions specified
    on the config file.

    Example:
        - Matrix with 3 rows and 5 columns before being processed

        #####
        #####
        #####
    """
    FILLED_POINT_TILE = "#"
    EMPTY_POINT_TILE = " "
    CENTER_TILE = "!"
    FILLED_PIXELS_PER_JUMP = 0
    SYMBOLS = [f"S{x}" for x in range(100000)]

    def __init__(self, settings):
        self.settings = settings
        self.rows = self.settings["rows"]
        self.columns = self.settings["columns"]

        self._set_pixels_per_jump()

        self.matrix = self.initialize_matrix()

    def _set_pixels_per_jump(self):
        max_pixels = self.settings["max_pixels"]
        jumps = self.settings["jumps"]

        Matrix.FILLED_PIXELS_PER_JUMP = int(max_pixels / jumps)

    def initialize_matrix(self):
        """ Initialize the matrix with the given dimension"""

        print("Initializing matrix...", end=" ")
        start = time.time()

        filled = [Matrix.FILLED_POINT_TILE]
        matrix = [filled * self.columns for _ in range(self.rows)]

        print(f"done in {time.time() - start} seconds")
        return matrix

    def get_midway_position(self):
        """ Get the coordinations of the middle point of the matrix """

        return int(self.rows / 2), int(self.columns / 2)

    def get_new_position(self, current_x, current_y):
        """ Gets new coords based on the given ones """

        new_x, new_y = current_x, current_y
        rows, columns = self.rows, self.columns
        roll = random.randint(1, 4)

        if roll == 1 and current_x > self.settings["padding"]:
            new_x -= 1
        if roll == 2 and current_x < rows - 1 - self.settings["padding"]:
            new_x += 1
        if roll == 3 and current_y > self.settings["padding"]:
            new_y -= 1
        if roll == 4 and current_y < columns - 1 - self.settings["padding"]:
            new_y += 1

        return new_x, new_y

    def get_random_position(self, tile_type=None):
        """ Gets a random coordinate.

        if a tile_type is passed then the coordinate
        must have a match character.
        """

        if tile_type:
            pad = self.settings["padding"]

            while True:
                rand_x, rand_y = self.get_random_position()
                current_tile = self.matrix[rand_x][rand_y]

                x_not_padding = rand_x > pad and rand_x < self.rows - pad
                y_not_padding = rand_y > pad and rand_y < self.columns - pad
                match_correct_tile_type = current_tile == tile_type

                if x_not_padding and y_not_padding and match_correct_tile_type:
                    return rand_x, rand_y
        else:
            rand_x = random.randint(0, self.rows - 1)
            rand_y = random.randint(0, self.columns - 1)

            return rand_x, rand_y

    def generate(self, max_empty_tiles, convert_to_image=False):
        """Generates all the possible tiles(characters) in the matrix

        These characteres are:
            - # : filled tile
            - ' ' : empty tile
            - ! : center tile
            - 'S1', 'S2', 'S3', etc : color tiles
        """

        print("Generating characters...", end=" ")
        start = time.time()
        amount = max_empty_tiles

        if self.settings["start_from_center"]:
            current_x, current_y = self.get_midway_position()
        else:
            tile_type = Matrix.FILLED_POINT_TILE
            current_x, current_y = self.get_random_position(tile_type)

        symbol_count = 0

        if Matrix.FILLED_PIXELS_PER_JUMP == 0:
            max_walk = max_empty_tiles
        else:
            max_walk = Matrix.FILLED_PIXELS_PER_JUMP

        count = 0

        while amount:
            if self.matrix[current_x][current_y] == Matrix.FILLED_POINT_TILE:
                red_gen_start = self.settings["red_gen_start"]

                if amount == max_empty_tiles and red_gen_start:
                    self.matrix[current_x][current_y] = Matrix.CENTER_TILE
                elif count == 0 and self.settings["red_gen_start"]:
                    self.matrix[current_x][current_y] = Matrix.CENTER_TILE
                else:
                    if self.settings["monochromatic"]:
                        empty_tile = Matrix.EMPTY_POINT_TILE
                        self.matrix[current_x][current_y] = empty_tile
                    else:
                        symbol = Matrix.SYMBOLS[symbol_count]
                        self.matrix[current_x][current_y] = symbol
                amount -= 1
                count += 1

            if count == max_walk:
                tile_type = Matrix.FILLED_POINT_TILE
                current_x, current_y = self.get_random_position(tile_type)

                count = 0
                symbol_count += 1
            else:
                new_coord = self.get_new_position(current_x, current_y)
                current_x, current_y = new_coord

        print(f"done in {time.time() - start} seconds")
        if convert_to_image:
            self.convert_to_img()

        if self.settings["save_matrix"]:
            self._save_matrix()

    def show(self):
        """ Print the matrix """
        for row in self.matrix:
            print("".join(row))

    def get_random_color(self):
        """ Gets a random RGB value """
        return [random.randint(0, 250) for _ in range(3)]

    def save_image(self, image):
        """ Saves the image generated from the matrix.

        Saves the image to the gen folder created in the
        directory where this script is being ran.

        If "create_new_file" is set to 0 then tbe image
        will be saved to the same file instead of creating
        a new one.
        """
        base_path = os.path.split(sys.argv[0])[0]
        directory_to_save = os.path.join(base_path, "gen")

        if not os.path.isdir(directory_to_save):
            os.makedirs(directory_to_save)

        if self.settings["create_new_file"]:
            name = f"IMG {time.time()}.png"
        else:
            name = "gend.png"

        image_path = os.path.join(directory_to_save, name)

        image.save(image_path)

    def _save_matrix(self):
        matrixes_path = paths.MATRIXES_PATH

        if not os.path.isdir(matrixes_path):
            os.makedirs(matrixes_path)

        matrix_string = []

        for row in self.matrix:
            matrix_string.append("".join(row))

        matrix_string = "\n".join(matrix_string)

        matrix_name = f"M{time.time()}"
        matrix_path = os.path.join(matrixes_path, matrix_name)

        with open(matrix_path, "w+") as mf:
            mf.write(matrix_string)

    def _generate_color_grid(self):
        columns = range(self.columns)
        rows = range(self.rows)
        black = (255, 255, 255)

        grid = [[black for _ in columns] for _ in rows]

        return grid

    def convert_to_img(self):
        """ Converts the previously generated matrix to a png file """

        print("Generating colored matrix", end=" ")

        start = time.time()
        fixed_bg = self.settings["fixed_bg"]

        matrix = self._generate_color_grid()

        colors = {}

        for x in range(self.rows):
            for y in range(self.columns):
                if self.matrix[x][y] == Matrix.CENTER_TILE:
                    matrix[x][y] = (252, 3, 61)
                else:
                    if self.matrix[x][y] == Matrix.EMPTY_POINT_TILE:
                        matrix[x][y] = (0, 0, 0)
                    else:
                        filled_tile = Matrix.FILLED_POINT_TILE
                        if self.matrix[x][y] == filled_tile and fixed_bg:
                            matrix[x][y] == (255, 255, 255)
                        else:
                            symbol = self.matrix[x][y]
                            try:
                                matrix[x][y] = colors[symbol]
                            except KeyError:
                                colors[symbol] = self.get_random_color()
                                matrix[x][y] = colors[symbol]

        numpy_matrix = np.asarray(matrix, dtype=np.uint8)
        img = Image.fromarray(numpy_matrix)
        self.save_image(img)

        print(f"done in {time.time() - start} seconds")
