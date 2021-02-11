import pathlib

import yaml

CURRENT_PATH = pathlib.Path(__file__)
ROOT_PATH = CURRENT_PATH.parent.parent.parent

DEFAULT_CFG = ROOT_PATH / 'config.yml'


def get_config(cfg_path=None):
    cfg_path = cfg_path or DEFAULT_CFG
    with open(cfg_path) as f:
        cfg = yaml.safe_load(f)
    return cfg


config = get_config()
