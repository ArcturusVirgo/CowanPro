# -*- coding: utf-8 -*-
from pathlib import Path

CURRENT_PROJECT_PATH = Path('F:/Cowan/Ge')


def PROJECT_PATH():
    return CURRENT_PROJECT_PATH


def SET_PROJECT_PATH(val: Path):
    global CURRENT_PROJECT_PATH
    CURRENT_PROJECT_PATH = val
