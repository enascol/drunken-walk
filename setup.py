""" Read and parse the config file to initialize the matrix """
import os
import os.path
import sys

import matrix
import settings as _set

from actions import analyze_settings as als

ORIGIN = __file__.rsplit('\\', maxsplit=1)[-1]

def parse_config_file():
    """ Parse settings from config.cfg"""

    config_path = os.path.join(os.path.split(sys.argv[0])[0], "config.cfg")
    try:
        config_file = open(config_path, "r").readlines()
        config = [line for line in config_file if not line.isspace()]
        settings = {}
        for line in config:
            pair = line.split("=")
            key, value = pair[0].strip(), int(pair[1].strip())
            settings[key] = value

        return settings
    except FileNotFoundError:
        print(f"[{ORIGIN}] Cant find config.cfg")
        raise


def start():
    """ Call Matrix() class passing settings"""

    _set.set_config(sys.argv)

    settings = parse_config_file()
    settings = als.execute(settings)
    cave = matrix.Matrix(settings)

    max_pixels = settings["max_pixels"]
    convert = settings["convert_to_image"]

    cave.generate(max_pixels, convert)


start()
