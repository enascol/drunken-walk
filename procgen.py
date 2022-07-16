import random
import sys
from PIL import Image
import numpy as np
import os, os.path
import time

class Matrix:
	FILLED_POINT_TILE = "#"
	EMPTY_POINT_TILE = " "
	CENTER_TILE = "!"
	SYMBOLS = [f"S{x}" for x in range(100000)]

	def __init__(self, settings):
		self.settings = settings
		self.rows = self.settings["rows"]
		self.columns = self.settings["columns"]

		self.matrix = self.generate_matrix()

	def generate_matrix(self):
		print("Initializing matrix...", end =" ")
		start = time.time()
		matrix = [[Matrix.FILLED_POINT_TILE] * self.columns for _ in range(self.rows)]
		print(f"done in {time.time() - start} seconds")
		return matrix
	
	def get_midway_position(self):
		return int(self.rows / 2), int(self.columns / 2)
	
	def get_new_position(self, current_x, current_y):
		x, y = current_x, current_y

		roll = random.randint(1, 4)

		if roll == 1 and x > self.settings["padding"]:
			x -= 1
		if roll == 2 and x < self.rows - 1 - self.settings["padding"]:
			x += 1
		if roll == 3 and y > self.settings["padding"]:
			y -= 1
		if roll == 4 and y < self.columns - 1 - self.settings["padding"]:
			y += 1

		return x, y
	
	def get_random_position(self, tile_type =None):
		if tile_type:
			padding = self.settings["padding"]

			while True:
				x, y = self.get_random_position()
				
				x_not_on_padding = x > padding and x < self.rows - padding
				y_not_on_padding = y > padding and y < self.columns - padding
				match_correct_tile_type = self.matrix[x][y] == tile_type
				
				if x_not_on_padding and y_not_on_padding and match_correct_tile_type:
					return x, y
		else:
			return random.randint(0, self.rows - 1), random.randint(0, self.columns -1)

	def generate(self, max_empty_tiles, convert_to_image =False):
		print("Generating characters...", end =" ")
		start = time.time()
		amount = max_empty_tiles

		if self.settings["start_from_center"]:
			x, y = self.get_midway_position()
		else:
			x, y = self.get_random_position(tile_type=Matrix.FILLED_POINT_TILE)

		symbol_count = 0

		if self.settings["max_pixels_emptied_before_jumping"] == 0:
			max_walk = max_empty_tiles
		else:
			max_walk = self.settings["max_pixels_emptied_before_jumping"]
		
		count = 0

		while amount:
			if self.matrix[x][y] == Matrix.FILLED_POINT_TILE:
				if amount == max_empty_tiles:
					if self.settings["red_center"]:
						self.matrix[x][y] = Matrix.CENTER_TILE
				elif count == 0 and self.settings["red_starting_gen_point"]:
					self.matrix[x][y] = Matrix.CENTER_TILE
				else:
					if self.settings["monochromatic"]:
						self.matrix[x][y] = Matrix.EMPTY_POINT_TILE
					else:
						self.matrix[x][y] = Matrix.SYMBOLS[symbol_count]
				amount -= 1
				count += 1

			if count == max_walk:
				x, y = self.get_random_position(tile_type=Matrix.FILLED_POINT_TILE)
				count = 0
				symbol_count += 1
			else:
				x, y = self.get_new_position(x, y)
		print(f"done in {time.time() - start} seconds")
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
		
		if self.settings["create_new_file"]:
			name = f"IMG {time.time()}.png"
		else:
			name = "gend.png"

		image_path = os.path.join(directory_to_save, name)

		image.save(image_path)
		
	def convert_to_img(self):
		print("Generating colored matrix", end =" ")
		start = time.time()
		fixed_white_background = self.settings["fixed_white_background"]

		matrix = [[(255, 255, 255) for _ in range(self.columns)] for _ in range(self.rows)]

		colors = {}

		for x in range(self.rows):
			for y in range(self.columns):
				if self.matrix[x][y] == Matrix.CENTER_TILE:
					matrix[x][y] = (252, 3, 61)
				else:
					if self.matrix[x][y] == Matrix.EMPTY_POINT_TILE:
						matrix[x][y] = (0, 0, 0)
					else:
						if self.matrix[x][y] == Matrix.FILLED_POINT_TILE and fixed_white_background:
							matrix[x][y] == (255, 255, 255)
						else:
							symbol = self.matrix[x][y]
							try:
								matrix[x][y] = colors[symbol]
							except KeyError:
								colors[symbol] = tuple([random.randint(0, 255) for _ in range(3)])
								matrix[x][y] = colors[symbol]

		m = np.asarray(matrix, dtype=np.uint8)
		img = Image.fromarray(m)	
		self.save_image(img)

		print(f"done in {time.time() - start} seconds")

def parse_config_file():
	config_path = os.path.join(os.path.split(sys.argv[0])[0], "config.cfg")
	try:
		config = [line for line in open(config_path, "r").readlines() if not line.isspace()]
		settings = {}
		for line in config:
			pair = line.split("=")
			key, value = pair[0].strip(), int(pair[1].strip())
			settings[key] = value
		
		return settings
	except FileNotFoundError:
		print(f"[Error] Cant find config.cfg in path {os.path.split(config_path)[0]}")
	
def start():
	settings = parse_config_file()
	cave = Matrix(settings)
	cave.generate(settings["max_pixels_to_empty"], settings["convert_to_image"])

start()