# ================================================
# Cowan原子结构计算程序的自动化实现
# ================================================

import copy
import functools
import os
import shutil
import subprocess
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Optional, List, Dict, Tuple

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from PySide6 import QtCore
from PySide6.QtCore import Signal
from plotly.offline import plot
from scipy.interpolate import interp1d
from scipy.signal import find_peaks

from .atom_info import *
from ..global_var import *


class Atom:
    def __init__(self, num: int, ion: int):
        """
        原子类，附属于 in36 对象

        Args:
            num: 原子序数
            ion: 离化度（剥离的电子数目）

        Notes:
            1. 使用 get_base_configuration 获取基组态
            2. 使用 arouse_electron 激发电子
            3. 使用 get_configuration 获取当前的电子组态
            4. 使用 revert_to_ground_state 将原子状态重置为基态
            5. goto 2

        """
        self.num = num  # 原子序数
        self.symbol = ATOM[self.num][0]  # 元素符号
        self.name = ATOM[self.num][1]  # 元素名称
        self.ion = ion  # 离化度
        self.electron_num = self.num - self.ion  # 实际的电子数量
        self.electron_arrangement = self.get_base_electron_arrangement()
        self.base_configuration = self.get_base_configuration()  # 基组态

    def get_base_electron_arrangement(self):
        """
        获取原子处于基态时，核外电子的排布情况

        Returns:
            返回一个字典，键为子壳层，值为子壳层的电子数, 例如 {
                '1s': 2,
                '2s': 2,
                '2p': 6,
                '3s': 2,
                '3p': 4,}

        """
        electron_arrangement = {}
        for key, value in map(lambda x: [str(x[:2]), int(x[2:])], BASE_CONFIGURATION[self.num][self.ion].split(' ')):
            electron_arrangement[key] = value
        return electron_arrangement

    def get_base_configuration(self):
        """
        将电子组态重置为基态，并且 获取基组态字符串

        """
        self.revert_to_ground_state()
        return self.get_configuration()

    def get_configuration(self) -> str:
        """
        根据该原子当前的电子排布情况，获取当前的电子组态

        Returns:
            返回一个字符串，例如 3s02 3p03 4s01
        """
        configuration = {}  # 按照子壳层的顺序排列的电子组态
        for i, subshell_name in enumerate(SUBSHELL_NAME):
            if subshell_name in self.electron_arrangement.keys():
                configuration[subshell_name] = self.electron_arrangement[subshell_name]
        delete_name = []
        for i, (subshell_name, num) in enumerate(configuration.items()):
            l_ = ANGULAR_QUANTUM_NUM_NAME.index(subshell_name[1])
            if num == 4 * l_ + 2:
                delete_name.append(subshell_name)
            else:
                delete_name.append(subshell_name)
                break
        if len(delete_name) >= 2:
            delete_name.pop(-1)
            delete_name.pop(-1)
        else:
            delete_name = []
        for name in delete_name:
            configuration.pop(name)

        configuration_list = []
        for name, num in configuration.items():
            configuration_list.append('{}{:0>2}'.format(name, num))
        return ' '.join(configuration_list)

    def arouse_electron(self, low_name, high_name):
        """
        激发电子，改变原子内电子的排布情况

        Args:
            low_name: 下态的支壳层名称
            high_name: 上态的支壳层名称
        """
        if low_name not in SUBSHELL_SEQUENCE:
            raise Exception(f'没有名为{low_name}的支壳层！')
        elif high_name not in SUBSHELL_SEQUENCE:
            raise Exception(f'没有名为{high_name}的支壳层!')
        elif low_name not in self.electron_arrangement.keys():
            raise Exception(f'没有处于{low_name}的电子！')
        elif self.electron_arrangement.get(high_name, 0) == 4 * ANGULAR_QUANTUM_NUM_NAME.index(high_name[1]) + 2:
            raise Exception(f'{high_name}的电子已经排满！')

        self.electron_arrangement[low_name] -= 1
        self.electron_arrangement[high_name] = (self.electron_arrangement.get(high_name, 0) + 1)
        if self.electron_arrangement[low_name] == 0:
            self.electron_arrangement.pop(low_name)

    def revert_to_ground_state(self):
        """
        将原子的状态重置为基态

        """
        self.electron_arrangement = self.get_base_electron_arrangement()


class ExpData:
    def __init__(self, filepath: Path):
        """
        实验数据对象，一般附属于 Cowan、SimulateSpectral 对象

        Args:
            filepath: 实验数据所在的路径
        """
        self.plot_path = (PROJECT_PATH() / 'figure/exp.html').as_posix()  # 实验谱线的绘图路径
        self.filepath: Path = filepath  # 实验数据的路径

        self.data: Optional[pd.DataFrame] = None  # 实验数据
        self.init_xrange = None  # 原始的波长范围
        self.x_range: Optional[List[float]] = None  # 实验数据的波长范围

        self.__read_file()

    def set_range(self, x_range: List[float]):
        """
        设置实验数据的波长范围

        Args:
            x_range: 波长范围，单位为 nm

        """
        self.x_range = x_range
        self.data = self.data[(self.data['wavelength'] < self.x_range[1]) &
                              (self.data['wavelength'] > self.x_range[0])]

    def reset_range(self):
        """
        重置实验数据的波长范围

        """
        self.set_range(self.init_xrange)

    def __read_file(self):
        """
        根据路径读入实验数据

        """
        filetype = self.filepath.suffix[1:]
        if filetype == 'csv':
            temp_data = pd.read_csv(self.filepath, sep=',', skiprows=1, names=['wavelength', 'intensity'])
        elif filetype == 'txt':
            temp_data = pd.read_csv(self.filepath, sep='\s+', skiprows=1, names=['wavelength', 'intensity'])
        else:
            raise ValueError(f'filetype {filetype} is not supported')
        temp_data['intensity_normalization'] = (temp_data['intensity'] - temp_data['intensity'].min()) / (
                temp_data['intensity'].max() - temp_data['intensity'].min())

        self.data = temp_data
        self.x_range = [self.data['wavelength'].min(), self.data['wavelength'].max()]
        self.init_xrange = copy.deepcopy(self.x_range)

    def plot_html(self):
        """
        绘制实验谱线

        """
        trace1 = go.Scatter(x=self.data['wavelength'], y=self.data['intensity'], mode='lines')
        data = [trace1]
        layout = go.Layout(
            margin=go.layout.Margin(autoexpand=False, b=15, l=30, r=0, t=0),
            xaxis=go.layout.XAxis(range=self.x_range),
        )
        # yaxis=go.layout.YAxis(range=[self.min_strength, self.max_strength]))
        fig = go.Figure(data=data, layout=layout)

        plot(fig, filename=self.plot_path, auto_open=False)


