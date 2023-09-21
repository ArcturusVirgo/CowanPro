# -*- coding: utf-8 -*-
from pathlib import Path

CURRENT_PROJECT_PATH = None


def PROJECT_PATH():
    if CURRENT_PROJECT_PATH is None:
        raise ValueError("CURRENT_PROJECT_PATH is None")
    return CURRENT_PROJECT_PATH


def SET_PROJECT_PATH(val: Path):
    global CURRENT_PROJECT_PATH
    CURRENT_PROJECT_PATH = val
