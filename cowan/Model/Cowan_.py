import os
import copy
import shutil
import subprocess
from typing import Optional, List
from pathlib import Path

from PySide6 import QtCore
from PySide6.QtCore import Signal

from .GlobalVar import PROJECT_PATH
from .InputFile import In36, In2
from .CalData import CalData
from .ExpData import ExpData


class Cowan:
    def __init__(self, in36, in2, name, exp_data, coupling_mode=1):
        """
        Cowan 对象，用于管理 in36、in2、exp_data 对象
        Args:
            in36: in36对象
            in2: in2对象
            name: Cowan的名称
            exp_data: 对应的实验数据
            coupling_mode: 耦合模式，1是L-S耦合 2是j-j耦合
        """
        self.in36: In36 = copy.deepcopy(in36)
        self.in2: In2 = copy.deepcopy(in2)
        self.name: str = name
        self.exp_data: ExpData = copy.deepcopy(exp_data)
        self.coupling_mode = coupling_mode  # 1是L-S耦合 2是j-j耦合

        self.cal_data: Optional[CalData] = None
        self.run_path = PROJECT_PATH() / f'cal_result/{self.name}'

    def set_xrange(self, range_: List[float], num: int):
        self.exp_data.set_xrange(range_)
        self.cal_data.widen_all.exp_data.set_xrange(range_)
        self.cal_data.widen_all.n = num
        self.cal_data.widen_part.exp_data.set_xrange(range_)
        self.cal_data.widen_part.n = num

        self.cal_data.widen_all.widen(False)

    def reset_xrange(self):
        self.exp_data.reset_xrange()
        self.cal_data.widen_all.exp_data.reset_xrange()
        self.cal_data.widen_part.exp_data.reset_xrange()
        self.cal_data.widen_all.n = None
        self.cal_data.widen_part.n = None

        self.cal_data.widen_all.widen(False)

    def load_class(self, class_info):
        self.in36.load_class(class_info.in36)
        # in2 对象
        self.in2.load_class(class_info.in2)
        # name
        self.name = class_info.name
        # exp_data 对象
        self.exp_data.load_class(class_info.exp_data)
        # coupling_mode
        self.coupling_mode = class_info.coupling_mode
        # cal_data 对象
        self.cal_data.load_class(class_info.cal_data)
        # run_path
        self.run_path = PROJECT_PATH() / f'cal_result/{self.name}'


class CowanThread(QtCore.QThread):
    sub_complete = Signal(str)
    all_completed = Signal(str)

    def __init__(self, old_cowan: Cowan):
        """
        用于多线程计算的 cowan 对象

        Args:
            old_cowan: 原始的 cowan 对象
        """
        super().__init__()
        self.old_cowan = old_cowan
        self.in36: In36 = old_cowan.in36
        self.in2: In2 = old_cowan.in2
        self.name: str = old_cowan.name
        self.exp_data: ExpData = old_cowan.exp_data
        self.coupling_mode = old_cowan.coupling_mode  # 1是L-S耦合 2是j-j耦合

        self.cal_data: Optional[CalData] = old_cowan.cal_data
        self.run_path = PROJECT_PATH() / f'cal_result/{self.name}'

        self.finished.connect(self.update_origin)

    def run(self):
        """
        运行 Cowan 程序

        创建 cal_data 对象

        """
        self.__get_ready()
        # 获取最初的运行路径
        original_path = Path.cwd()

        # 运行文件
        os.chdir(self.run_path)
        self.sub_complete.emit('0')
        rcn = subprocess.run('./RCN.exe')
        self.sub_complete.emit('25')
        rcn2 = subprocess.run('./RCN2.exe')
        self.sub_complete.emit('50')
        self.__edit_ing11()
        rcg = subprocess.run('./RCG.exe')
        self.sub_complete.emit('100')
        os.chdir(original_path)

        # 更新 cal_data 对象
        self.cal_data = CalData(self.name, self.exp_data)
        self.all_completed.emit('completed')

    def __get_ready(self):
        """
        运行 Cowan 程序前的准备工作

        创建运行文件夹，复制运行文件，保存 in36、in2 文件

        """
        if self.run_path.exists():
            shutil.rmtree(self.run_path)
        shutil.copytree(PROJECT_PATH() / 'bin', self.run_path)
        self.in36.save(self.run_path / 'in36')
        self.in2.save(self.run_path / 'in2')

    def __edit_ing11(self):
        """
        在Cowan运行过程中，编辑文件，调整耦合模式

        """
        with open('./out2ing', 'r', encoding='utf-8') as f:
            text = f.read()
        text = f'    {self.coupling_mode}{text[5:]}'
        with open('./ing11', 'w', encoding='utf-8') as f:
            f.write(text)
        with open('./out2ing', 'w', encoding='utf-8') as f:
            f.write(text)

    def update_origin(self):
        """
        更新原始的 cowan 对象

        """
        self.old_cowan.cal_data = self.cal_data