class In36:
    def __init__(self):
        """
        in36 对象，一般附属于 Cowan 对象

        """
        self.atom: Optional[Atom] = None

        self.control_card = ['2', ' ', ' ', '-9', ' ', '  ', ' 2', '   ', '10', '  1.0', '    5.e-08', '    1.e-11',
                             '-2', '  ', ' ', '1', '90', '  ', '  1.0', ' 0.65', '  0.0', '  0.0', '     ', ]
        self.configuration_card = []

    def read_from_file(self, path: Path):
        """
        读取已经编写号的in36文件

        自动更新原子对象，组态卡，控制卡

        Args:
            path (Path): in36文件的路径
        """
        with open(path, 'r') as f:
            lines = f.readlines()
        # 控制卡读入
        control_card_text = lines[0].strip('\n')
        control_card_list = []
        if len(control_card_text) != 80:
            control_card_text += ' ' * (80 - len(control_card_text))
        rules = [1, 1, 1, 2, 1, 2, 2, 3, 2, 5, 10, 10, 2, 2, 1, 1, 2, 2, 5, 5, 5, 5, 5]
        for rule in rules:
            control_card_list.append(control_card_text[:rule])
            control_card_text = control_card_text[rule:]
        # 组态卡读入
        input_card_list = []
        for line in lines[1:]:
            value = line.split()
            if value == ['-1']:
                break
            v0 = '{:>5}'.format(value[0])
            v1 = '{:>10}'.format(value[1])
            v2 = '{:>7}'.format(value[2])
            v3 = '           '
            v4 = ' '.join(value[3:])
            input_card_list.append([[v0, v1, v2, v3, v4], self.__judge_parity(v4)])
        self.control_card, self.configuration_card = control_card_list, input_card_list

        # 更新原子信息
        num = int(self.configuration_card[0][0][0].split(' ')[-1])
        ion = int(self.configuration_card[0][0][1].split('+')[-1])
        self.atom = Atom(num=num, ion=ion)

    def set_atom(self, atom: Atom):
        """
        设置原子对象

        Args:
            atom (Atom): 原子对象

        """
        self.atom = copy.deepcopy(atom)

    def add_configuration(self, configuration: str):
        """
        向 in36 文件的组态卡添加组态（会自动剔除重复的组态）

        Args:
            configuration (str): 要添加的组态
        """
        if self.configuration_card:  # 如果组态卡不为空
            temp_list = list(zip(*list(zip(*self.configuration_card))[0]))[-1]
        else:  # 如果组态卡为空
            temp_list = []
        if configuration not in temp_list:
            v0 = '{:>5}'.format(self.atom.num)
            v1 = '{:>10}'.format(f'{self.atom.ion + 1}{ATOM[self.atom.num][0]}+{self.atom.ion}')
            v2 = '{:>7}'.format('11111')
            v3 = '           '
            v4 = configuration
            self.configuration_card.append([[v0, v1, v2, v3, v4], self.__judge_parity(v4)])

    def configuration_move(self, index, opt: str):
        """
        移动组态的先后顺序

        Args:
            index: 要移动的组态的索引
            opt: 操作名称 up 或 down

        """
        if opt == 'up':
            if 1 <= index <= len(self.configuration_card):
                self.configuration_card[index], self.configuration_card[index - 1] = (
                    self.configuration_card[index - 1], self.configuration_card[index],)
        elif opt == 'down':
            if 0 <= index <= len(self.configuration_card) - 2:
                self.configuration_card[index], self.configuration_card[index + 1] = (
                    self.configuration_card[index + 1], self.configuration_card[index],)
        else:
            raise ValueError('opt must be "up" or "down"')

    def del_configuration(self, index: int):
        """
        删除 in36 组态卡中的组态

        Args:
            index (int): 要删除的组态的索引

        """
        self.configuration_card.pop(index)

    def get_configuration_name(self, low_index, high_index):
        """
        根据组态索引获取电子跃迁的支壳层名称

        Args:
            low_index: 下态的索引
            high_index: 上态的索引

        Returns:
            返回一个字符串，如 '2p --> 3s'
        """
        first_parity = self.configuration_card[0][1]
        first_configuration = []
        second_configuration = []
        for configuration, parity in self.configuration_card:
            if parity == first_parity:
                first_configuration.append(configuration[-1])
            else:
                second_configuration.append(configuration[-1])
        low_index, high_index = low_index - 1, high_index - 1
        low_configuration = first_configuration[low_index]
        high_configuration = second_configuration[high_index]

        low_configuration = low_configuration.split(' ')
        high_configuration = high_configuration.split(' ')

        low_dict = {}
        high_dict = {}

        for low in low_configuration:
            low_dict[low[:2]] = low[2:]
        for high in high_configuration:
            high_dict[high[:2]] = high[2:]
        configuration_name = list(set(list(low_dict.keys()) + list(high_dict.keys())))
        res = {}
        for name in configuration_name:
            res[name] = int(low_dict.get(name, 0)) - int(high_dict.get(name, 0))
        low_name = []
        high_name = []
        for key, value in res.items():
            if value < 0:
                for i in range(-value):
                    high_name.append(key)
            elif value > 0:
                for i in range(value):
                    low_name.append(key)
        return '{} --> {}'.format(','.join(low_name), ','.join(high_name))

    def get_text(self):
        """
        生成 in36 文件所包含的字符串

        Returns:
            in36 文件的字符串
        """
        in36 = ''
        in36 += ''.join(self.control_card)
        in36 += '\n'
        for v in self.configuration_card:
            in36 += ''.join(v[0])
            in36 += '\n'
        in36 += '   -1\n'
        return in36

    def save(self, path: Path):
        """
        保存为 in36 文件

        Args:
            path (Path): 生成的 in36 文件的路径

        """
        with open(path, 'w', encoding='utf-8') as f:
            f.write(self.get_text())

    @staticmethod
    def __judge_parity(configuration: str) -> int:
        """
        判断指定组态的宇称

        Args:
            configuration: 要判断宇称的电子组态，字符串形式，如 '2p06 3s01'

        Returns:
            返回一个整数，其中
            0: 偶宇称
            1: 奇宇称
        """
        configuration = list(configuration.split(' '))
        sum_ = 0
        for v in configuration:
            sum_ += ANGULAR_QUANTUM_NUM_NAME.index(v[1]) * eval(v[3:])

        if sum_ % 2 == 0:
            return 0
        else:
            return 1


class In2:
    def __init__(self):
        """
        in2 对象，附属于 Cowan 对象

        Args:

        """
        self.input_card: List[str] = [
            'g5inp', '  ', '0', ' 0', '0', '00', '  0.000', ' ', '00000000', ' 0000000', '   00000', ' 000', '0', '90',
            '99', '90', '90', '90', '.0000', '     ', '0', '7', '2', '2', '9', '     ', ]

    def read_from_file(self, path: Path):
        """
        读取 in2 文件

        更新输入卡

        Args:
            path: in2文件的路径

        """
        with open(path, 'r') as f:
            line = f.readline()
        line = line.strip('\n')
        if len(line) != 80:
            line += ' ' * (80 - len(line) - 1)
        rules = [5, 2, 1, 2, 1, 2, 7, 1, 8, 8, 8, 4, 1, 2, 2, 2, 2, 2, 5, 5, 1, 1, 1, 1, 1, 5, ]
        input_card_list = []
        for rule in rules:
            input_card_list.append(line[:rule])
            line = line[rule:]
        self.input_card = input_card_list

    def get_text(self):
        """
        获取 in2 文件所包含的字符串

        Returns:
            in2 字符串
        """
        in2 = 'g5inp     000 0.0000          01        .095.095  8499848484 0.00   1 18229'
        new_in2 = in2[:50] + ''.join(self.input_card[13:18]) + in2[60:]
        # in2 += ''.join(self.input_card)
        new_in2 += '\n'
        new_in2 += '        -1\n'
        return new_in2

    def save(self, path: Path):
        """
        保存为 in2 文件

        Args:
            path: 要保存的文件夹

        """
        with open(path, 'w', encoding='utf-8') as f:
            f.write(self.get_text())


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
        self.run_path = old_cowan.run_path

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
        self.old_cowan.in36 = self.in36
        self.old_cowan.in2 = self.in2
        self.old_cowan.name = self.name
        self.old_cowan.exp_data = self.exp_data
        self.old_cowan.coupling_mode = self.coupling_mode
        self.old_cowan.cal_data = self.cal_data
        self.old_cowan.run_path = self.run_path


