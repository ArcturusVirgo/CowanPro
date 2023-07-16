import os
import shutil
import subprocess
from pathlib import Path
from pprint import pprint
from typing import Optional, List, Dict, Tuple, Union

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from fastdtw import fastdtw
from matplotlib import pyplot as plt
from plotly.offline import plot

from cowan.atom import *
from cowan.constant import *


class SpaceTimeResolution:
    def __init__(self):
        # 实验数据对象 列表
        self.exp_data_list: List[ExpData] = []
        # 模拟光谱数据对象 列表
        self.simulate_spectral_list: List[SimulateSpectral] = []
        # 对应关系
        self.location_to_index: Dict[Tuple[str]: int] = {}

    # 添加一个位置时间
    def add_location(self, location, exp_data, simulate_spectral):
        # 如果已经存在这个位置的值，就先将这个位置的值删除
        if location in self.location_to_index.keys():
            self.del_location(location)
        # 开始添加
        self.location_to_index[location] = len(self.exp_data_list) - 1
        self.exp_data_list.append(exp_data)
        self.simulate_spectral_list.append(simulate_spectral)

    # 删除一个位置时间
    def del_location(self, location):
        self.exp_data_list.pop(self.location_to_index[location])
        self.simulate_spectral_list.pop(self.location_to_index[location])
        self.location_to_index.pop(location)


class SimulateSpectral:
    def __init__(self):
        self.cowan_list: List[Cowan] = []
        self.exp_data: Optional[ExpData] = None

        self.abundance = []
        self.sim_data = None

    def load_exp_data(self, path: Path):
        self.exp_data = ExpData(path)

    def add_cowan(self, *args):
        self.cowan_list += args

    def del_cowan(self, index):
        self.cowan_list.pop(index)

    def get_simulate_data(self, temperature, electron_density):
        """
        获取模拟光谱
        Args:
            temperature:
            electron_density:

        Returns:

        """
        self.__update_abundance(temperature, electron_density)
        for cowan in self.cowan_list:
            cowan.cal_data.widen_all.widen(temperature)
        res = pd.DataFrame()
        res['wavelength'] = self.cowan_list[0].cal_data.widen_all.widen_data['wavelength']
        temp = np.zeros(res.shape[0])
        for cowan, abu in zip(self.cowan_list, self.abundance):
            temp += cowan.cal_data.widen_all.widen_data['cross_P'].values * abu
        res['intensity'] = temp
        self.sim_data = res

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


class Cowan:
    def __init__(self, in36, in2, name, exp_data, coupling_mode=1):
        self.in36: In36 = in36
        self.in2: In2 = in2
        self.name = name
        self.exp_data = exp_data
        self.coupling_mode = coupling_mode  # 1是L-S耦合 2是j-j耦合

        self.cal_data: Optional[CalData] = None
        self.run_path = PROJECT_PATH / f'cal_result/{self.name}'

    def run(self):
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


class In36:
    def __init__(self):
        self.atom: Optional[Atom] = None

        self.control_card = []
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
            temp_list = list(zip(*self.configuration_card))[-1]
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
        self.input_card: List[str] = []

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


class CalData:
    def __init__(self, name, exp_data: ExpData):
        self.name = name
        self.exp_data = exp_data
        self.x_range = exp_data.x_range
        self.filepath = (PROJECT_PATH / f'cal_result/{name}/spectra.dat').as_posix()
        self.plot_path = (PROJECT_PATH / f'figure/line/{name}.html').as_posix()
        self.init_data: pd.DataFrame | None = None

        self.widen_all: Optional[WidenAll] = None
        self.widen_part = None

        self.read_file()

    def read_file(self):
        self.init_data = pd.read_csv(self.filepath, sep='\s+',
                                     names=['energy_l', 'energy_h', 'wavelength_ev', 'intensity',
                                            'index_l', 'index_h', 'J_l', 'J_h'])
        self.widen_all = WidenAll(self.name, self.init_data, self.exp_data)

    def plot_html(self):
        temp_data = self.__get_line_data(self.init_data[['wavelength_ev', 'intensity']])
        trace1 = go.Scatter(x=temp_data['wavelength'], y=temp_data['intensity'], mode='lines')
        data = [trace1]
        layout = go.Layout(margin=go.layout.Margin(autoexpand=False, b=15, l=30, r=0, t=0),
                           xaxis=go.layout.XAxis(range=self.x_range),
                           )
        # yaxis=go.layout.YAxis(range=[self.min_strength, self.max_strength]))
        fig = go.Figure(data=data, layout=layout)
        plot(fig, filename=self.plot_path, auto_open=False)

    def __get_line_data(self, origin_data):
        temp_data = origin_data.copy()
        temp_data['wavelength'] = 1239.85 / temp_data['wavelength_ev']
        temp_data = temp_data[(temp_data['wavelength'] < self.x_range[1]) &
                              (temp_data['wavelength'] > self.x_range[0])]
        lambda_ = []
        strength = []
        if temp_data['wavelength'].min() > self.x_range[0]:
            lambda_ += [self.x_range[0]]
            strength += [0]
        for x, y in zip(temp_data['wavelength'], temp_data['intensity']):
            lambda_ += [x, x, x]
            strength += [0, y, 0]
        if temp_data['wavelength'].max() < self.x_range[1]:
            lambda_ += [self.x_range[1]]
            strength += [0]
        temp = pd.DataFrame({
            'wavelength': lambda_,
            'intensity': strength
        })
        return temp


