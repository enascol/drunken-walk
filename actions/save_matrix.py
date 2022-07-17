""" Saves a matrix to a text file in /matrixes"""

import os
import os.path

import time

ORIGIN = __file__.rsplit('\\', maxsplit=1)[-1]

def execute(matrix, path):
    print(f"[{ORIGIN}] Saving matrix to {path}")

    if not os.path.isdir(path):
        os.makedirs(path)

    matrix_string = []

    for row in matrix:
        matrix_string.append("".join(row))

    matrix_string = "\n".join(matrix_string)

    matrix_name = f"M{time.time()}"
    matrix_path = os.path.join(path, matrix_name)

    with open(matrix_path, "w+") as mf:
        mf.write(matrix_string)