class CalData:
    def __init__(self, name, exp_data: ExpData):
        """
        计算结果对象，附属于 Cowan 对象

        Args:
            name: Cowan的名称
            exp_data: 对应的实验数据
        """
        self.name = name
        self.exp_data = exp_data
        self.filepath = (PROJECT_PATH() / f'cal_result/{name}/spectra.dat').as_posix()
        self.plot_path = (PROJECT_PATH() / f'figure/line/{name}.html').as_posix()
        self.init_data: pd.DataFrame | None = None

        self.widen_all: Optional[WidenAll] = None  # 通过self.read_file()赋初值
        self.widen_part: Optional[WidenPart] = None  # 通过self.read_file()赋初值

        self.read_file()

    def read_file(self):
        """
        读取Cowan程序计算的结果

        产生两个展宽对象：widen_all、widen_part

        """
        self.init_data = pd.read_csv(
            self.filepath,
            sep='\s+',
            names=['energy_l', 'energy_h', 'wavelength_ev', 'intensity', 'index_l', 'index_h', 'J_l', 'J_h', ],
        )
        self.widen_all = WidenAll(self.name, self.init_data, self.exp_data)
        self.widen_part = WidenPart(self.name, self.init_data, self.exp_data)

    def get_average_wavelength(self):
        """
        获取平均波长

        Returns:
            返回当前离化度的各个组态的平均波长，数据格式为字典
            键为组态序号（str），值为平均波长（float）
        """
        temp_data = {}
        # 按照跃迁正例分开
        data_grouped = self.init_data.groupby(by=['index_l', 'index_h'])
        for index in data_grouped.groups.keys():
            temp_group = pd.DataFrame(data_grouped.get_group(index))
            intensity = temp_group['intensity'].values
            wavelength = 1239.85 / temp_group['wavelength_ev'].values
            temp_data[f'{index[0]}_{index[1]}'] = (intensity * wavelength).sum() / intensity.sum()
        return temp_data

    def plot_line(self):
        """
        绘制线状谱
        """
        temp_data = self.__get_line_data(self.init_data[['wavelength_ev', 'intensity']])
        trace1 = go.Scatter(
            x=temp_data['wavelength'], y=temp_data['intensity'], mode='lines'
        )
        data = [trace1]
        layout = go.Layout(
            margin=go.layout.Margin(autoexpand=False, b=15, l=30, r=0, t=0),
            xaxis=go.layout.XAxis(range=self.exp_data.x_range),
        )
        # yaxis=go.layout.YAxis(range=[self.min_strength, self.max_strength]))
        fig = go.Figure(data=data, layout=layout)
        plot(fig, filename=self.plot_path, auto_open=False)

    def __get_line_data(self, origin_data):
        """
        将计算结果转换为线状谱

        Args:
            origin_data: 读取进来的原始数据

        Returns:
            转化后的数据
        """
        temp_data = origin_data.copy()
        temp_data['wavelength'] = 1239.85 / temp_data['wavelength_ev']
        temp_data = temp_data[
            (temp_data['wavelength'] < self.exp_data.x_range[1])
            & (temp_data['wavelength'] > self.exp_data.x_range[0])
            ]
        lambda_ = []
        strength = []
        if temp_data['wavelength'].min() > self.exp_data.x_range[0]:
            lambda_ += [self.exp_data.x_range[0]]
            strength += [0]
        for x, y in zip(temp_data['wavelength'], temp_data['intensity']):
            lambda_ += [x, x, x]
            strength += [0, y, 0]
        if temp_data['wavelength'].max() < self.exp_data.x_range[1]:
            lambda_ += [self.exp_data.x_range[1]]
            strength += [0]
        temp = pd.DataFrame({'wavelength': lambda_, 'intensity': strength})
        return temp


class WidenAll:
    def __init__(self, name, init_data, exp_data: ExpData, n=None, ):
        """
        整体展宽对象，附属于 CalData 对象

        Args:
            name: CalData的名称
            init_data: 计算的原始数据
            exp_data: 实验数据
            n: 展宽时的点的个数，如果为None，则使用实验数据的波长
        """
        self.name = name
        self.init_data = init_data.copy()
        self.exp_data = exp_data
        self.n = n
        self.only_p = None
        self.delta_lambda: float = 0.0
        self.fwhm_value: float = 0.5

        self.plot_path_gauss = (PROJECT_PATH() / f'figure/gauss/{self.name}.html').as_posix()
        self.plot_path_cross_NP = (PROJECT_PATH() / f'figure/cross_NP/{self.name}.html').as_posix()
        self.plot_path_cross_P = (PROJECT_PATH() / f'figure/cross_P/{self.name}.html').as_posix()

        self.widen_data: pd.DataFrame | None = None

    def widen(self, temperature: float, only_p=True):
        """
        展宽

        列标题依次为：energy_l, energy_h, wavelength_ev, intensity, index_l, index_h, J_l, J_h
        分别代表：下态能量，上态能量，波长，强度，下态序号，上态序号，下态J值，上态J值

        Args:
            temperature (float): 等离子体温度
            only_p: 只计算包含能级布局的数据
        Returns:
            返回一个DataFrame，包含了展宽后的数据
            列标题为：wavelength, gaussian, cross-NP, cross-P
            如果only_p为True，则没有cross-NP列和gaussian列
        """
        self.only_p = only_p

        data = self.init_data.copy()
        fwhmgauss = self.fwhmgauss
        lambda_range = self.exp_data.x_range

        new_data = data.copy()
        # 找到下态最小能量和最小能量对应的J值
        min_energy = new_data['energy_l'].min()
        min_J = new_data[new_data['energy_l'] == min_energy]['J_l'].min()
        # 筛选波长范围在实验数据范围内的跃迁正例个数
        min_wavelength_nm = lambda_range[0]
        max_wavelength_nm = lambda_range[1]
        min_wavelength_ev = 1239.85 / max_wavelength_nm
        max_wavelength_ev = 1239.85 / min_wavelength_nm
        new_data = new_data[
            (new_data['wavelength_ev'] > min_wavelength_ev)
            & (new_data['wavelength_ev'] < max_wavelength_ev)
            ]
        if self.n is None:
            wave = 1239.85 / np.array(self.exp_data.data['wavelength'].values)
            print('使用的是实验数据的波长')
        else:
            wave = 1239.85 / np.linspace(min_wavelength_nm, max_wavelength_nm, self.n)
            print('使用的是自定义的波长')
        result = pd.DataFrame()
        result['wavelength'] = 1239.85 / wave

        if new_data.empty:
            result['gauss'] = 0
            result['cross_NP'] = 0
            result['cross_P'] = 0
            self.widen_data = result
            return -1
        new_data = new_data.reindex()
        # 获取展宽所需要的数据
        new_wavelength = abs(1239.85 / (1239.85 / new_data['wavelength_ev'] + self.delta_lambda))  # 单位时ev
        new_wavelength = new_wavelength.values
        new_intensity = abs(new_data['intensity'])
        new_intensity = new_intensity.values
        flag = new_data['energy_l'] > new_data['energy_h']
        not_flag = np.bitwise_not(flag)
        temp_1 = new_data['energy_l'][flag]
        temp_2 = new_data['energy_h'][not_flag]
        new_energy = temp_1.combine_first(temp_2)
        new_energy = new_energy.values
        temp_1 = new_data['J_l'][flag]
        temp_2 = new_data['J_h'][not_flag]
        new_J = temp_1.combine_first(temp_2)
        new_J = new_J.values
        # 计算布居
        population = ((2 * new_J + 1) * np.exp(-abs(new_energy - min_energy) * 0.124 / temperature) / (2 * min_J + 1))

        res = [self.__complex_cal(val, new_intensity, fwhmgauss(val), new_wavelength, population, new_J) for val in
               wave]
        res = list(zip(*res))
        if not self.only_p:
            result['gauss'] = res[0]
            result['cross_NP'] = res[1]
        result['cross_P'] = res[2]
        self.widen_data = result

    def plot_widen(self):
        """
        绘制展宽后的谱线

        """
        if not self.only_p:
            self.__plot_html(self.widen_data, self.plot_path_gauss, 'wavelength', 'gauss')
            self.__plot_html(self.widen_data, self.plot_path_cross_NP, 'wavelength', 'cross_NP')
        self.__plot_html(self.widen_data, self.plot_path_cross_P, 'wavelength', 'cross_P')

    def __plot_html(self, data, path, x_name, y_name):
        """
        绘制html文件
        Args:
            data: 数据
            path: 要保存的路径
            x_name: x的列名
            y_name: y的列名

        """
        trace1 = go.Scatter(x=data[x_name], y=data[y_name], mode='lines')
        data = [trace1]
        layout = go.Layout(
            margin=go.layout.Margin(autoexpand=False, b=15, l=30, r=0, t=0),
            xaxis=go.layout.XAxis(range=self.exp_data.x_range),
        )
        # yaxis=go.layout.YAxis(range=[self.min_strength, self.max_strength]))
        fig = go.Figure(data=data, layout=layout)
        plot(fig, filename=path, auto_open=False)

    def __complex_cal(
            self,
            wave: float,
            new_intensity: np.array,
            fwhmgauss: float,
            new_wavelength: np.array,
            population: np.array,
            new_J: np.array,
    ):
        """
        展宽时的复杂计算
        Args:
            wave:
            new_intensity:
            fwhmgauss:
            new_wavelength:
            population:
            new_J:

        Returns:
            展宽后的数据，为一个元组，依次为：gauss, cross_NP, cross_P
            如果only_p为True，则前两个元素为-1
        """
        uu = ((new_intensity * population / (2 * new_J + 1)) * 2 * fwhmgauss / (
                2 * np.pi * ((new_wavelength - wave) ** 2 + np.power(2 * fwhmgauss, 2) / 4)))
        if self.only_p:
            return -1, -1, uu.sum()
        else:
            tt = (new_intensity / np.sqrt(2 * np.pi) / fwhmgauss * 2.355 * np.exp(
                -(2.355 ** 2) * (new_wavelength - wave) ** 2 / fwhmgauss ** 2 / 2))
            ss = ((new_intensity / (2 * new_J + 1)) * 2 * fwhmgauss / (
                    2 * np.pi * ((new_wavelength - wave) ** 2 + np.power(2 * fwhmgauss, 2) / 4)))
            return tt.sum(), ss.sum(), uu.sum()

    def fwhmgauss(self, wavelength: float):
        """
        高斯展宽的半高宽
        Args:
            wavelength (float): 波长

        Returns:
            返回高斯展宽的半高宽
        """
        return self.fwhm_value


