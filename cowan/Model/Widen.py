from typing import Optional, Dict

import numpy as np
import pandas as pd
import plotly.graph_objs as go
from plotly.offline import plot

from .GlobalVar import PROJECT_PATH
from .ExpData import ExpData


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
        self.temperature: float = 25.6

        self.plot_path_gauss = (PROJECT_PATH() / f'figure/gauss/{self.name}.html').as_posix()
        self.plot_path_cross_NP = (PROJECT_PATH() / f'figure/cross_NP/{self.name}.html').as_posix()
        self.plot_path_cross_P = (PROJECT_PATH() / f'figure/cross_P/{self.name}.html').as_posix()

        self.widen_data: pd.DataFrame | None = None

    def widen(self, only_p=True):
        """
        展宽

        列标题依次为：energy_l, energy_h, wavelength_ev, intensity, index_l, index_h, J_l, J_h
        分别代表：下态能量，上态能量，波长，强度，下态序号，上态序号，下态J值，上态J值

        Args:
            only_p: 只计算包含能级布局的数据
        Returns:
            返回一个DataFrame，包含了展宽后的数据
            列标题为：wavelength, gaussian, cross-NP, cross-P
            如果only_p为True，则没有cross-NP列和gaussian列
        """
        print('{} widen start! [temperate: {}eV] [delta_lambda: {}nm] [fwhm: {}nm] [range: {} - {}]'.format(
            self.name, self.temperature, self.delta_lambda, self.fwhm_value,
            self.exp_data.x_range[0], self.exp_data.x_range[1]))
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
            print('    use exp wavelength')
        else:
            wave = 1239.85 / np.linspace(min_wavelength_nm, max_wavelength_nm, self.n)
            print('    use new wavelength')
        result = pd.DataFrame()
        result['wavelength'] = 1239.85 / wave

        if new_data.empty:
            result['gauss'] = 0
            result['cross_NP'] = 0
            result['cross_P'] = 0
            self.widen_data = result
            print(f'{self.name} widen completed! [return None]')
            return -1
        new_data = new_data.reindex()
        # 获取展宽所需要的数据
        new_wavelength = abs(1239.85 / (1239.85 / new_data['wavelength_ev'] + self.delta_lambda))  # 单位时ev
        new_wavelength = new_wavelength.values
        new_intensity = abs(new_data['intensity'])
        new_intensity = new_intensity.values
        # 挑选上能级
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
        population = ((2 * new_J + 1) * np.exp(-abs(new_energy - min_energy) * 0.124 / self.temperature) / (
                2 * min_J + 1))
        print('    population completed!')

        res = [self.__complex_cal(val, new_intensity, fwhmgauss(val), new_wavelength, population, new_J) for val in
               wave]
        print('    res cal completed!')
        res = list(zip(*res))
        if not self.only_p:
            result['gauss'] = res[0]
            result['cross_NP'] = res[1]
        result['cross_P'] = res[2]
        self.widen_data = result
        print(f'{self.name} widen completed!')

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

    def load_class(self, class_info):
        self.name = class_info.name
        self.init_data = class_info.init_data
        self.exp_data.load_class(class_info.exp_data)
        self.n = class_info.n
        self.only_p = class_info.only_p
        self.delta_lambda = class_info.delta_lambda
        self.fwhm_value = class_info.fwhm_value
        # start [无版本号 > 1.0.0]
        if 'temperature' in class_info.__dict__.keys():
            self.temperature = class_info.temperature
        else:
            self.temperature = 25.6
        # end [无版本号 > 1.0.0]
        self.plot_path_gauss = (PROJECT_PATH() / f'figure/gauss/{self.name}.html').as_posix()
        self.plot_path_cross_NP = (PROJECT_PATH() / f'figure/cross_NP/{self.name}.html').as_posix()
        self.plot_path_cross_P = (PROJECT_PATH() / f'figure/cross_P/{self.name}.html').as_posix()
        self.widen_data = class_info.widen_data


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
        self.temperature = 25.6

        self.plot_path_list = {}

        # self.widen_data: Optional[pd.DataFrame] = None
        self.grouped_widen_data: Optional[Dict[str, pd.DataFrame]] = None

    def widen_by_group(self):
        """
        按组态进行展宽

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
            temp_result = self.__widen(self.temperature, temp_group)
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

    def load_class(self, class_info):
        self.name = class_info.name
        self.init_data = class_info.init_data
        self.exp_data.load_class(class_info.exp_data)
        self.n = class_info.n
        self.only_p = class_info.only_p
        self.delta_lambda = class_info.delta_lambda
        self.fwhm_value = class_info.fwhm_value
        # start [无版本号 > 1.0.0]
        if 'temperature' in class_info.__dict__.keys():
            self.temperature = class_info.temperature
        else:
            self.temperature = 25.6
        # end [无版本号 > 1.0.0]
        self.plot_path_list = {}
        for key in class_info.plot_path_list.keys():
            self.plot_path_list[key] = (
                    PROJECT_PATH() / f'figure/part/{self.name}_{key}.html'
            ).as_posix()
        self.grouped_widen_data = class_info.grouped_widen_data
