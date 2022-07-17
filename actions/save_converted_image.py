""" Saves the image generated from the matrix.

Saves the image to the gen folder created in the
directory where this script is being ran.

If "create_new_file" is set to 0 then tbe image
will be saved to the same file instead of creating
a new one.
"""

import os
import os.path

import time

ORIGIN = __file__.rsplit('\\', maxsplit=1)[-1]

def execute(image, path, create_new_file=False):
    print(f"[{ORIGIN}] Saving image...")

    if not os.path.isdir(path):
        os.makedirs(path)

    if create_new_file:
        name = f"IMG{time.time()}.png"
    else:
        name = "gend.png"

    image_path = os.path.join(path, name)
    image.save(image_path)

    print(f"[{ORIGIN}] Saved to {image_path}")