class WidenPart:
    def __init__(self, name, init_data, exp_data: ExpData, n=None, ):
        """
        按组态展宽对象，附属于 CalData 对象
        Args:
            name: 名称
            init_data: 原始数据
            exp_data: 对应的实验数据
            n: 展宽时的点的个数，如果为None，则使用实验数据的波长
        """
        self.name = name
        self.init_data = init_data.copy()
        self.exp_data = exp_data
        self.n = n
        self.only_p = None
        self.delta_lambda: float = 0.0
        self.fwhm_value = 0.5

        self.plot_path_list = {}

        # self.widen_data: Optional[pd.DataFrame] = None
        self.grouped_widen_data: Optional[Dict[str, pd.DataFrame]] = None

    def widen_by_group(self, temperature=25.6):
        """
        按组态进行展宽

        Args:
            temperature: 展宽时的温度

        Returns:
            返回一个字典，包含了按跃迁正例分组后的展宽数据，例如
            {'1-2': pd.DataFrame, '1-3': pd.DataFrame, ...}
            pd.DataFrame的列标题为：wavelength, gaussian, cross-NP, cross-P
        """
        temp_data = {}
        # 按照跃迁正例展宽
        data_grouped = self.init_data.groupby(by=['index_l', 'index_h'])
        for index in data_grouped.groups.keys():
            temp_group = pd.DataFrame(data_grouped.get_group(index))
            temp_result = self.__widen(temperature, temp_group)
            # 如果这个波段没有跃迁正例
            if type(temp_result) == int:
                continue
            temp_data[f'{index[0]}_{index[1]}'] = temp_result
        self.plot_path_list = {}
        for key, value in temp_data.items():
            self.plot_path_list[key] = (
                    PROJECT_PATH() / f'figure/part/{self.name}_{key}.html'
            ).as_posix()
        self.grouped_widen_data = temp_data

    def __widen(self, temperature: float, temp_data: pd.DataFrame, only_p=True):
        """
        展宽

        Args:
            temperature (float): 等离子体温度
            temp_data: 展宽的原始数据
                列标题依次为：energy_l, energy_h, wavelength_ev, intensity, index_l, index_h, J_l, J_h
                分别代表：下态能量，上态能量，波长，强度，下态序号，上态序号，下态J值，上态J值
            only_p: 只计算含有布局的
        Returns:
            返回一个DataFrame，包含了展宽后的数据
            列标题为：wavelength, gaussian, cross-NP, cross-P
            如果only_p为True，则没有cross-NP列和gaussian列
        """
        self.only_p = only_p

        data = temp_data.copy()
        fwhmgauss = self.fwhmgauss
        lambda_range = self.exp_data.x_range

        new_data = data.copy()
        # 找到下态最小能量和最小能量对应的J值
        min_energy = new_data['energy_l'].min()
        min_J = new_data[new_data['energy_l'] == min_energy]['J_l'].min()
        # 筛选波长范围在实验数据范围内的跃迁正例个数
        min_wavelength_nm = lambda_range[0]
        max_wavelength_nm = lambda_range[1]
        min_wavelength_ev = 1239.85 / max_wavelength_nm
        max_wavelength_ev = 1239.85 / min_wavelength_nm
        new_data = new_data[
            (new_data['wavelength_ev'] > min_wavelength_ev)
            & (new_data['wavelength_ev'] < max_wavelength_ev)
            ]
        if new_data.empty:
            result = pd.DataFrame()
            result['wavelength'] = self.exp_data.data['wavelength'].values
            result['gauss'] = np.zeros(self.exp_data.data['wavelength'].values.shape)
            result['cross_NP'] = np.zeros(self.exp_data.data['wavelength'].values.shape)
            result['cross_P'] = np.zeros(self.exp_data.data['wavelength'].values.shape)
            return result
        new_data = new_data.reindex()
        # 获取展宽所需要的数据
        new_wavelength = abs(
            1239.85 / (1239.85 / new_data['wavelength_ev'] + self.delta_lambda)
        )  # 单位时ev
        new_wavelength = new_wavelength.values
        new_intensity = abs(new_data['intensity'])
        new_intensity = new_intensity.values
        flag = new_data['energy_l'] > new_data['energy_h']
        not_flag = np.bitwise_not(flag)
        temp_1 = new_data['energy_l'][flag]
        temp_2 = new_data['energy_h'][not_flag]
        new_energy = temp_1.combine_first(temp_2)
        new_energy = new_energy.values
        temp_1 = new_data['J_l'][flag]
        temp_2 = new_data['J_h'][not_flag]
        new_J = temp_1.combine_first(temp_2)
        new_J = new_J.values
        # 计算布居
        population = ((2 * new_J + 1) * np.exp(-abs(new_energy - min_energy) * 0.124 / temperature) / (2 * min_J + 1))
        if self.n is None:
            wave = 1239.85 / self.exp_data.data['wavelength'].values
        else:
            wave = np.linspace(min_wavelength_ev, max_wavelength_ev, self.n)
        result = pd.DataFrame()
        result['wavelength'] = 1239.85 / wave

        res = [
            self.__complex_cal(
                val, new_intensity, fwhmgauss(val), new_wavelength, population, new_J
            )
            for val in wave
        ]
        res = list(zip(*res))
        if not self.only_p:
            result['gauss'] = res[0]
            result['cross_NP'] = res[1]
        result['cross_P'] = res[2]
        return result

    def plot_widen_by_group(self):
        """
        绘制按组态展宽后的谱线

        """
        for key, value in self.grouped_widen_data.items():
            self.__plot_html(value, self.plot_path_list[key], 'wavelength', 'cross_P')

    def __plot_html(self, data, path, x_name, y_name):
        """
        绘制html文件

        Args:
            data: 要绘制的数据
            path: 生成的文件的路径
            x_name: x轴的列名
            y_name: y轴的列名

        """
        trace1 = go.Scatter(x=data[x_name], y=data[y_name], mode='lines')
        data = [trace1]
        layout = go.Layout(
            margin=go.layout.Margin(autoexpand=False, b=15, l=30, r=0, t=0),
            xaxis=go.layout.XAxis(range=self.exp_data.x_range),
        )
        # yaxis=go.layout.YAxis(range=[self.min_strength, self.max_strength]))
        fig = go.Figure(data=data, layout=layout)
        plot(fig, filename=path, auto_open=False)

    def __complex_cal(
            self,
            wave: float,
            new_intensity: np.array,
            fwhmgauss: float,
            new_wavelength: np.array,
            population: np.array,
            new_J: np.array,
    ):
        """
                展宽时的复杂计算
                Args:
                    wave:
                    new_intensity:
                    fwhmgauss:
                    new_wavelength:
                    population:
                    new_J:

                Returns:
                    展宽后的数据，为一个元组，依次为：gauss, cross_NP, cross_P
                    如果only_p为True，则前两个元素为-1
        """
        uu = ((new_intensity * population / (2 * new_J + 1)) * 2 * fwhmgauss / (
                2 * np.pi * ((new_wavelength - wave) ** 2 + np.power(2 * fwhmgauss, 2) / 4)))
        if self.only_p:
            return -1, -1, uu.sum()
        else:
            tt = (new_intensity / np.sqrt(2 * np.pi) / fwhmgauss * 2.355 * np.exp(
                -(2.355 ** 2) * (new_wavelength - wave) ** 2 / fwhmgauss ** 2 / 2))
            ss = ((new_intensity / (2 * new_J + 1)) * 2 * fwhmgauss / (
                    2 * np.pi * ((new_wavelength - wave) ** 2 + np.power(2 * fwhmgauss, 2) / 4)))
            return tt.sum(), ss.sum(), uu.sum()

    def fwhmgauss(self, wavelength: float):
        """
        高斯展宽的半高宽
        Args:
            wavelength (float): 波长

        Returns:
            返回高斯展宽的半高宽
        """
        return self.fwhm_value