class Atom:
    def __init__(self, num: int, ion: int):
        self.num = num  # 原子序数
        self.symbol = ATOM[self.num][0]  # 元素符号
        self.name = ATOM[self.num][1]  # 元素名称
        self.ion = ion  # 离化度
        self.electron_num = self.num - self.ion  # 实际的电子数量
        self.electron_arrangement = self.get_electron_arrangement()  # 电子排布情况
        self.base_configuration = ' '.join(self.get_configuration())  # 基组态

    def get_electron_arrangement(self):
        """
            根据当前现有电子数，获取电子基组态的核外排布情况

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
        temp_electronic_num = self.electron_num
        for subshell in SUBSHELL_SEQUENCE:
            max_electronic_num = 4 * ANGULAR_QUANTUM_NUM_NAME.index(subshell[1]) + 2  # 子壳层的最大电子数
            if temp_electronic_num > max_electronic_num:
                electron_arrangement[subshell] = max_electronic_num
                temp_electronic_num -= max_electronic_num
            else:
                electron_arrangement[subshell] = temp_electronic_num
                break
        return electron_arrangement

    def revert_to_ground_state(self):
        """
            将电子排布状态重置为基态基态
        """
        self.electron_num = self.num - self.ion
        self.electron_arrangement = self.get_electron_arrangement()

    def get_configuration(self) -> str:
        """
            根据当前的电子排布情况，获取当前的电子组态

        Returns:
            返回一个字符串
            例如 1. 基态：3s02 3p04
                2. 激发态： 3s02 3p03 4s01
        """
        configuration = {}  # 按照子壳层的顺序排列的电子组态
        flag = False  # 是否开始写入
        for i, subshell_name in enumerate(SUBSHELL_NAME):
            if subshell_name in self.electron_arrangement.keys():
                l = ANGULAR_QUANTUM_NUM_NAME.index(subshell_name[1])
                if self.electron_arrangement[subshell_name] != 4 * l + 2 and not flag:  # 如果不是满子壳层
                    if i != 0:
                        configuration[SUBSHELL_NAME[i - 1]] = self.electron_arrangement[SUBSHELL_NAME[i - 1]]
                    flag = True
                if flag:
                    configuration[subshell_name] = self.electron_arrangement[subshell_name]
        if not flag:
            last_subshell_name = list(self.electron_arrangement.keys())[-1]
            for i, subshell_name in enumerate(SUBSHELL_NAME):
                if subshell_name in self.electron_arrangement.keys():
                    if last_subshell_name == subshell_name:
                        if i != 0:
                            configuration[SUBSHELL_NAME[i - 1]] = self.electron_arrangement[SUBSHELL_NAME[i - 1]]
                        flag = True
                    if flag:
                        configuration[subshell_name] = self.electron_arrangement[subshell_name]

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


class WidenAll:
    def __init__(self,
                 name,
                 init_data,
                 exp_data: ExpData,
                 delta_lambda=0.0,
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

        Args:
            data (pandas.DataFrame):
                pandas的DataFrame格式数据
                列标题依次为：energy_l, energy_h, wavelength_ev, intensity, index_l, index_h, J_l, J_h
                分别代表：下态能量，上态能量，波长，强度，下态序号，上态序号，下态J值，上态J值
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
            return -1
        new_data = new_data.reindex()
        # 获取展宽所需要的数据
        new_wavelength = abs(1239.85 / (1239.85 / new_data['wavelength_ev'] - self.delta_lambda))  # 单位时ev
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
    pass


if __name__ == '__main__':
    in36_3 = In36()
    in36_3.read_from_file(PROJECT_PATH / 'in36_3')
    in36_4 = In36()
    in36_4.read_from_file(PROJECT_PATH / 'in36_4')
    in36_5 = In36()
    in36_5.read_from_file(PROJECT_PATH / 'in36_5')
    in36_6 = In36()
    in36_6.atom = Atom(13, 6)
    in36_6.add_configuration(in36_6.atom.get_configuration())
    arouse = ['3s', '3d', '4s', '4d', '5d']
    for v in arouse:
        in36_6.atom.arouse_electron('2p', v)
        in36_6.add_configuration(in36_6.atom.get_configuration())
        in36_6.atom.revert_to_ground_state()
    in36_6.control_card = in36_5.control_card.copy()

    in2 = In2()
    in2.read_from_file(PROJECT_PATH / 'in2')

    exp_data = ExpData(PROJECT_PATH / 'exp_data.csv')

    cowan_3 = Cowan(in36_3, in2, 'Al_3', exp_data)
    cowan_4 = Cowan(in36_4, in2, 'Al_4', exp_data)
    cowan_5 = Cowan(in36_5, in2, 'Al_5', exp_data)
    cowan_6 = Cowan(in36_6, in2, 'Al_6', exp_data)

    sim = SimulateSpectral()
    sim.add_cowan(cowan_3, cowan_4, cowan_5, cowan_6)
    for c in sim.cowan_list:
        c.run()
        c.cal_data.widen_all.widen(23.5)
    sim.get_simulate_data(23.5, 1e20)
    sim.load_exp_data(Path('f:/Cowan/Al/exp_data.csv'))
    plt.plot(sim.exp_data.data['wavelength'], sim.exp_data.data['intensity'] / sim.exp_data.data['intensity'].max())
    plt.plot(sim.sim_data['wavelength'], sim.sim_data['intensity'] / sim.sim_data['intensity'].max())
    plt.show()
