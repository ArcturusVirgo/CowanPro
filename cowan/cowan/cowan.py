import copy
import functools
import os
import shutil
import subprocess
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from typing import Optional, List, Dict

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import scipy
from PySide6 import QtCore
from PySide6.QtCore import Signal
from fastdtw import fastdtw
from plotly.offline import plot
from scipy.interpolate import interp1d
from scipy.signal import find_peaks

from cowan.constant import *
from .atom_info import *


class Atom:
    def __init__(self, num: int, ion: int):
        self.num = num  # 原子序数
        self.symbol = ATOM[self.num][0]  # 元素符号
        self.name = ATOM[self.num][1]  # 元素名称
        self.ion = ion  # 离化度
        self.electron_num = self.num - self.ion  # 实际的电子数量
        self.electron_arrangement = self.get_base_electron_arrangement()
        self.base_configuration = self.get_base_configuration()  # 基组态

    def get_base_electron_arrangement(self):
        """
            获取电子基组态的核外排布情况

        Returns:
            返回一个字典，键为子壳层，值为子壳层的电子数
            例如 {
                '1s': 2,
                '2s': 2,
                '2p': 6,
                '3s': 2,
                '3p': 4,
            }

        """
        electron_arrangement = {}
        for key, value in map(lambda x: [str(x[:2]), int(x[2:])], BASE_CONFIGURATION[self.electron_num].split(' ')):
            electron_arrangement[key] = value
        return electron_arrangement

    def revert_to_ground_state(self):
        """
            将电子排布状态重置为基态基态
        """
        self.electron_arrangement = self.get_base_electron_arrangement()

    def get_base_configuration(self):
        self.electron_arrangement = self.get_base_electron_arrangement()
        return self.get_configuration()

    def get_configuration(self) -> str:
        """
            根据当前的电子排布情况，获取当前的电子组态

        Returns:
            返回一个字符串
            例如 1. 基态：3s02 3p04
                2. 激发态： 3s02 3p03 4s01
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
            激发电子，改变电子排布情况

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
        self.electron_arrangement[high_name] = self.electron_arrangement.get(high_name, 0) + 1
        if self.electron_arrangement[low_name] == 0:
            self.electron_arrangement.pop(low_name)


class ExpData:
    def __init__(self, filepath: Path):
        self.plot_path = (PROJECT_PATH / 'figure/exp.html').as_posix()
        self.filepath: Path = filepath

        self.data: Optional[pd.DataFrame] = None
        self.x_range: Optional[List[float]] = None

        self.__read_file()

    def set_range(self, x_range: List[float]):
        """
        设置x轴范围
        Args:
            x_range: x轴范围，单位是nm
        """
        self.x_range = x_range
        self.data = self.data[(self.data['wavelength'] < self.x_range[1]) &
                              (self.data['wavelength'] > self.x_range[0])]

    def __read_file(self):
        """
        读取实验数据
        设置最小值和最大值
        """
        filetype = self.filepath.suffix[1:]
        if filetype == 'csv':
            temp_data = pd.read_csv(self.filepath, sep=',', skiprows=1, names=['wavelength', 'intensity'])
        elif filetype == 'txt':
            temp_data = pd.read_csv(self.filepath, sep='\s+', skiprows=1, names=['wavelength', 'intensity'])
        else:
            raise ValueError(f'filetype {filetype} is not supported')
        temp_data['intensity_normalization'] = temp_data['intensity'] / temp_data['intensity'].max()

        self.data = temp_data
        self.x_range = [self.data['wavelength'].min(), self.data['wavelength'].max()]

    def plot_html(self):
        trace1 = go.Scatter(x=self.data['wavelength'], y=self.data['intensity'], mode='lines')
        data = [trace1]
        layout = go.Layout(margin=go.layout.Margin(autoexpand=False, b=15, l=30, r=0, t=0),
                           xaxis=go.layout.XAxis(range=self.x_range), )
        # yaxis=go.layout.YAxis(range=[self.min_strength, self.max_strength]))
        fig = go.Figure(data=data, layout=layout)

        plot(fig, filename=self.plot_path, auto_open=False)


class In36:
    def __init__(self, atom):
        self.atom: Atom = copy.deepcopy(atom)

        self.control_card = ['2', ' ', ' ', '-9', ' ', '  ', ' 2', '   ', '10', '  1.0', '    5.e-08', '    1.e-11',
                             '-2', '  ', ' ', '1', '90', '  ', '  1.0', ' 0.65', '  0.0', '  0.0', '     ']
        self.configuration_card = []

    def read_from_file(self, path: Path):
        """
        读取in36文件
        Args:
            path (Path): in36文件的路径
        """
        with open(path, 'r') as f:
            lines = f.readlines()
        # 控制卡读入
        control_card_text = lines[0]
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
            v1 = '{:>9}'.format(value[1])
            v2 = '{:>7}'.format(value[2])
            v3 = '             '
            v4 = ' '.join(value[3:])
            input_card_list.append([[v0, v1, v2, v3, v4], self.__judge_parity(v4)])
        self.control_card, self.configuration_card = control_card_list, input_card_list

        # 更新原子信息
        num = int(self.configuration_card[0][0][0].split(' ')[-1])
        ion = int(self.configuration_card[0][0][1].split('+')[-1])
        self.atom = Atom(num=num, ion=ion)

    def add_configuration(self, configuration: str):
        """
        添加组态（会自动剔除重复数据）
        Args:
            configuration(str): 要添加的组态
        """
        if self.configuration_card:  # 如果组态卡不为空
            temp_list = list(zip(*list(zip(*self.configuration_card))[0]))[-1]
        else:  # 如果组态卡为空
            temp_list = []
        if configuration not in temp_list:
            v0 = '{:>5}'.format(self.atom.num)
            v1 = '{:>9}'.format(f'{self.atom.ion + 1}{ATOM[self.atom.num][0]}+{self.atom.ion}')
            v2 = '{:>7}'.format('11111')
            v3 = '             '
            v4 = configuration
            self.configuration_card.append([[v0, v1, v2, v3, v4], self.__judge_parity(v4)])

    def configuration_move(self, index, opt: str):
        if opt == 'up':
            if 1 <= index <= len(self.configuration_card):
                self.configuration_card[index], self.configuration_card[index - 1] \
                    = self.configuration_card[index - 1], self.configuration_card[index]
        elif opt == 'down':
            if 0 <= index <= len(self.configuration_card) - 2:
                self.configuration_card[index], self.configuration_card[index + 1] \
                    = self.configuration_card[index + 1], self.configuration_card[index]
        else:
            raise ValueError('opt must be "up" or "down"')

    def del_configuration(self, index):
        self.configuration_card.pop(index)

    def get_text(self):
        in36 = ''
        in36 += ''.join(self.control_card)
        in36 += '\n'
        for v in self.configuration_card:
            in36 += ''.join(v[0])
            in36 += '\n'
        in36 += '   -1\n'
        return in36

    def save(self, path: Path):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(self.get_text())

    @staticmethod
    def __judge_parity(configuration: str) -> int:
        """
        判断指定组态的宇称
            Args:
                configuration: 要判断的电子组态

            Returns:
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
        self.input_card: List[str] = ['g5inp', '  ', '0', ' 0', '0', '00', '  0.000', ' ', '00000000', ' 0000000',
                                      '   00000', ' 000', '0', '90', '99', '90', '90', '90', '.0000', '     ', '0', '7',
                                      '2', '2', '9', '     ']

    def read_from_file(self, path):
        with open(path, "r") as f:
            line = f.readline()
        line = line.strip('\n')
        if len(line) != 80:
            line += ' ' * (80 - len(line) - 1)
        rules = [5, 2, 1, 2, 1, 2, 7, 1, 8, 8, 8, 4, 1, 2, 2, 2, 2, 2, 5, 5, 1, 1, 1, 1, 1, 5]
        input_card_list = []
        for rule in rules:
            input_card_list.append(line[:rule])
            line = line[rule:]
        self.input_card = input_card_list

    def get_text(self):
        in2 = ''
        in2 += ''.join(self.input_card)
        in2 += '\n'
        in2 += '        -1\n'
        return in2

    def save(self, path: Path):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(self.get_text())


