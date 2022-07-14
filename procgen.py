import random
import sys
from PIL import Image
import numpy as np

class Cave:
	FILLED_POINT_TILE = "#"
	EMPTY_POINT_TILE = " "
	PADDING = 2
	MAX_WALK_BEFORE_JUMP = 0

	def __init__(self, rows =100, columns =300):
		self.rows = rows
		self.columns = columns

		self.matrix = self.generate_matrix()

	def generate_matrix(self):
		return [[Cave.FILLED_POINT_TILE] * self.columns for _ in range(self.rows)]
	
	def get_midway_position(self):
		return int(self.rows / 2), int(self.columns / 2)
	
	def get_new_position(self, current_x, current_y):
		x, y = current_x, current_y

		roll = random.randint(1, 4)

		if roll == 1 and x > Cave.PADDING:
			x -= 1
		if roll == 2 and x < self.rows - Cave.PADDING:
			x += 1
		if roll == 3 and y > Cave.PADDING:
			y -= 1
		if roll == 4 and y < self.columns - Cave.PADDING:
			y += 1

		return x, y
	
	def get_random_position(self, tile_type =None):
		if tile_type:
			while True:
				x, y = self.get_random_position()
				if self.matrix[x][y] == tile_type:
					return x, y
		else:
			return random.randint(0, self.rows - 1), random.randint(0, self.columns -1)

	def generate(self, max_empty_tiles):
		amount = max_empty_tiles
		print(amount)
		x, y = self.get_midway_position()

		if Cave.MAX_WALK_BEFORE_JUMP == 0:
			max_walk = max_empty_tiles
		else:
			max_walk = Cave.MAX_WALK_BEFORE_JUMP
		
		count = 0

		while amount:
			if self.matrix[x][y] == Cave.FILLED_POINT_TILE:
				self.matrix[x][y] = Cave.EMPTY_POINT_TILE
				amount -= 1
				count += 1

			if count == max_walk:
				x, y = self.get_random_position(tile_type=Cave.FILLED_POINT_TILE)
				count = 0
			else:
				x, y = self.get_new_position(x, y)

	def show(self):
		for row in self.matrix:
			print("".join(row))
	
	def get_random_color(self):
		return random.randint(0, 250), random.randint(0, 250), random.randint(0, 250)

	def convert_to_img(self, path):
		matrix = [[(255, 255, 255) for _ in range(self.columns)] for _ in range(self.rows)]

		for x in range(self.rows):
			for y in range(self.columns):
				if self.matrix[x][y] == Cave.EMPTY_POINT_TILE:
					matrix[x][y] = (0, 0, 0)
		
		matrix = np.asarray(matrix, dtype=np.uint8)
		img = Image.fromarray(matrix)	

		img.save(path)
	
	def configure(self, settings):
		settings = convert_string_to_settings(",".join(settings))
		options = [
			("empty_tile", " "), 
			("filled_tile", "#"), 
			("walk_before_jump", 0),
			("padding", 2),
			("max_empty", 1),
			("rows", 10),
			("columns", 10) 
		]

		for option in options:
			o, v  = option
			if o not in settings:
				settings[o] = v
		
		Cave.EMPTY_POINT_TILE = settings["empty_tile"]
		Cave.FILLED_POINT_TILE = settings["filled_tile"]
		Cave.MAX_WALK_BEFORE_JUMP = int(settings["walk_before_jump"])
		Cave.PADDING = int(settings["padding"])
		self.rows = int(settings["rows"])
		self.columns = int(settings["columns"])
		settings["max_empty"] = int(settings["max_empty"])
		
		return settings

def convert_string_to_settings(settings):
	parsed_1 = [option.strip() for option in settings.split(",")]
	return dict([[x.strip() for x in option.split("=")] for option in parsed_1])


ROWS, COLUMNS, MAX, JUMP_BEFORE_WALK = range(4)

settings = [int(x) for x in sys.argv[1:]]
print(settings)
cave = Cave(settings[ROWS], settings[COLUMNS])
Cave.MAX_WALK_BEFORE_JUMP = settings[JUMP_BEFORE_WALK]
cave.generate(settings[MAX])
cave.show()
cave.convert_to_img("oii.png")