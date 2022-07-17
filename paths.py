import os.path

TOPLEVEL_PATH = os.path.split(os.path.realpath(__file__))[0]
CONFIG_PATH = os.path.join(TOPLEVEL_PATH, "config.cfg")
GEN_PATH = os.path.join(TOPLEVEL_PATH, "gen")
MATRIXES_PATH = os.path.join(TOPLEVEL_PATH, "matrixes")

