import random
import sys
from PIL import Image
import numpy as np
import os, os.path
import time

ROWS, COLUMNS, MAX, JUMP_BEFORE_WALK, CONVERT = range(5)
DEFAULT = [100, 100, 0, 0, 1]
DEFAULT[MAX] = int((DEFAULT[ROWS] * DEFAULT[COLUMNS]) / 2)

class Matrix:
	FILLED_POINT_TILE = "#"
	EMPTY_POINT_TILE = " "
	CENTER_TILE = "!"
	PADDING = 2
	MAX_WALK_BEFORE_JUMP = 0

	def __init__(self, rows =100, columns =300):
		self.rows = rows
		self.columns = columns

		self.matrix = self.generate_matrix()

	def generate_matrix(self):
		return [[Matrix.FILLED_POINT_TILE] * self.columns for _ in range(self.rows)]
	
	def get_midway_position(self):
		return int(self.rows / 2), int(self.columns / 2)
	
	def get_new_position(self, current_x, current_y):
		x, y = current_x, current_y

		roll = random.randint(1, 4)

		if roll == 1 and x > Matrix.PADDING:
			x -= 1
		if roll == 2 and x < self.rows - 1 - Matrix.PADDING:
			x += 1
		if roll == 3 and y > Matrix.PADDING:
			y -= 1
		if roll == 4 and y < self.columns - 1 - Matrix.PADDING:
			y += 1

		return x, y
	
	def get_random_position(self, tile_type =None):
		if tile_type:
			while True:
				x, y = self.get_random_position()
				
				x_not_on_padding = x > Matrix.PADDING and x < self.rows - Matrix.PADDING
				y_not_on_padding = y > Matrix.PADDING and y < self.columns - Matrix.PADDING
				match_correct_tile_type = self.matrix[x][y] == tile_type
				
				if x_not_on_padding and y_not_on_padding and match_correct_tile_type:
					return x, y
		else:
			return random.randint(0, self.rows - 1), random.randint(0, self.columns -1)

	def generate(self, max_empty_tiles, convert_to_image =False):
		amount = max_empty_tiles
		print(amount)
		x, y = self.get_midway_position()

		if Matrix.MAX_WALK_BEFORE_JUMP == 0:
			max_walk = max_empty_tiles
		else:
			max_walk = Matrix.MAX_WALK_BEFORE_JUMP
		
		count = 0

		while amount:
			if self.matrix[x][y] == Matrix.FILLED_POINT_TILE:
				if amount == max_empty_tiles:
					self.matrix[x][y] = Matrix.CENTER_TILE
				else:
					self.matrix[x][y] = Matrix.EMPTY_POINT_TILE
				amount -= 1
				count += 1

			if count == max_walk:
				x, y = self.get_random_position(tile_type=Matrix.FILLED_POINT_TILE)
				count = 0
			else:
				x, y = self.get_new_position(x, y)
		
		if convert_to_image:
			self.convert_to_img()

	def show(self):
		for row in self.matrix:
			print("".join(row))
	
	def get_random_color(self):
		return random.randint(0, 250), random.randint(0, 250), random.randint(0, 250)

	def save_image(self, image):
		base_path = os.path.split(sys.argv[0])[0]
		directory_to_save = os.path.join(base_path, "gen")

		if not os.path.isdir(directory_to_save):
			os.makedirs(directory_to_save)
		
		name = f"IMG {time.time()}.png"
		image_path = os.path.join(directory_to_save, "gend.png")

		image.save(image_path)
		
	def convert_to_img(self):
		matrix = [[(255, 255, 255) for _ in range(self.columns)] for _ in range(self.rows)]

		for x in range(self.rows):
			for y in range(self.columns):
				if self.matrix[x][y] == Matrix.EMPTY_POINT_TILE:
					matrix[x][y] = (0, 0, 0)
				
				if self.matrix[x][y] == Matrix.CENTER_TILE:
					matrix[x][y] = (252, 3, 61)
		
		matrix = np.asarray(matrix, dtype=np.uint8)
		img = Image.fromarray(matrix)	

		self.save_image(img)

def check_settings(settings):
	l = len(settings)
	for x in range(l, 5):
		settings.append(DEFAULT[x])
	
	return settings

settings = check_settings([int(x) for x in sys.argv[1:]])
print(settings)

cave = Matrix(settings[ROWS], settings[COLUMNS])
Matrix.MAX_WALK_BEFORE_JUMP = settings[JUMP_BEFORE_WALK]
cave.generate(settings[MAX], settings[CONVERT])