class CowanList:
    def __init__(self):
        """
        用于存储 cowan 对象
        """
        self.chose_cowan: List[str] = []  # 用于存储 cowan 对象在历史列表中的索引
        self.add_or_not: List[bool] = []  # cowan 对象是否被添加

        self.cowan_run_history: Dict[str:Cowan] = {}  # 用于存储 cowan 对象

    def add_cowan(self, key):
        """
        从历史记录中 添加 cowan 对象，如果列表中已经存在就删除再添加

        Args:
            key: 要添加的 cowan 对象的名称（name属性）

        """
        if key in self.chose_cowan:
            self.del_cowan(key)
        self.chose_cowan.append(key)
        self.add_or_not.append(True)

    def del_cowan(self, key):
        """
        删除 cowan 对象

        Args:
            key: 要删除的 cowan 对象的名称（name属性）

        """
        index = self.chose_cowan.index(key)
        self.chose_cowan.pop(index)
        self.add_or_not.pop(index)

    def add_history(self, cowan: Cowan):
        """
        向历史记录中添加 cowan 对象，如果了已经存在，就删除再添加
        如果它存在于已选择的列表中，就就删除再添加

        Args:
            cowan: 要添加的 cowan 对象

        """
        if cowan.name in self.cowan_run_history.keys():
            self.cowan_run_history.pop(cowan.name)
        self.cowan_run_history[cowan.name] = copy.deepcopy(cowan)
        # 如果它存在于已选择的列表中，就更新它
        if cowan.name in self.chose_cowan:
            self.add_cowan(cowan.name)

    def clear_history(self):
        """
        清空历史记录

        如果它存在于已选择的列表中，就不进行删除操作

        """
        keys = list(self.cowan_run_history.keys())
        for key in keys:
            if key not in self.chose_cowan:
                self.cowan_run_history.pop(key)

    def update_exp_data(self, exp_data: ExpData):
        """
        更新所有cowan对象中的exp_data对象

        Args:
            exp_data: 要更新的exp_data对象

        """
        for cowan in self.cowan_run_history.values():
            cowan.exp_data = exp_data

    def __getitem__(self, index):
        return self.cowan_run_history[self.chose_cowan[index]], self.add_or_not[index]


