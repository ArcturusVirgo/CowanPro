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
        self.run_history_list = []
        self.cowan: Optional[Cowan] = None
        self.page1_atom: Optional[Atom] = None
        self.page1_exp_data: Optional[ExpData] = None
        self.page1_in36: Optional[In36] = None
        self.page1_in2: Optional[In2] = None

        # 第二页使用
        self.simulate: Optional[SimulateSpectral] = None

        # 初始化
        self.init()
        self.bind_slot()

    def init(self):
        # 给元素选择器设置初始值
        self.ui.atomic_num.addItems(list(map(str, ATOM.keys())))
        self.ui.atomic_symbol.addItems(list(zip(*ATOM.values()))[0])
        self.ui.atomic_name.addItems(list(zip(*ATOM.values()))[1])
        # in36组态表格相关设置
        self.ui.in36_configuration_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)  # 设置行选择模式
        self.ui.in36_configuration_view.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents)  # 设置表格列宽自适应
        self.ui.page2_grid_list.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)  # 设置表格不可编辑
        self.ui.page2_grid_list.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents)  # 设置表格列宽自适应
        # 设置右键菜单
        self.ui.in36_configuration_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.run_history_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.selection_list.setContextMenuPolicy(Qt.CustomContextMenu)

    def bind_slot(self):
        # 设置左侧列表与右侧页面切换之间的关联
        self.ui.navigation.currentRowChanged.connect(self.ui.stackedWidget.setCurrentIndex)

        # ------------------------------- 菜单栏 -------------------------------
        # self.ui.save_project.triggered.connect(self.slot_save_project)
        # self.ui.exit_project.triggered.connect(self.slot_exit_project)
        self.ui.load_exp_data.triggered.connect(functools.partial(Menu.load_exp_data, self))  # 加载实验数据
        # self.ui.show_guides.triggered.connect(self.slot_show_guides)  # 显示参考线

        # ------------------------------- 第一页 -------------------------------
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
        self.ui.configuration_move_down.clicked.connect(functools.partial(Page1.configuration_move_down, self))  # 组态下移
        self.ui.configuration_move_up.clicked.connect(functools.partial(Page1.configuration_move_up, self))  # 组态上移
        self.ui.run_cowan.clicked.connect(functools.partial(Page1.run_cowan, self))  # 运行Cowan
        # 单选框
        self.ui.auto_write_in36.clicked.connect(functools.partial(Page1.auto_write_in36, self))  # 自动生成in36
        self.ui.manual_write_in36.clicked.connect(functools.partial(Page1.manual_write_in36, self))  # 手动输入in36
        self.ui.gauss.clicked.connect(  # 线状谱展宽成gauss
            lambda: self.ui.web_cal_widen.load(QUrl.fromLocalFile(self.cowan.cal_data.widen_all.plot_path_gauss)))
        self.ui.crossP.clicked.connect(  # 线状谱展宽成crossP
            lambda: self.ui.web_cal_widen.load(QUrl.fromLocalFile(self.cowan.cal_data.widen_all.plot_path_cross_P)))
        self.ui.crossNP.clicked.connect(  # 线状谱展宽成crossNP
            lambda: self.ui.web_cal_widen.load(QUrl.fromLocalFile(self.cowan.cal_data.widen_all.plot_path_cross_NP)))
        # 输入框
        self.ui.in2_11_e.valueChanged.connect(functools.partial(Page1.in2_11_e_value_changed, self))  # in2 11 e
        # 右键菜单
        self.ui.in36_configuration_view.customContextMenuRequested.connect(
            functools.partial(Page1.in36_configuration_view_right_menu, self))  # 组态显示卡的右键菜单
        self.ui.run_history_list.customContextMenuRequested.connect(
            functools.partial(Page1.run_history_list_right_menu, self))  # 运行历史
        self.ui.selection_list.customContextMenuRequested.connect(
            functools.partial(Page1.selection_list_right_menu, self))  # 叠加离子

        # self.ui.run_history_list.itemDoubleClicked.connect(self.slot_load_history)  # 加载库中的项目


if __name__ == '__main__':
    app = QApplication([])
    # window = LoginWindow()  # 启动登陆页面
    window = MainWindow()  # 启动主界面
    window.show()
    app.exec()
