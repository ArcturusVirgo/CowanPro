import matplotlib


def rainbow_color(x):
    """
    将 0 - 1 之间的浮点数转换为彩虹色
    Args:
        x: 0-1 之间的浮点数

    Returns:
        返回一个元组 (r,g,b,a)
    """
    camp = matplotlib.colormaps['rainbow']
    rgba = camp(x)
    return (
        int(rgba[0] * 255),
        int(rgba[1] * 255),
        int(rgba[2] * 255),
        int(rgba[3] * 255),
    )