class Cowan:
    def __init__(self, in36, in2, name, exp_data, coupling_mode=1):
        self.in36: In36 = copy.deepcopy(in36)
        self.in2: In2 = copy.deepcopy(in2)
        self.name: str = name
        self.exp_data: ExpData = copy.deepcopy(exp_data)
        self.coupling_mode = coupling_mode  # 1是L-S耦合 2是j-j耦合

        self.cal_data: Optional[CalData] = None
        self.run_path = PROJECT_PATH / f'cal_result/{self.name}'

    def run(self, delta_lambda=0.0):
        """
        运行 Cowan 程序，创建 cal_data 对象
        Returns:

        """
        self.__get_ready()
        # 获取最初的运行路径
        original_path = Path.cwd()

        # 运行文件
        os.chdir(self.run_path)
        rcn = subprocess.run('./RCN.exe')
        rcn2 = subprocess.run('./RCN2.exe')
        self.__edit_ing11()
        rcg = subprocess.run('./RCG.exe')
        os.chdir(original_path)

        # 更新 cal_data 对象
        self.cal_data = CalData(self.name, self.exp_data)

    def __get_ready(self):
        if self.run_path.exists():
            shutil.rmtree(self.run_path)
        shutil.copytree(PROJECT_PATH / 'bin', self.run_path)
        self.in36.save(self.run_path / 'in36')
        self.in2.save(self.run_path / 'in2')

    def __edit_ing11(self):
        with open('./out2ing', 'r', encoding='utf-8') as f:
            text = f.read()
        text = f'    {self.coupling_mode}{text[5:]}'
        with open('./ing11', 'w', encoding='utf-8') as f:
            f.write(text)
        with open('./out2ing', 'w', encoding='utf-8') as f:
            f.write(text)


