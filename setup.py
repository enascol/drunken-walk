import matrix

import os, os.path
import sys

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
	cave = matrix.Matrix(settings)
	cave.generate(settings["max_pixels_to_empty"], settings["convert_to_image"])

start()