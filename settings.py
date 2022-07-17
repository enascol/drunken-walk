""" Module to parse option passed when running the setup script. """

import paths

def set_config(args):
    """ Changes configuration file based on arguments passed to the script """

    try:
        args = args[1]
        settings = _get_new_settings(args)
        _write_to_config(settings)
    except IndexError as error:
        print(error)
    except FileNotFoundError as error:
        print(error)


def _parse_args(args):
    pairs = [
        [p.strip() for p in pair.split("=")]
        for pair in [
            setting.strip() for setting in args.split(",")
        ]
    ]

    new_settings = {key: value for key, value in pairs}

    return new_settings


def _parse_config_file():
    try:
        configs = open(paths.CONFIG_PATH, "r").readlines()
    except FileNotFoundError:
        raise FileNotFoundError("[Error] CONFIG.CFG NOT FOUND")

    settings_pair = []

    for setting in configs:
        not_empty_line = not setting.isspace()
        not_a_comment = setting[0][0] != "#"

        if not_a_comment and not_empty_line:
            setting = setting.strip()
            pair = [item.strip() for item in setting.split("=")]
            settings_pair.append(pair)

    return {key: value for key, value in settings_pair}


def _write_to_config(settings):
    with open(paths.CONFIG_PATH, "w") as config_file:
        config_file.write(settings)


def _convert_settings_to_string(settings):
    settings_string = []

    for key, value in settings.items():
        setting = " = ".join([key, value])
        settings_string.append(setting)

    return "\n".join(settings_string)


def _get_new_settings(args):
    arg_settings = _parse_args(args)
    config_settings = _parse_config_file()

    for key, value in arg_settings.items():
        if key in config_settings:
            config_settings[key] = value
        else:
            print(f"[Warning] UNKNOWN OPTION {key}. IGNORED.")

    return _convert_settings_to_string(config_settings)