class CalData:
    def __init__(self, name, exp_data: ExpData):
        self.name = name
        self.exp_data = exp_data
        self.filepath = (PROJECT_PATH / f'cal_result/{name}/spectra.dat').as_posix()
        self.plot_path = (PROJECT_PATH / f'figure/line/{name}.html').as_posix()
        self.init_data: pd.DataFrame | None = None

        self.widen_all: Optional[WidenAll] = None
        self.widen_part: Optional[WidenPart] = None

        self.read_file()

    def read_file(self):
        self.init_data = pd.read_csv(self.filepath, sep='\s+',
                                     names=['energy_l', 'energy_h', 'wavelength_ev', 'intensity',
                                            'index_l', 'index_h', 'J_l', 'J_h'])
        self.widen_all = WidenAll(self.name, self.init_data, self.exp_data)
        self.widen_part = WidenPart(self.name, self.init_data, self.exp_data)

    def plot_line(self):
        temp_data = self.__get_line_data(self.init_data[['wavelength_ev', 'intensity']])
        trace1 = go.Scatter(x=temp_data['wavelength'], y=temp_data['intensity'], mode='lines')
        data = [trace1]
        layout = go.Layout(margin=go.layout.Margin(autoexpand=False, b=15, l=30, r=0, t=0),
                           xaxis=go.layout.XAxis(range=self.exp_data.x_range),
                           )
        # yaxis=go.layout.YAxis(range=[self.min_strength, self.max_strength]))
        fig = go.Figure(data=data, layout=layout)
        plot(fig, filename=self.plot_path, auto_open=False)

    def __get_line_data(self, origin_data):
        temp_data = origin_data.copy()
        temp_data['wavelength'] = 1239.85 / temp_data['wavelength_ev']
        temp_data = temp_data[(temp_data['wavelength'] < self.exp_data.x_range[1]) &
                              (temp_data['wavelength'] > self.exp_data.x_range[0])]
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
        temp = pd.DataFrame({
            'wavelength': lambda_,
            'intensity': strength
        })
        return temp


