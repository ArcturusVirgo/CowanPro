import inspect
import shutil
import sys
import shelve
from pathlib import Path
from typing import Optional
import functools
import copy

from PySide6.QtWidgets import QAbstractItemView, QFileDialog, QDialog, QTextBrowser, QMessageBox

from cowan.cowan import *
from cowan.ui import *
from cowan.constant import *
from cowan.slots.slots import *


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_main_window()
        self.ui.setupUi(self)

        # 第一页使用
        self.cowan: Optional[Cowan] = None
        self.page1_atom: Optional[Atom] = None
        self.page1_exp_data: Optional[ExpData] = None
        self.page1_in36: Optional[In36] = None
        self.page1_in2: Optional[In2] = None

        # 初始化
        self.init()
        self.bind_slot()

    def init(self):
        # 给元素选择器设置初始值
        self.ui.atomic_num.addItems(list(map(str, ATOM.keys())))
        self.ui.atomic_symbol.addItems(list(zip(*ATOM.values()))[0])
        self.ui.atomic_name.addItems(list(zip(*ATOM.values()))[1])

    def bind_slot(self):
        # 设置左侧列表与右侧页面切换之间的关联
        self.ui.navigation.currentRowChanged.connect(self.ui.stackedWidget.setCurrentIndex)

        # # 菜单栏
        # self.ui.save_project.triggered.connect(self.slot_save_project)
        # self.ui.exit_project.triggered.connect(self.slot_exit_project)
        self.ui.load_exp_data.triggered.connect(functools.partial(Menu.load_exp_data, self))  # 加载实验数据
        # self.ui.show_guides.triggered.connect(self.slot_show_guides)  # 显示参考线

        # 元素选择 - 下拉框
        self.ui.atomic_num.activated.connect(functools.partial(Page1.atom_num_changed, self))  # 原子序数
        self.ui.atomic_symbol.activated.connect(functools.partial(Page1.atom_symbol_changed, self))  # 元素符号
        self.ui.atomic_name.activated.connect(functools.partial(Page1.atom_name_changed, self))  # 元素名称
        self.ui.atomic_ion.activated.connect(functools.partial(Page1.atom_ion_changed, self))  # 离化度

        # 按钮
        self.ui.add_configuration.clicked.connect(functools.partial(Page1.add_configuration, self))  # 添加组态
        self.ui.load_in36.clicked.connect(functools.partial(Page1.load_in36, self))  # 加载in36文件
        self.ui.load_in2.clicked.connect(functools.partial(Page1.load_in2, self))  # 加载in2文件
        self.ui.preview_in36.clicked.connect(functools.partial(Page1.preview_in36, self))  # 预览in36
        self.ui.preview_in2.clicked.connect(functools.partial(Page1.preview_in2, self))  # 预览in2
        # self.ui.run_cowan.clicked.connect(self.slot_run_cowan)  # 运行Cowan
        # self.ui.configuration_move_up.clicked.connect(self.slot_configuration_move_up)  # 组态上移
        # self.ui.configuration_move_down.clicked.connect(self.slot_configuration_move_down)  # 组态下移
        # self.ui.del_configuration.clicked.connect(self.slot_del_configuration)  # 删除组态
        # self.ui.clear_history.clicked.connect(self.slot_clear_history)  # 清空运行历史
        # self.ui.add_to_selection.clicked.connect(self.slot_add_to_selection)  # 将该项目添加至库中
        # self.ui.del_selection.clicked.connect(self.slot_del_selection)  # 将该项目从库中删除
        # self.ui.run_history_list.itemDoubleClicked.connect(self.slot_load_history)  # 加载库中的项目


if __name__ == '__main__':
    app = QApplication([])
    # window = LoginWindow()  # 启动登陆页面
    window = MainWindow()  # 启动主界面
    window.show()
    app.exec()
