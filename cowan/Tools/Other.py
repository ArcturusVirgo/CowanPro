import matplotlib
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
