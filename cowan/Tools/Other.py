import colorama
import matplotlib
import pandas as pd
from PySide6.QtCore import Qt


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


def get_configuration_add_list(self):
    add_example = []
    for i in range(self.ui.treeWidget.topLevelItemCount()):
        parent = self.ui.treeWidget.topLevelItem(i)
        if parent.checkState(0) == Qt.Checked:
            add_example.append([True, []])
        else:
            add_example.append([False, []])
        for j in range(parent.childCount()):
            child = parent.child(j)
            if child.checkState(0) == Qt.Checked:
                add_example[i][1].append(True)
            else:
                add_example[i][1].append(False)
    return add_example


def print_to_console(text, outline_level=0, color=('', ''), thickness=0, end='\n'):
    """
    前景色            背景色           颜色
    ---------------------------------------
    30                40              黑色
    31                41              红色
    32                42              绿色
    33                43              黃色
    34                44              蓝色
    35                45              紫红色
    36                46              青蓝色
    37                47              白色
    ---------------------------------------

    Args:
        thickness:
        text:
        outline_level:
        color:
        end:

    Returns:

    """
    color_str_list = ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']
    colorama_fore_list = [
        colorama.Fore.BLACK,
        colorama.Fore.RED,
        colorama.Fore.GREEN,
        colorama.Fore.YELLOW,
        colorama.Fore.BLUE,
        colorama.Fore.MAGENTA,
        colorama.Fore.CYAN,
        colorama.Fore.WHITE,
    ]
    colorama_back_list = [
        colorama.Back.BLACK,
        colorama.Back.RED,
        colorama.Back.GREEN,
        colorama.Back.YELLOW,
        colorama.Back.BLUE,
        colorama.Back.MAGENTA,
        colorama.Back.CYAN,
        colorama.Back.WHITE,
    ]
    if color[0] not in color_str_list:
        fore_color = ''
    else:
        fore_color = colorama_fore_list[color_str_list.index(color[0])]
    if color[1] not in color_str_list:
        back_color = ''
    else:
        back_color = colorama_back_list[color_str_list.index(color[1])]

    style_color = colorama.Style.NORMAL
    if thickness == 1:
        style_color = colorama.Style.BRIGHT
    elif thickness == -1:
        style_color = colorama.Style.DIM
    print('  ' * outline_level, end='')
    print(
        style_color
        + back_color
        + fore_color
        + text
        + colorama.Style.RESET_ALL,
        end=end,
    )


def dataframe_append_series(dataframe: pd.DataFrame, series: pd.Series, series_name: str) -> pd.DataFrame:
    series.name = series_name
    dataframe = pd.concat([dataframe, series], axis=1)
    return dataframe


colorama.init(autoreset=True)