class SimulateSpectral:
    def __init__(self):
        """
        模拟光谱对象，储存于 SpaceTimeResolution 对象中

        """
        self.cowan_list: Optional[List[Cowan]] = None  # 用于存储 cowan 对象
        self.add_or_not: Optional[List[bool]] = None  # cowan 对象是否被添加
        self.exp_data: Optional[ExpData] = None  # 实验光谱数据
        self.spectrum_similarity = None  # 光谱相似度
        self.temperature = None  # 模拟的等离子体温度
        self.electron_density = None  # 模拟的等离子体电子密度

        self.characteristic_peaks = []  # 特征峰波长
        self.peaks_index = []  # 特征峰索引

        self.abundance = []  # 离子丰度
        self.sim_data = None  # 模拟光谱数据

        self.plot_path = PROJECT_PATH().joinpath('figure/add.html').as_posix()
        self.example_path = (
            PROJECT_PATH().joinpath('figure/part/example.html').as_posix()
        )

    def load_exp_data(self, path: Path):
        """
        读取实验光谱数据

        Args:
            path: 实验光谱数据的路径

        """
        self.exp_data = ExpData(path)

    def init_cowan_list(self, cowan_lists: CowanList):
        """
        初始化 cowan_list 和 add_or_not，便于后面的计算

        Args:
            cowan_lists: cowan 对象列表

        """
        temp_list = []
        for key in cowan_lists.chose_cowan:
            temp_list.append(cowan_lists.cowan_run_history[key])
        self.cowan_list = copy.deepcopy(temp_list)
        self.add_or_not = copy.deepcopy(cowan_lists.add_or_not)

    def del_cowan_list(self):
        """
        删除 cowan_list 和 add_or_not，节省内存

        """
        self.cowan_list = None
        self.add_or_not = None

    def get_simulate_data(self, temperature, electron_density):
        """
        获取模拟光谱

        Args:
            temperature: 等离子体温度
            electron_density: 等离子体电子密度

        """
        if self.cowan_list is None or self.add_or_not is None:
            raise Exception('cowan_list 未初始化！！！')
        # 将温度和密度赋值给当前对象
        self.temperature = temperature
        self.electron_density = electron_density
        # 获取各种离子的丰度
        self.__choose_abundance(temperature, electron_density)
        for cowan, flag in zip(self.cowan_list, self.add_or_not):
            if flag:
                cowan.cal_data.widen_all.widen(temperature)
        res = pd.DataFrame()
        res['wavelength'] = self.cowan_list[0].cal_data.widen_all.widen_data['wavelength']
        temp = np.zeros(res.shape[0])
        # temp_np = np.zeros(res.shape[0])
        for cowan, abu, flag in zip(self.cowan_list, self.abundance, self.add_or_not):
            if flag:
                temp += cowan.cal_data.widen_all.widen_data['cross_P'].values * abu
                # print(cowan.name, abu)
                # temp_np += cowan.cal_data.widen_all.widen_data['cross_P'].values
        res['intensity'] = temp
        res['intensity_normalization'] = res['intensity'] / res['intensity'].max()
        # plt.plot(res['wavelength'].values, temp_np, label='np')
        # plt.plot(res['wavelength'].values, temp, label='p')
        # plt.legend()
        # plt.show()

        self.sim_data = res
        self.get_spectrum_similarity()
        return copy.deepcopy(self)

    def plot_html(self, show_point=False):
        """
        绘制叠加光谱

        """
        x1 = self.exp_data.data['wavelength']
        y1 = self.exp_data.data['intensity_normalization']
        x2 = self.sim_data['wavelength']
        y2 = self.sim_data['intensity_normalization']
        trace1 = go.Scatter(
            x=x1, y=y1, mode='lines', line={'color': 'rgb(98, 115, 244)'}
        )

        trace2 = go.Scatter(
            x=x2, y=y2, mode='lines', line={'color': 'rgb(237, 78, 64)'}
        )
        if show_point:
            exp_points_x = [x1.tolist()[index_] for index_ in self.peaks_index[0]]
            exp_points_y = [y1.tolist()[index_] for index_ in self.peaks_index[0]]
            cal_points_x = [x2.tolist()[index_] for index_ in self.peaks_index[1]]
            cal_points_y = [y2.tolist()[index_] for index_ in self.peaks_index[1]]
            trace3 = go.Scatter(
                x=exp_points_x,
                y=exp_points_y,
                mode='markers',
                line={'color': 'rgb(98, 115, 244)'},
            )
            trace4 = go.Scatter(
                x=cal_points_x,
                y=cal_points_y,
                mode='markers',
                line={'color': 'rgb(237, 78, 64)'},
            )
            data = [trace1, trace2, trace3, trace4]
        else:
            data = [trace1, trace2]
        layout = go.Layout(
            margin=go.layout.Margin(autoexpand=False, b=15, l=30, r=0, t=0),
            xaxis=go.layout.XAxis(range=self.exp_data.x_range),
        )
        # yaxis=go.layout.YAxis(range=[self.min_strength, self.max_strength]))
        fig = go.Figure(data=data, layout=layout)
        plot(fig, filename=self.plot_path, auto_open=False)

    def plot_con_contribution_html(self, add_list):
        """
        绘制各个组态的贡献

        Args:
            add_list: 组态选择列表，具体形式如下：
                [[T, [F, T, F, ...]], [T, [F, T, F, ...]], ...]

        """
        height = 0
        trace = []
        for i, c in enumerate(self.cowan_list):
            # i 是CowanList中的索引
            # c 是 Cowan 对象
            if add_list[i][0]:  # 如果这个离子要画在图上
                for j, (key, value) in enumerate(c.cal_data.widen_part.grouped_widen_data.items()):
                    if add_list[i][1][j]:  # 遍历组态
                        index_low, index_high = map(int, key.split('_'))
                        name = '{},{},{}<br />{}'.format(c.name.replace('_', '+'), index_low, index_high,
                                                         c.in36.get_configuration_name(index_low, index_high))
                        if value['cross_P'].max() == 0:
                            trace.append(
                                go.Scatter(
                                    x=value['wavelength'],
                                    y=value['cross_P'] + height,
                                    mode='lines',
                                    name='',
                                    hovertext=name,
                                )
                            )
                        else:
                            trace.append(
                                go.Scatter(
                                    x=value['wavelength'],
                                    y=value['cross_P'] / value['cross_P'].max() + height,
                                    mode='lines',
                                    name='',
                                    hovertext=name,
                                )
                            )
                        height += 1.2
        layout = go.Layout(
            margin=go.layout.Margin(autoexpand=False, b=15, l=30, r=0, t=0),
            xaxis=go.layout.XAxis(range=self.exp_data.x_range),
            # yaxis=go.layout.YAxis(range=[self.min_strength, self.max_strength]))
        )
        fig = go.Figure(data=trace, layout=layout)
        plot(fig, filename=self.example_path, auto_open=False)

    def plot_ion_contribution_html(self, add_list, with_popular):
        """
        绘制各个离子的贡献

        Args:
            add_list: 组态选择列表，具体形式如下：
                [[T, [F, T, F, ...]], [T, [F, T, F, ...]], ...]
            with_popular: 是否考虑布局

        """
        height = 0
        trace = []

        if with_popular:  # 如果考虑离子丰度
            temp_popular = self.abundance
        else:
            temp_popular = [1 for _ in range(len(self.abundance))]
        for i, cowan_ in enumerate(self.cowan_list):
            if add_list[i][0]:
                x = cowan_.cal_data.widen_all.widen_data['wavelength'].values
                y = cowan_.cal_data.widen_all.widen_data['cross_P'].values * temp_popular[i]
                if with_popular:  # 如果考虑丰度
                    trace.append(
                        go.Scatter(
                            x=x,
                            y=y,
                            mode='lines',
                            name='',
                            hovertext=cowan_.name,
                        )
                    )
                else:  # 不考虑丰度
                    trace.append(
                        go.Scatter(
                            x=x,
                            y=y / y.max() + height,
                            mode='lines',
                            name='',
                            hovertext=cowan_.name,
                        )
                    )
                height += 1.2
        layout = go.Layout(
            margin=go.layout.Margin(autoexpand=False, b=15, l=30, r=0, t=0),
            xaxis=go.layout.XAxis(range=self.exp_data.x_range),
            # yaxis=go.layout.YAxis(range=[self.min_strength, self.max_strength]))
        )
        fig = go.Figure(data=trace, layout=layout)
        plot(fig, filename=self.example_path, auto_open=False)

    # 计算离子丰度
    def __choose_abundance(self, temperature, electron_density):
        """
        将所需要的离子丰度挑选出来

        Args:
            temperature: 等离子体温度
            electron_density: 等离子体电子密度

        """
        all_abundance = self.get_abu(temperature, electron_density)
        # print(len(all_abundance))
        temp_abundance = []
        for c in self.cowan_list:
            ion = int(c.name.split('_')[1])
            temp_abundance.append(all_abundance[ion])
        self.abundance = temp_abundance

    def get_abu(self, t, e):
        """
        获取离子丰度

        Args:
            t: 等离子体温度
            e: 等离子体电子密度

        Returns:
            返回一个列表，每个元素为对应离子的丰度
        """
        return self.__cal_abundance2(t, e)

    def __cal_abundance1(self, temperature, electron_density) -> np.ndarray:
        """
        计算各种离子的丰度（用我自己的方法）

        Args:
            temperature: 等离子体温度，单位是ev
            electron_density: 等离子体粒子数密度

        Returns:
            返回一个列表，类型为np.ndarray，每个元素为对应离子的丰度
            例如：[0 1 2 3 4 5 6 7 8]
            分别代表 一次离化，二次离化，三次离化，四次离化，五次离化，六次离化，七次离化，八次离化 九次离化 的粒子数密度
        """
        atomic_num = self.cowan_list[0].in36.atom.num
        ion_num = np.array([i for i in range(atomic_num - 1)])
        ion_energy = np.array(list(IONIZATION_ENERGY[atomic_num].values())[1:])
        electron_num = np.array([self.__get_outermost_num(i) for i in range(1, atomic_num)])

        S = (9 * 1e-6 * electron_num * np.sqrt(temperature / ion_energy) * np.exp(-ion_energy / temperature)) / (
                ion_energy ** 1.5 * (4.88 + temperature / ion_energy))
        Ar = (5.2 * 1e-14 * np.sqrt(ion_energy / temperature) * ion_num * (
                0.429 + 0.5 * np.log(ion_energy / temperature) + 0.469 * np.sqrt(temperature / ion_energy)))
        A3r = (2.97 * 1e-27 * electron_num / (temperature * ion_energy ** 2 * (4.88 + temperature / ion_energy)))
        ratio = S / (Ar + electron_density * A3r)
        abundance = self.__calculate_a_over_S(ratio)
        return abundance

    def __cal_abundance2(self, temperature, electron_density):
        """
        使用fortran程序中的方法计算离子丰度

        Args:
            temperature: 等离子体温度，单位是ev
            electron_density: 等离子体粒子数密度

        Returns:
            返回一个列表，每个元素为对应离子的丰度
        """
        atomic_num = self.cowan_list[0].in36.atom.num
        ion_num = np.array([i for i in range(atomic_num)])
        ion_energy = np.array(list(IONIZATION_ENERGY[atomic_num].values()))
        electron_num = np.array([self.__get_outermost_num(i) for i in range(atomic_num)])

        S = (9 * 1e-6 * electron_num * np.sqrt(temperature / ion_energy) * np.exp(-ion_energy / temperature)) / (
                ion_energy ** 1.5 * (4.88 + temperature / ion_energy))
        Ar = (5.2 * 1e-14 * np.sqrt(ion_energy / temperature) * ion_num * (
                0.429 + 0.5 * np.log(ion_energy / temperature) + 0.469 * np.sqrt(temperature / ion_energy)))
        A3r = (2.97 * 1e-27 * electron_num / (temperature * ion_energy ** 2 * (4.88 + temperature / ion_energy)))
        Co = S / (Ar + electron_density * A3r)
        CoM = [Co[0]]
        for i in range(1, atomic_num):
            CoM.append(Co[i] * CoM[i - 1])
        Cosum = 0
        CoMM = []
        for i in range(atomic_num):
            CoMM.append((i + 1) * CoM[i])
            Cosum += CoMM[i]
        Rat = [electron_density / Cosum]
        for i in range(1, atomic_num):
            Rat.append(Co[i - 1] * Rat[i - 1])
        Ratsum = sum(Rat)
        aveion = electron_density / Ratsum
        Ratio = []
        for i in range(atomic_num):
            if Rat[i] / Ratsum < 1e-4:
                Ratio.append(0)
            else:
                Ratio.append(Rat[i] / Ratsum)
        return Ratio

    def __get_outermost_num(self, ion: int):
        """
        获取离子的最外层电子数

        Args:
            ion: 离化度，0为原子，1为1次离化，2为2次离化，以此类推

        Returns:
            electron_num : 最外层电子数
        """
        temp_electron_num = self.cowan_list[0].in36.atom.num - ion
        for n in range(1, 7):
            if temp_electron_num > 2 * n ** 2:
                temp_electron_num -= 2 * n ** 2
            else:
                electron_num = temp_electron_num
                return electron_num

    @staticmethod
    def __calculate_a_over_S(a_ratios):
        """
        已知a1/a2, a2/a3, ..., a_n-1/a_n，计算a1/S, a2/S, ..., a_n/S，其中S=a1+a2+...+a_n

        Args:
            a_ratios: a1/a2, a2/a3, ..., a_n-1/a_n

        Returns:
            a1/S, a2/S, ..., a_n/S
        """
        a = np.zeros(len(a_ratios) + 1)
        a[0] = 1
        for i in range(1, len(a)):
            a[i] = a[i - 1] * a_ratios[i - 1]

        # 计算S
        S = np.sum(a)

        # 计算a1/S, a2/S, ..., a_n/S
        a_over_S = a / S

        return a_over_S

    def get_spectrum_similarity(self):
        """
        获取光谱相似度，直接存储在 self.spectrum_similarity 中

        """
        if len(self.characteristic_peaks) == 0:
            self.spectrum_similarity = self.spectrum_similarity1(
                self.exp_data.data[['wavelength', 'intensity']],
                self.sim_data[['wavelength', 'intensity']],
            )
        else:
            self.spectrum_similarity = self.spectrum_similarity2(
                self.exp_data.data[['wavelength', 'intensity']],
                self.sim_data[['wavelength', 'intensity']],
            )

    def spectrum_similarity1(self, fax: pd.DataFrame, fbx: pd.DataFrame):
        """
        自动峰值匹配法

        Args:
            fax:
            fbx:

        """
        x, y1, y2 = self.get_y1y2(fax, fbx)
        peaks1, _ = find_peaks(y1)
        peaks2, _ = find_peaks(y2)
        d = {}
        for index in peaks2:
            d[index] = y2[index]
        peaks2 = sorted(d.items(), key=lambda item: item[1], reverse=True)
        peaks2 = list(zip(*peaks2[:5]))[0]
        temp_peaks = []
        for index in peaks2:
            min_index, temp = -1, abs(index - peaks1[0])
            for i, index_1 in enumerate(peaks1[1:]):
                if temp > abs(index - index_1):
                    temp = abs(index - index_1)
                    min_index = i + 1
            temp_peaks.append(peaks1[min_index])
        peaks1 = temp_peaks

        new_peaks2 = []
        for index in peaks2:
            temp_index = np.argmin(np.abs(x[index] - self.sim_data['wavelength'].values))
            new_peaks2.append(temp_index)
        self.peaks_index = [peaks1, new_peaks2]

        similarity = 0
        for i in range(len(peaks1) - 1):
            for j in range(i + 1, len(peaks1)):
                similarity += abs(
                    y1[peaks1[i]] / y1[peaks1[j]] - y2[peaks2[i]] / y2[peaks2[j]]
                )
        if similarity > len(peaks1):
            similarity = len(peaks1)
        return similarity

    def spectrum_similarity2(self, fax: pd.DataFrame, fbx: pd.DataFrame):
        """
        指定峰值匹配法，自动匹配实验谱线的峰
        Args:
            fax: 实验数据
            fbx: 计算数据

        """
        # 拿到一维的数据
        x, y1, y2 = self.get_y1y2(fax, fbx)
        # 找出模拟光谱的峰值位置
        peaks2, _ = find_peaks(y2)
        # 指出模拟光谱谱峰对应的波长
        peaks2_wavelength = np.array([x[index] for index in peaks2])
        # 将给定的特征峰的强度与模拟光谱特征峰的强度进行比较
        exp_wavelength_indexes = []  # 用来存放实验谱峰的索引值
        cal_wavelength_indexes = []  # 用来存放计算谱峰的索引值
        for wavelength in self.characteristic_peaks:
            exp_index = np.argmin(abs(x - wavelength))
            # min_index: wavelength 所对应的峰在 peaks2 中的索引
            # temp: wavelength 所对应的峰与 peaks2 中最近的峰的距离
            min_index, temp = 0, abs(wavelength - peaks2_wavelength[0])
            for i, index_1 in enumerate(peaks2_wavelength[1:]):
                if temp > abs(wavelength - index_1):
                    temp = abs(wavelength - index_1)
                    min_index = i + 1
            exp_wavelength_indexes.append(exp_index)
            cal_wavelength_indexes.append(peaks2[min_index])
        # 如果对应谱峰太远，就直接赋值
        for i in range(len(exp_wavelength_indexes)):
            if abs(exp_wavelength_indexes[i] - cal_wavelength_indexes[i]) > (len(x)) * 0.01:
                cal_wavelength_indexes[i] = exp_wavelength_indexes[i]

        new_cal_wavelength_indexes = []
        for index in cal_wavelength_indexes:
            temp_index = np.argmin(np.abs(x[index] - self.sim_data['wavelength'].values))
            new_cal_wavelength_indexes.append(temp_index)
        self.peaks_index = [exp_wavelength_indexes, new_cal_wavelength_indexes]

        # 计算两个光谱数据峰值位置以及强度的相似性
        similarity = 0
        for i in range(len(exp_wavelength_indexes) - 1):
            for j in range(i + 1, len(exp_wavelength_indexes)):
                similarity += abs(
                    y1[exp_wavelength_indexes[i]] / y1[exp_wavelength_indexes[j]]
                    - y2[cal_wavelength_indexes[i]] / y2[cal_wavelength_indexes[j]]
                )
        if similarity > len(exp_wavelength_indexes) * 3:
            similarity = len(exp_wavelength_indexes) * 3
        return similarity

    def spectrum_similarity3(self, fax: pd.DataFrame, fbx: pd.DataFrame):
        """
        指定峰值匹配法，直接通过波长取峰
        Args:
            fax:
            fbx:

        """
        x, y1, y2 = self.get_y1y2(fax, fbx)
        exp_wavelength_indexes = []
        # 将给定的特征峰的强度与模拟光谱特征峰的强度进行比较
        for wavelength in self.characteristic_peaks:
            exp_index = np.argmin(abs(x - wavelength))
            exp_wavelength_indexes.append(exp_index)

        new_cal_wavelength_indexes = []
        for index in exp_wavelength_indexes:
            temp_index = np.argmin(np.abs(x[index] - self.sim_data['wavelength'].values))
            new_cal_wavelength_indexes.append(temp_index)
        self.peaks_index = [exp_wavelength_indexes, new_cal_wavelength_indexes]

        # 计算两个光谱数据峰值位置以及强度的相似性
        similarity = 0
        for i in range(len(exp_wavelength_indexes) - 1):
            for j in range(i + 1, len(exp_wavelength_indexes)):
                similarity += abs(
                    y1[exp_wavelength_indexes[i]] / y1[exp_wavelength_indexes[j]]
                    - y2[exp_wavelength_indexes[i]] / y2[exp_wavelength_indexes[j]]
                )
        if similarity > len(exp_wavelength_indexes) * 3:
            similarity = len(exp_wavelength_indexes) * 3
        return similarity

    @staticmethod
    def get_y1y2(fax: pd.DataFrame, fbx: pd.DataFrame, min_x=None, max_x=None):
        col_names_a = fax.columns
        col_names_b = fbx.columns
        if (min_x is None) and (max_x is None):
            min_x = max(fax[col_names_a[0]].min(), fbx[col_names_b[0]].min())
            max_x = min(fax[col_names_a[0]].max(), fbx[col_names_b[0]].max())
        fax_new = fax[(fax[col_names_a[0]] <= max_x) & (min_x <= fax[col_names_a[0]])]
        fbx_new = fbx[(fbx[col_names_b[0]] <= max_x) & (min_x <= fbx[col_names_b[0]])]
        f2 = interp1d(
            fbx_new[col_names_b[0]], fbx_new[col_names_b[1]], fill_value='extrapolate'
        )
        x = fax_new[col_names_a[0]].values
        y1 = fax_new[col_names_a[1]].values
        y2 = f2(x)
        y1 = y1 / max(y1)
        y2 = y2 / max(y2)
        return x, y1, y2


