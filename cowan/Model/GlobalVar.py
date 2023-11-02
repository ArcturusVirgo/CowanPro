from pathlib import Path

CURRENT_PROJECT_PATH = None


def PROJECT_PATH():
    """
    获取当前的项目路径

    Returns:

    """
    if CURRENT_PROJECT_PATH is None:
        raise ValueError("CURRENT_PROJECT_PATH is None")
    return CURRENT_PROJECT_PATH


def SET_PROJECT_PATH(val: Path):
    """
    设置当前的项目路径

    Args:
        val: 项目路径

    Returns:

    """
    global CURRENT_PROJECT_PATH
    CURRENT_PROJECT_PATH = val