class WidenAll:
    def __init__(self,
                 name,
                 init_data,
                 exp_data: ExpData,
                 delta_lambda=0.0,  # 单位是nm
                 n=None, ):
        self.name = name
        self.init_data = init_data.copy()
        self.exp_data = exp_data
        self.delta_lambda: float = delta_lambda
        self.n = n
        self.only_p = None

        self.plot_path_gauss = (PROJECT_PATH / f'figure/gauss/{self.name}.html').as_posix()
        self.plot_path_cross_NP = (PROJECT_PATH / f'figure/cross_NP/{self.name}.html').as_posix()
        self.plot_path_cross_P = (PROJECT_PATH / f'figure/cross_P/{self.name}.html').as_posix()

        self.widen_data: pd.DataFrame | None = None

    def widen(self, temperature: float, only_p=True):
        """
            列标题依次为：energy_l, energy_h, wavelength_ev, intensity, index_l, index_h, J_l, J_h
            分别代表：下态能量，上态能量，波长，强度，下态序号，上态序号，下态J值，上态J值
        Args:
            only_p: 只计算含有布局的
            temperature (float): 等离子体温度
        Returns:
            返回一个DataFrame，包含了展宽后的数据
            列标题为：wavelength, gaussian, cross-NP, cross-P
        """
        self.only_p = only_p

        data = self.init_data.copy()
        fwhmgauss = self.__fwhmgauss
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
        new_data = new_data[(new_data['wavelength_ev'] > min_wavelength_ev) &
                            (new_data['wavelength_ev'] < max_wavelength_ev)]
        if new_data.empty:
            result = pd.DataFrame()
            result['wavelength'] = [0, 0]
            result['gauss'] = [0, 0]
            result['cross_NP'] = [0, 0]
            result['cross_P'] = [0, 0]
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
        population = (2 * new_J + 1) * np.exp(-abs(new_energy - min_energy) * 0.124 / temperature) / (2 * min_J + 1)
        if self.n is None:
            wave = 1239.85 / np.array(self.exp_data.data['wavelength'].values)
        else:
            wave = np.linspace(min_wavelength_ev, max_wavelength_ev, self.n)
        result = pd.DataFrame()
        result['wavelength'] = 1239.85 / wave

        res = [self.__complex_cal(val, new_intensity, fwhmgauss(val), new_wavelength, population, new_J)
               for val in wave]
        res = list(zip(*res))
        if not self.only_p:
            result['gauss'] = res[0]
            result['cross_NP'] = res[1]
        result['cross_P'] = res[2]
        self.widen_data = result

    def plot_widen(self):
        if not self.only_p:
            self.__plot_html(self.widen_data, self.plot_path_gauss, 'wavelength', 'gauss')
            self.__plot_html(self.widen_data, self.plot_path_cross_NP, 'wavelength', 'cross_NP')
        self.__plot_html(self.widen_data, self.plot_path_cross_P, 'wavelength', 'cross_P')

    def __plot_html(self, data, path, x_name, y_name):
        trace1 = go.Scatter(x=data[x_name], y=data[y_name], mode='lines')
        data = [trace1]
        layout = go.Layout(margin=go.layout.Margin(autoexpand=False, b=15, l=30, r=0, t=0),
                           xaxis=go.layout.XAxis(range=self.exp_data.x_range),
                           )
        # yaxis=go.layout.YAxis(range=[self.min_strength, self.max_strength]))
        fig = go.Figure(data=data, layout=layout)
        plot(fig, filename=path, auto_open=False)

    def __complex_cal(self,
                      wave: float,
                      new_intensity: np.array,
                      fwhmgauss: float,
                      new_wavelength: np.array,
                      population: np.array,
                      new_J: np.array):
        uu = (new_intensity * population / (2 * new_J + 1)) * 2 * fwhmgauss / (
                2 * np.pi * ((new_wavelength - wave) ** 2 + np.power(2 * fwhmgauss, 2) / 4))
        if self.only_p:
            return -1, -1, uu.sum()
        else:
            tt = new_intensity / np.sqrt(2 * np.pi) / fwhmgauss * 2.355 * np.exp(
                -2.355 ** 2 * (new_wavelength - wave) ** 2 / fwhmgauss ** 2 / 2)
            ss = (new_intensity / (2 * new_J + 1)) * 2 * fwhmgauss / (
                    2 * np.pi * ((new_wavelength - wave) ** 2 + np.power(2 * fwhmgauss, 2) / 4))
            return tt.sum(), ss.sum(), uu.sum()

    @staticmethod
    def __fwhmgauss(wavelength: float):
        return 0.5