class SimulateGrid:
    def __init__(self, temperature, density, simulate):
        """
        用于存储模拟光谱的网格数据

        Args:
            temperature: 温度范围 [开始 结束 个数]
            density: 密度范围 [开始底数 开始指数 结束底数 结束指数 个数]
            simulate: 要模拟的simulate对象
        """
        super().__init__()
        self.task = 'cal'
        self.update_exp = None

        self.simulate = copy.deepcopy(simulate)
        self.temperature_tuple = temperature
        self.density_tuple = density
        self.t_num: int = int(temperature[-1])
        self.ne_num: int = int(density[-1])
        t_list = np.linspace(temperature[0], temperature[1], self.t_num)
        ne_list = np.power(
            10,
            np.linspace(
                np.log10(density[0] * 10 ** density[1]),
                np.log10(density[2] * 10 ** density[3]),
                self.ne_num,
            ),
        )
        self.t_list = ['{:.3f}'.format(v) for v in t_list]
        self.ne_list = ['{:.3e}'.format(v) for v in ne_list]

        self.grid_data = {}

    def change_task(self, task, *args):
        """
        切换任务

        Args:
            task: 任务名称 'cal' 计算网格数据 'update' 更新网格数据
            *args: 在更新网格时，需要传入一个实验光谱对象

        """
        if task in ['cal', 'update']:
            self.task = task
        if task == 'update':
            self.update_exp = args[0]


