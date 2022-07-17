""" Shows informations base on settings """

from matplotlib.style import available


ORIGIN = __file__.rsplit('\\', maxsplit=1)[-1]

def execute(settings):
    settings = _check_max_pixels(settings)
    settings = _check_jumps(settings)

    return settings

def get_available_area(settings):
    area = settings["rows"] * settings["columns"]
    perimeter = (settings["rows"] + settings["columns"]) * 2 * settings["padding"]
    available_area = area - perimeter

    return available_area

def _check_max_pixels(settings):
    rows = settings["rows"]
    columns = settings["columns"]
    area = rows * columns

    if settings["max_pixels"] >= area:
        print(f"[{ORIGIN}] max_pixels set too close to max available area, grid might not generate")
        
        if settings["auto_adjust_settings"]:
            max_pixels = rows * columns / 2
            print(f"[{ORIGIN} auto_adjust_settings set to 1, ajudsting max_pixesl to {max_pixels}]")
            settings["max_pixels"] = max_pixels
    
    return settings

def _check_jumps(settings):
    max_pixels = settings["max_pixels"]   
    jumps = settings["jumps"]
    pixels_per_jump = int(max_pixels / jumps)

    print(f"[{ORIGIN}] jumps setting of value {jumps} will generated {pixels_per_jump} pixels per jump")

    return settings