class WidenPart:
    def __init__(self,
                 name,
                 init_data,
                 exp_data: ExpData,
                 delta_lambda=0.0,  # 单位是nm
                 n=None, ):
        self.name = name
        self.init_data = init_data.copy()
        self.exp_data = exp_data
        self.delta_lambda: float = delta_lambda
        self.n = n
        self.only_p = None

        self.plot_path_list = {}

        self.widen_data: Optional[pd.DataFrame] = None
        self.grouped_widen_data: Optional[Dict[str, pd.DataFrame]] = None

    def widen_by_group(self, temperature=25.6):
        """
        返回一个字典，包含了按跃迁正例分组后的展宽数据，例如
        {'1-2': pd.DataFrame, '1-3': pd.DataFrame, ...}
        pd.DataFrame的列标题为：wavelength, gaussian, cross-NP, cross-P
        Args:
            temperature: 展宽时的温度

        Returns:

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
            self.plot_path_list[key] = (PROJECT_PATH / f'figure/part/{self.name}_{key}.html').as_posix()
        self.grouped_widen_data = temp_data

    def __widen(self, temperature: float, temp_data: pd.DataFrame, only_p=True):
        """
            列标题依次为：energy_l, energy_h, wavelength_ev, intensity, index_l, index_h, J_l, J_h
            分别代表：下态能量，上态能量，波长，强度，下态序号，上态序号，下态J值，上态J值
        Args:
            temp_data:
            only_p: 只计算含有布局的
            temperature (float): 等离子体温度
        Returns:
            返回一个DataFrame，包含了展宽后的数据
            列标题为：wavelength, gaussian, cross-NP, cross-P
        """
        self.only_p = only_p

        data = temp_data.copy()
        fwhmgauss = self.__fwhmgauss
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
        new_data = new_data[(new_data['wavelength_ev'] > min_wavelength_ev) &
                            (new_data['wavelength_ev'] < max_wavelength_ev)]
        if new_data.empty:
            result = pd.DataFrame()
            result['wavelength'] = self.exp_data.data['wavelength'].values
            result['gauss'] = np.zeros(self.exp_data.data['wavelength'].values.shape)
            result['cross_NP'] = np.zeros(self.exp_data.data['wavelength'].values.shape)
            result['cross_P'] = np.zeros(self.exp_data.data['wavelength'].values.shape)
            return result
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
        population = (2 * new_J + 1) * np.exp(-abs(new_energy - min_energy) * 0.124 / temperature) / (2 * min_J + 1)
        if self.n is None:
            wave = 1239.85 / self.exp_data.data['wavelength'].values
        else:
            wave = np.linspace(min_wavelength_ev, max_wavelength_ev, self.n)
        result = pd.DataFrame()
        result['wavelength'] = 1239.85 / wave

        res = [self.__complex_cal(val, new_intensity, fwhmgauss(val), new_wavelength, population, new_J)
               for val in wave]
        res = list(zip(*res))
        if not self.only_p:
            result['gauss'] = res[0]
            result['cross_NP'] = res[1]
        result['cross_P'] = res[2]
        return result

    def plot_widen_by_group(self):
        for key, value in self.grouped_widen_data.items():
            self.__plot_html(value, self.plot_path_list[key], 'wavelength', 'cross_P')

    def __plot_html(self, data, path, x_name, y_name):
        trace1 = go.Scatter(x=data[x_name], y=data[y_name], mode='lines')
        data = [trace1]
        layout = go.Layout(margin=go.layout.Margin(autoexpand=False, b=15, l=30, r=0, t=0),
                           xaxis=go.layout.XAxis(range=self.exp_data.x_range),
                           )
        # yaxis=go.layout.YAxis(range=[self.min_strength, self.max_strength]))
        fig = go.Figure(data=data, layout=layout)
        plot(fig, filename=path, auto_open=False)

    def __complex_cal(self,
                      wave: float,
                      new_intensity: np.array,
                      fwhmgauss: float,
                      new_wavelength: np.array,
                      population: np.array,
                      new_J: np.array):
        uu = (new_intensity * population / (2 * new_J + 1)) * 2 * fwhmgauss / (
                2 * np.pi * ((new_wavelength - wave) ** 2 + np.power(2 * fwhmgauss, 2) / 4))
        if self.only_p:
            return -1, -1, uu.sum()
        else:
            tt = new_intensity / np.sqrt(2 * np.pi) / fwhmgauss * 2.355 * np.exp(
                -2.355 ** 2 * (new_wavelength - wave) ** 2 / fwhmgauss ** 2 / 2)
            ss = (new_intensity / (2 * new_J + 1)) * 2 * fwhmgauss / (
                    2 * np.pi * ((new_wavelength - wave) ** 2 + np.power(2 * fwhmgauss, 2) / 4))
            return tt.sum(), ss.sum(), uu.sum()

    @staticmethod
    def __fwhmgauss(wavelength: float):
        return 0.5


class SimulateSpectral:
    def __init__(self):
        self.cowan_list: List[Cowan] = []
        self.add_or_not: List[bool] = []
        self.exp_data: Optional[ExpData] = None
        self.spectrum_similarity = None
        self.temperature = None
        self.electron_density = None

        self.abundance = []
        self.sim_data = None

        self.plot_path = PROJECT_PATH.joinpath('figure/add.html').as_posix()
        self.example_path = PROJECT_PATH.joinpath('figure/part/example.html').as_posix()

    def load_exp_data(self, path: Path):
        self.exp_data = ExpData(path)

    def add_cowan(self, *args):
        for cowan in args:
            self.cowan_list.append(copy.deepcopy(cowan))
            self.add_or_not.append(True)

    def del_cowan(self, index):
        self.cowan_list.pop(index)
        self.add_or_not.pop(index)

    def get_simulate_data(self, temperature, electron_density):
        """
        获取模拟光谱
        Args:
            temperature:
            electron_density:

        Returns:

        """
        self.temperature = temperature
        self.electron_density = electron_density
        self.__update_abundance(temperature, electron_density)
        for cowan, flag in zip(self.cowan_list, self.add_or_not):
            if flag:
                cowan.cal_data.widen_all.widen(temperature)
        res = pd.DataFrame()
        res['wavelength'] = self.cowan_list[0].cal_data.widen_all.widen_data['wavelength']
        temp = np.zeros(res.shape[0])
        for cowan, abu, flag in zip(self.cowan_list, self.abundance, self.add_or_not):
            if flag:
                temp += cowan.cal_data.widen_all.widen_data['cross_P'].values * abu
        res['intensity'] = temp
        self.sim_data = res
        self.get_spectrum_similarity()
        return copy.deepcopy(self)

    def plot_html(self):
        x1 = self.exp_data.data['wavelength']
        y1 = self.exp_data.data['intensity'] / self.exp_data.data['intensity'].max() + 0.5
        x2 = self.sim_data['wavelength']
        y2 = self.sim_data['intensity'] / self.sim_data['intensity'].max()
        trace1 = go.Scatter(x=x1, y=y1, mode='lines')
        trace2 = go.Scatter(x=x2, y=y2, mode='lines')
        data = [trace1, trace2]
        layout = go.Layout(margin=go.layout.Margin(autoexpand=False, b=15, l=30, r=0, t=0),
                           xaxis=go.layout.XAxis(range=self.exp_data.x_range),
                           )
        # yaxis=go.layout.YAxis(range=[self.min_strength, self.max_strength]))
        fig = go.Figure(data=data, layout=layout)
        plot(fig, filename=self.plot_path, auto_open=False)

    def plot_example_html(self, add_list):
        # for c in self.cowan_list:
        #     c.cal_data.widen_part.widen_by_group()
        height = 0
        trace = []
        for i, c in enumerate(self.cowan_list):
            if add_list[i][0]:
                for j, (key, value) in enumerate(c.cal_data.widen_part.grouped_widen_data.items()):
                    if add_list[i][1][j]:
                        if value['cross_P'].max() == 0:
                            trace.append(
                                go.Scatter(x=value['wavelength'],
                                           y=value['cross_P'] + height,
                                           mode='lines',
                                           name=f'{c.name}_{key}'))
                        else:
                            trace.append(
                                go.Scatter(x=value['wavelength'],
                                           y=value['cross_P'] / value['cross_P'].max() + height,
                                           mode='lines',
                                           name=f'{c.name}_{key}'))
                        height += 1.2
        layout = go.Layout(margin=go.layout.Margin(autoexpand=False, b=15, l=30, r=0, t=0),
                           xaxis=go.layout.XAxis(range=self.exp_data.x_range),
                           )
        # yaxis=go.layout.YAxis(range=[self.min_strength, self.max_strength]))
        fig = go.Figure(data=trace, layout=layout)
        plot(fig, filename=self.example_path, auto_open=False)

    # 计算离子丰度
    def __update_abundance(self, temperature, electron_density):
        """
            将所需要的离子丰度挑选出来
        Args:
            temperature:
            electron_density:

        Returns:

        """
        all_abundance = self.__cal_abundance2(temperature, electron_density)
        temp_abundance = []
        for c in self.cowan_list:
            ion = int(c.name.split('_')[1]) - 1
            temp_abundance.append(all_abundance[ion])
        self.abundance = temp_abundance

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
        ion_energy = np.array(IONIZATION_ENERGY[atomic_num][1:])
        electron_num = np.array([self.__get_outermost_num(i) for i in range(1, atomic_num)])

        S = (9 * 1e-6 * electron_num * np.sqrt(temperature / ion_energy) * np.exp(-ion_energy / temperature)) / (
                ion_energy ** 1.5 * (4.88 + temperature / ion_energy))
        Ar = 5.2 * 1e-14 * np.sqrt(ion_energy / temperature) * ion_num * (
                0.429 + 0.5 * np.log(ion_energy / temperature) + 0.469 * np.sqrt(temperature / ion_energy))
        A3r = 2.97 * 1e-27 * electron_num / (temperature * ion_energy ** 2 * (4.88 + temperature / ion_energy))

        ratio = S / (Ar + electron_density * A3r)
        abundance = self.__calculate_a_over_S(ratio)
        return abundance

    def __cal_abundance2(self, temperature, electron_density):
        """
        使用fortran程序中的方法计算离子丰度
        Args:
            temperature:
            electron_density:

        Returns:

        """
        atomic_num = self.cowan_list[0].in36.atom.num
        ion_num = np.array([i for i in range(atomic_num)])
        ion_energy = np.array(IONIZATION_ENERGY[atomic_num])
        electron_num = np.array([self.__get_outermost_num(i) for i in range(atomic_num)])

        S = (9 * 1e-6 * electron_num * np.sqrt(temperature / ion_energy) * np.exp(-ion_energy / temperature)) / (
                ion_energy ** 1.5 * (4.88 + temperature / ion_energy))
        Ar = 5.2 * 1e-14 * np.sqrt(ion_energy / temperature) * ion_num * (
                0.429 + 0.5 * np.log(ion_energy / temperature) + 0.469 * np.sqrt(temperature / ion_energy))
        A3r = 2.97 * 1e-27 * electron_num / (temperature * ion_energy ** 2 * (4.88 + temperature / ion_energy))

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

    # 计算光谱相似度
    def get_spectrum_similarity(self):

        self.spectrum_similarity = self.spectrum_similarity5(self.exp_data.data[['wavelength', 'intensity']],
                                                             self.sim_data[['wavelength', 'intensity']])

    @staticmethod
    def spectrum_similarity1(fax: pd.DataFrame, fbx: pd.DataFrame):
        """
        计算两个光谱的相似度
        遍历实验光谱的每个点，找到模拟光谱中最近的点，计算距离，并求和
        Args:
            fax: 实验光谱
            fbx: 模拟光谱

        Returns:

        """
        col_names_a = fax.columns
        col_names_b = fbx.columns
        x1 = fax[col_names_a[0]].values
        y1 = fax[col_names_a[1]].values
        x2 = fbx[col_names_b[0]].values
        y2 = fbx[col_names_b[1]].values
        y1 = y1 / y1.max()
        y2 = y2 / y2.max()

        res = 0
        for i in range(fax.shape[0]):
            res += min(np.sqrt((x1[i] - x2) ** 2 + (y1[i] - y2) ** 2))
        return res / fax.shape[0]

    def spectrum_similarity2(self, fax: pd.DataFrame, fbx: pd.DataFrame):
        """
        计算两个光谱的相似度，根据R2进行判断
        Args:
            fax: 实验光谱
            fbx: 模拟光谱

        Returns:

        """
        x, y1, y2 = self.get_y1y2(fax, fbx)

        # y2是测量值，y1是预测值
        SS_reg = np.power(y1 - y2.mean(), 2).sum()
        SS_tot = np.power(y2 - y2.mean(), 2).sum()
        R2 = SS_reg / SS_tot
        if R2 > 1:
            return 1 / R2
        else:
            return R2

    def spectrum_similarity3(self, fax: pd.DataFrame, fbx: pd.DataFrame):
        x, y1, y2 = self.get_y1y2(fax, fbx)

        distance, path = fastdtw(y1, y2)
        return distance

    def spectrum_similarity4(self, fax: pd.DataFrame, fbx: pd.DataFrame):
        x, y1, y2 = self.get_y1y2(fax, fbx)
        corr = np.corrcoef(y1, y2)[0, 1]
        return corr + 1

    def spectrum_similarity5(self, fax: pd.DataFrame, fbx: pd.DataFrame):
        """
        峰值匹配法
        :param fax:
        :param fbx:
        :return:
        """
        x, y1, y2 = self.get_y1y2(fax, fbx)
        # 找出两个光谱数据的峰值位置
        peaks1, _ = find_peaks(y1, height=0.1)
        peaks2, _ = find_peaks(y2, height=0.1)
        # 计算两个光谱数据峰值位置的相似性
        match = np.intersect1d(peaks1, peaks2)
        similarity = len(match) / min(len(peaks1), len(peaks2))
        return similarity

    def spectrum_similarity6(self, fax: pd.DataFrame, fbx: pd.DataFrame):
        x, y1, y2 = self.get_y1y2(fax, fbx)
        n = len(y1)
        rho = (n * (y1 * y2).sum() - y1.sum() * y2.sum()) / \
              (np.sqrt((n * (y1 ** 2).sum() - (y1.sum()) ** 2) * (n * (y2 ** 2).sum() - (y2.sum()) ** 2)))
        return rho

    def spectrum_similarity7(self, fax: pd.DataFrame, fbx: pd.DataFrame):
        x, y1, y2 = self.get_y1y2(fax, fbx)
        return scipy.stats.pearsonr(y1, y2)[0]

    def spectrum_similarity8(self, fax: pd.DataFrame, fbx: pd.DataFrame):
        x, y1, y2 = self.get_y1y2(fax, fbx)
        return np.sqrt(sum(pow(a - b, 2) for a, b in zip(y1, y2)))

    def spectrum_similarity9(self, fax: pd.DataFrame, fbx: pd.DataFrame):
        x, y1, y2 = self.get_y1y2(fax, fbx)
        tmp = np.sum(y1 * y2)
        non = np.linalg.norm(x) * np.linalg.norm(y2)
        return np.round(tmp / float(non), 9)

    @staticmethod
    def get_y1y2(fax: pd.DataFrame, fbx: pd.DataFrame, min_x=None, max_x=None):
        col_names_a = fax.columns
        col_names_b = fbx.columns
        if (min_x is None) and (max_x is None):
            min_x = max(fax[col_names_a[0]].min(), fbx[col_names_b[0]].min())
            max_x = min(fax[col_names_a[0]].max(), fbx[col_names_b[0]].max())
        fax_new = fax[(fax[col_names_a[0]] <= max_x) & (min_x <= fax[col_names_a[0]])]
        fbx_new = fbx[(fbx[col_names_b[0]] <= max_x) & (min_x <= fbx[col_names_b[0]])]
        f2 = interp1d(fbx_new[col_names_b[0]], fbx_new[col_names_b[1]], fill_value="extrapolate")
        x = fax_new[col_names_a[0]].values
        y1 = fax_new[col_names_a[1]].values
        y2 = f2(x)
        y1 = y1 / max(y1)
        y2 = y2 / max(y2)
        return x, y1, y2


class SimulateGrid(QtCore.QThread):
    progress = Signal(str)  # 计数完成后发送一次信号
    end = Signal(str)  # 计数完成后发送一次信号

    def __init__(self, temperature, density, simulate):
        super().__init__()
        self.simulate = copy.deepcopy(simulate)
        self.t_num: int = int(temperature[-1])
        self.ne_num: int = int(density[-1])
        t_list = np.linspace(temperature[0], temperature[1], self.t_num)
        ne_list = np.power(10, np.linspace(
            np.log10(density[0] * 10 ** density[1]),
            np.log10(density[2] * 10 ** density[3]), self.ne_num))
        self.t_list = ['{:.3f}'.format(v) for v in t_list]
        self.ne_list = ['{:.3e}'.format(v) for v in ne_list]

        self.grid_data = {}

    def run(self):
        def callback(t, ne, f):
            nonlocal current_progress
            current_progress += 1
            self.grid_data[(t, ne)] = f.result()
            self.progress.emit(str(current_progress))

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


class SpaceTimeResolution:
    def __init__(self):
        # 模拟光谱数据对象 列表
        self.simulate_spectral_dict = {}

    # 添加一个位置时间
    def add_st(self, location: tuple, simulate_spectral):
        self.simulate_spectral_dict[location] = copy.deepcopy(simulate_spectral)

    # 删除一个位置时间
    def del_st(self, location):
        self.simulate_spectral_dict.pop(location)

    def run(self):
        pass

# if __name__ == '__main__':
#     in36_3 = In36()
#     in36_3.read_from_file(PROJECT_PATH / 'in36_3')
#     in36_4 = In36()
#     in36_4.read_from_file(PROJECT_PATH / 'in36_4')
#     in36_5 = In36()
#     in36_5.read_from_file(PROJECT_PATH / 'in36_5')
#     in36_6 = In36()
#     in36_6.atom = Atom(13, 6)
#     in36_6.add_configuration(in36_6.atom.get_configuration())
#     arouse = ['3s', '3d', '4s', '4d', '5d']
#     for v in arouse:
#         in36_6.atom.arouse_electron('2p', v)
#         in36_6.add_configuration(in36_6.atom.get_configuration())
#         in36_6.atom.revert_to_ground_state()
#     in36_6.control_card = in36_5.control_card.copy()
#
#     in2 = In2()
#     in2.read_from_file(PROJECT_PATH / 'in2')
#
#     exp_data = ExpData(PROJECT_PATH / 'exp_data.csv')
#
#     cowan_3 = Cowan(in36_3, in2, 'Al_3', exp_data)
#     cowan_4 = Cowan(in36_4, in2, 'Al_4', exp_data)
#     cowan_5 = Cowan(in36_5, in2, 'Al_5', exp_data)
#     cowan_6 = Cowan(in36_6, in2, 'Al_6', exp_data)
#
#     sim = SimulateSpectral()
#     sim.add_cowan(cowan_3, cowan_4, cowan_5, cowan_6)
#     for c in sim.cowan_list:
#         c.run()
#         c.cal_data.widen_all.widen(23.5)
#     sim.get_simulate_data(23.5, 1e20)
#     sim.load_exp_data(Path('f:/Cowan/Al/exp_data.csv'))
#     plt.plot(sim.exp_data.data['wavelength'], sim.exp_data.data['intensity'] / sim.exp_data.data['intensity'].max())
#     plt.plot(sim.sim_data['wavelength'], sim.sim_data['intensity'] / sim.sim_data['intensity'].max())
#     # plt.show()
