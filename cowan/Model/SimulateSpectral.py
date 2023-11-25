import copy
import warnings
from pathlib import Path
from typing import List, Optional

import numpy as np
import pandas as pd
import plotly.graph_objs as go
from plotly.offline import plot
from scipy.interpolate import interp1d
from scipy.signal import find_peaks

from .AtomInfo import IONIZATION_ENERGY, BASE_CONFIGURATION, OLD_IONIZATION_ENERGY, OUTER_ELECTRON_NUM
from .CowanList import CowanList
from .Cowan_ import Cowan
from .ExpData import ExpData
from .GlobalVar import PROJECT_PATH


class SimulateSpectral:
    def __init__(self):
        """
        模拟光谱对象，储存于 SpaceTimeResolution 对象中

        """
        self.cowan_list: Optional[List[Cowan]] = None  # 用于存储 cowan 对象
        self.add_or_not: Optional[List[bool]] = None  # cowan 对象是否被添加
        # self.offset_list: Optional[List[float]] = None  # cowan 对象的偏移量
        self.exp_data: Optional[ExpData] = None  # 实验光谱数据
        self.spectrum_similarity = None  # 光谱相似度
        self.temperature = None  # 模拟的等离子体温度
        self.electron_density = None  # 模拟的等离子体电子密度

        self.characteristic_peaks = []  # 特征峰波长
        self.peaks_index = []  # 特征峰索引

        self.abundance = []  # 离子丰度
        self.sim_data = None  # 模拟光谱数据

        self.plot_path = PROJECT_PATH().joinpath('figure/add.html').as_posix()
        self.example_path = (PROJECT_PATH().joinpath('figure/part/example.html').as_posix())

    def load_exp_data(self, path: Path):
        """
        读取实验光谱数据

        Args:
            path: 实验光谱数据的路径

        """
        self.exp_data = ExpData(path)

    def set_xrange(self, x_range, num, cowan_lists: CowanList):
        self.exp_data.set_xrange(x_range)
        self.init_cowan_list(cowan_lists)
        for cowan in self.cowan_list:
            cowan.set_xrange(x_range, num)
        if self.temperature is not None and self.electron_density is not None:
            self.cal_simulate_data(self.temperature, self.electron_density)
        self.del_cowan_list()

    def reset_xrange(self, cowan_lists: CowanList):
        self.exp_data.reset_xrange()
        self.init_cowan_list(cowan_lists)
        for cowan in self.cowan_list:
            cowan.reset_xrange()
        if self.temperature is not None and self.electron_density is not None:
            self.cal_simulate_data(self.temperature, self.electron_density)
        self.del_cowan_list()

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
        self.add_or_not = cowan_lists.add_or_not

    def del_cowan_list(self):
        """
        删除 cowan_list，节省内存

        """
        self.cowan_list = None
        self.add_or_not = None

    def cal_simulate_data(self, temperature, electron_density):
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
                cowan.cal_data.set_temperature(temperature)
                cowan.cal_data.widen_all.widen()
        res = pd.DataFrame()
        res['wavelength'] = self.cowan_list[0].cal_data.widen_all.widen_data['wavelength']
        temp = np.zeros(res.shape[0])
        for cowan, abu, flag in zip(self.cowan_list, self.abundance, self.add_or_not):
            if flag:
                temp += cowan.cal_data.widen_all.widen_data['cross_P'].values * abu
        res['intensity'] = temp
        if res['intensity'].max() == 0.0:
            res['intensity_normalization'] = copy.deepcopy(res['intensity'])
        else:
            res['intensity_normalization'] = res['intensity'] / res['intensity'].max()

        self.sim_data = res
        self.cal_spectrum_similarity()
        return copy.deepcopy(self)

    def export_plot_data(self, filepath:Path):
        temp_data = pd.DataFrame()
        temp_data['exp_wavelength'] = self.exp_data.data['wavelength']
        temp_data['exp_intensity_normalization'] = self.exp_data.data['intensity_normalization']
        temp_data['cal_wavelength'] = self.sim_data['wavelength']
        temp_data['cal_intensity_normalization'] = self.sim_data['intensity_normalization']
        temp_data.to_csv(filepath, sep=',', index=False)

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
        return self.__cal_abundance(t, e)

    def __cal_abundance(self, temperature, electron_density) -> np.array:
        """
        计算各种离子的丰度

        Args:
            temperature: 等离子体温度，单位是ev
            electron_density: 等离子体粒子数密度

        Returns:
            返回一个列表，类型为np.ndarray，每个元素为对应离子的丰度
            例如：[0 1 2 3 4 5 6 7 8]
            分别代表 一次离化，二次离化，三次离化，四次离化，五次离化，六次离化，七次离化，八次离化 九次离化 的粒子数密度
        """
        atom_nums = self.cowan_list[0].in36.atom.num
        ion_num = np.array([k for k in range(atom_nums)])
        ion_energy = np.array([OLD_IONIZATION_ENERGY[atom_nums][k] for k in range(atom_nums)])
        electron_num = np.array([OUTER_ELECTRON_NUM[atom_nums][k] for k in range(atom_nums)])

        S = (9 * 1e-6 * electron_num * np.sqrt(temperature / ion_energy) * np.exp(-ion_energy / temperature)) / (
                ion_energy ** 1.5 * (4.88 + temperature / ion_energy))
        Ar = (5.2 * 1e-14 * np.sqrt(ion_energy / temperature) * ion_num * (
                0.429 + 0.5 * np.log(ion_energy / temperature) + 0.469 * np.sqrt(temperature / ion_energy)))
        A3r = (2.97 * 1e-27 * electron_num / (temperature * ion_energy ** 2 * (4.88 + temperature / ion_energy)))
        ratio = S / (Ar + electron_density * A3r)
        abundance = self.__calculate_a_over_S(ratio)
        return abundance

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

    def cal_spectrum_similarity(self):
        """
        获取光谱相似度，直接存储在 self.spectrum_similarity 中

        """
        if self.exp_data.data.shape[0] == 0:
            warnings.warn('实验光谱数据在此波段内为空，无法计算光谱相似度')
            return
        if self.exp_data.data['wavelength'].max() < self.sim_data['wavelength'].min() and \
                self.sim_data['wavelength'].max() < self.exp_data.data['wavelength'].min():
            warnings.warn('实验波长与模拟波长不匹配！！！')
            return

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
        if len(peaks2) < 5:
            warnings.warn('计算得到的峰值个数 < 5, 相似度返回 -1')
            return -1
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
        if max(y1) != 0.0:
            y1 = y1 / max(y1)
        if max(y2) != 0.0:
            y2 = y2 / max(y2)
        return x, y1, y2

    def get_temperature_and_density(self) -> tuple:
        return self.temperature, self.electron_density

    def get_exp_data(self) -> pd.DataFrame:
        return self.exp_data.data

    def get_sim_data(self) -> pd.DataFrame:
        return self.sim_data

    def load_class(self, class_info):
        if class_info.cowan_list is None:
            self.cowan_list = None
        else:
            for i in range(len(self.cowan_list)):
                self.cowan_list[i].load_class(class_info.cowan_list[i])
        self.add_or_not = class_info.add_or_not
        if class_info.exp_data is None:
            self.exp_data = None
        else:
            self.exp_data.load_class(class_info.exp_data)
        self.spectrum_similarity = class_info.spectrum_similarity
        self.temperature = class_info.temperature
        self.electron_density = class_info.electron_density

        self.characteristic_peaks = class_info.characteristic_peaks
        self.peaks_index = class_info.peaks_index

        self.abundance = class_info.abundance
        self.sim_data = class_info.sim_data

        self.plot_path = PROJECT_PATH().joinpath('figure/add.html').as_posix()
        self.example_path = (PROJECT_PATH().joinpath('figure/part/example.html').as_posix())