class SimulateGridThread(QtCore.QThread):
    progress = Signal(str)  # 计数完成后发送一次信号
    end = Signal(str)  # 计数完成后发送一次信号
    up_end = Signal(str)  #

    def __init__(self, old_grid: SimulateGrid):
        """
        用于多线程模拟光谱的网格数据

        Args:
            old_grid: 旧的网格数据对象
        """
        super().__init__()
        self.old_grid = old_grid
        self.task = old_grid.task
        self.update_exp = old_grid.update_exp

        self.simulate = old_grid.simulate
        self.temperature_tuple = old_grid.temperature_tuple
        self.density_tuple = old_grid.density_tuple
        self.t_num: int = old_grid.t_num
        self.ne_num: int = old_grid.ne_num

        self.t_list = old_grid.t_list
        self.ne_list = old_grid.ne_list

        self.grid_data = old_grid.grid_data

    def run(self):
        """
        多线程运行的主函数

        """
        if self.task == 'cal':
            self.cal_grid()
        elif self.task == 'update':
            self.update_similarity(self.update_exp)

    def cal_grid(self):
        """
        计算网格数据

        """

        def callback(t, ne, f):
            """
            回调函数，用于更新进度条以及获取结果
            Args:
                t: 温度（用作键值对）
                ne: 密度（用作键值对）
                f: 函数对象（用于获取结果）

            """
            nonlocal current_progress
            current_progress += 1
            temp_cowan = f.result()
            temp_cowan.cowan_list = None
            temp_cowan.add_or_not = None
            self.grid_data[(t, ne)] = temp_cowan
            self.progress.emit(str(int(current_progress / self.t_num / self.ne_num * 100)))

        # 多线程
        self.grid_data = {}
        current_progress = 0
        pool = ProcessPoolExecutor(os.cpu_count())
        for temperature in self.t_list:
            for density in self.ne_list:
                future = pool.submit(self.simulate.get_simulate_data, eval(temperature), eval(density))
                future.add_done_callback(functools.partial(callback, temperature, density))
        pool.shutdown()
        self.end.emit(0)

        # 单线程
        # self.grid_data = {}
        # for temperature in self.t_list:
        #     for density in self.ne_list:
        #         self.simulate.get_simulate_data(eval(temperature), eval(density))
        #         self.grid_data[(temperature, density)] = copy.deepcopy(self.simulate)

    def update_similarity(self, exp_obj):
        """
        更新网格数据的相似度

        Args:
            exp_obj: 实验光谱对象

        """
        for key, value in self.grid_data.items():
            self.simulate = copy.deepcopy(value)
            self.simulate.exp_data = copy.deepcopy(exp_obj)
            self.simulate.get_spectrum_similarity()
            self.grid_data[key] = copy.deepcopy(self.simulate)
        self.up_end.emit(0)

    def update_origin(self):
        """
        更新原始的网格数据

        """
        self.old_grid.task = self.task
        self.old_grid.update_exp = self.update_exp
        self.old_grid.simulate = self.simulate
        self.old_grid.temperature_tuple = self.temperature_tuple
        self.old_grid.density_tuple = self.density_tuple
        self.old_grid.t_num = self.t_num
        self.old_grid.ne_num = self.ne_num
        self.old_grid.t_list = self.t_list
        self.old_grid.ne_list = self.ne_list
        self.old_grid.grid_data = self.grid_data


class SpaceTimeResolution:
    def __init__(self):
        """
        用于存储空间时间分辨光谱
        """
        # 模拟光谱数据对象 列表
        self.simulate_spectral_dict = {}

        self.change_by_time_path = (PROJECT_PATH().joinpath('figure/change/by_time.html').as_posix())
        self.change_by_location_path = (PROJECT_PATH().joinpath('figure/change/by_location.html').as_posix())
        self.change_by_space_time_path = (PROJECT_PATH().joinpath('figure/change/by_space_time.html').as_posix())

    def add_st(self, st: tuple, simulate_spectral):
        """
        添加一个位置时间的是按分辨光谱

        Args:
            st: 时间位置，格式为 (t，(x, y, z)) 类型为字符串
            simulate_spectral: 模拟光谱数据对象

        """
        temp = copy.deepcopy(simulate_spectral)
        temp.del_cowan_list()
        self.simulate_spectral_dict[st] = temp

    def del_st(self, st):
        self.simulate_spectral_dict.pop(st)

    def plot_change_by_time(self, location: Tuple[str, str, str]):
        """
        绘制温度和电子密度随时间变化的图像（在指定的位置处）

        Args:
            location: 位置

        """
        times = []
        for key, value in self.simulate_spectral_dict.items():
            if key[1] == location:
                times.append(eval(key[0]))
        times = sorted(times)
        temperature = []
        electron_density = []
        for time in times:
            temperature.append(self.simulate_spectral_dict[(str(time), location)].temperature)
            electron_density.append(self.simulate_spectral_dict[(str(time), location)].electron_density)

        trace1 = go.Scatter(x=times, y=temperature, mode='lines')
        trace2 = go.Scatter(x=times, y=electron_density, mode='lines', yaxis='y2')
        data = [trace1, trace2]
        layout = go.Layout(
            margin=go.layout.Margin(autoexpand=True, b=15, l=30, r=0, t=0),
            yaxis2=dict(anchor='x', overlaying='y', side='right'),  # 设置坐标轴的格式，一般次坐标轴在右侧
            # xaxis=go.layout.XAxis(range=self.exp_data.x_range),
        )
        fig = go.Figure(data=data, layout=layout)
        plot(fig, filename=self.change_by_time_path, auto_open=False)

    def plot_change_by_location(self, time):
        """
        绘制温度和电子密度随位置变化的图像（在指定的时间处）

        Args:
            time: 时间

        """
        x_s = []
        for key, value in self.simulate_spectral_dict.items():
            if key[0] == time:
                x_s.append(eval(key[1][0]))
        x_s = sorted(x_s)

        temperature = {}
        electron_density = {}

        for x in x_s:
            temperature[(x, 0, 0)] = self.simulate_spectral_dict[(time, (str(x), '0', '0'))].temperature
            electron_density[(x, 0, 0)] = self.simulate_spectral_dict[(time, (str(x), '0', '0'))].electron_density

        def fun(xx, yy=0, zz=0):
            return temperature[(xx, yy, zz)], electron_density[(xx, yy, zz)]

        trace1 = go.Scatter(x=x_s, y=[fun(v)[0] for v in x_s], mode='lines')
        trace2 = go.Scatter(x=x_s, y=[fun(v)[1] for v in x_s], mode='lines', yaxis='y2')
        data = [trace1, trace2]
        layout = go.Layout(
            margin=go.layout.Margin(autoexpand=True, b=15, l=30, r=0, t=0),
            yaxis2=dict(anchor='x', overlaying='y', side='right'),  # 设置坐标轴的格式，一般次坐标轴在右侧
            # xaxis=go.layout.XAxis(range=self.exp_data.x_range),
        )
        fig = go.Figure(data=data, layout=layout)
        plot(fig, filename=self.change_by_location_path, auto_open=False)

    def plot_change_by_space_time(self, var_index):
        """
        绘制温度和电子密度随位置和时间变化的图像

        Args:
            var_index: 选择是温度还是时间 0：温度 1：密度

        """
        spaces = []
        times = []
        for key in self.simulate_spectral_dict:
            if key[0] not in times:
                times.append(key[0])
            if key[1][0] not in spaces:
                spaces.append(key[1][0])
        spaces = sorted(spaces, key=lambda x: eval(x))
        times = sorted(times, key=lambda x: eval(x))
        t_res = []
        d_res = []
        for time in times:
            temp_t_res = []
            temp_d_res = []
            for space in spaces:
                temp_t_res.append(
                    self.simulate_spectral_dict[(time, (space, '0', '0'))].temperature
                )
                temp_d_res.append(
                    self.simulate_spectral_dict[
                        (time, (space, '0', '0'))
                    ].electron_density
                )
            t_res.append(temp_t_res)
            d_res.append(temp_d_res)

        if var_index == 0:
            trace1 = go.Heatmap(x=spaces, y=times, z=t_res)
        else:
            trace1 = go.Heatmap(x=spaces, y=times, z=d_res)
        data = [trace1]
        layout = go.Layout(
            margin=go.layout.Margin(b=15, l=60, r=0, t=0),
            # yaxis={
            #     'type': 'log',
            #     'tickformat': '.2e'
            # }
        )
        fig = go.Figure(data=data, layout=layout)
        plot(fig, filename=self.change_by_space_time_path, auto_open=False)
