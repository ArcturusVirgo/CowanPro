from typing import Optional

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot

from .GlobalVar import PROJECT_PATH
from .ExpData import ExpData
from .Widen import WidenAll, WidenPart


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
        self.plot_path = (PROJECT_PATH() / f'figure/line/{self.name}.html').as_posix()
        self.init_data: pd.DataFrame | None = None

        self.widen_all: Optional[WidenAll] = None  # 通过self.read_file()赋初值
        self.widen_part: Optional[WidenPart] = None  # 通过self.read_file()赋初值

        self.info_dict = {}

        self.read_file()

    def read_file(self):
        """
        读取Cowan程序计算的结果

        产生两个展宽对象：widen_all、widen_part

        """
        self.init_data = pd.read_fwf(
            (PROJECT_PATH() / f'cal_result/{self.name}/spectra.dat').as_posix(),
            widths=[9, 9, 9, 9, 3, 3, 5, 5],
            names=['energy_l', 'energy_h', 'wavelength_ev', 'intensity', 'index_l', 'index_h', 'J_l', 'J_h', ],
        )
        self.widen_all = WidenAll(self.name, self.init_data, self.exp_data)
        self.widen_part = WidenPart(self.name, self.init_data, self.exp_data)

    def plot_line(self):
        """
        绘制线状谱
        """

        def get_line_data(origin_data):
            """
            将计算结果转换为线状谱

            Args:
                origin_data: 读取进来的原始数据

            Returns:
                转化后的数据
            """
            temp_data_ = origin_data.copy()
            temp_data_['wavelength'] = 1239.85 / temp_data_['wavelength_ev']
            temp_data_ = temp_data_[
                (temp_data_['wavelength'] < self.exp_data.x_range[1])
                & (temp_data_['wavelength'] > self.exp_data.x_range[0])
                ]
            lambda_ = []
            strength = []
            if temp_data_['wavelength'].min() > self.exp_data.x_range[0]:
                lambda_ += [self.exp_data.x_range[0]]
                strength += [0]
            for x, y in zip(temp_data_['wavelength'], temp_data_['intensity']):
                lambda_ += [x, x, x]
                strength += [0, y, 0]
            if temp_data_['wavelength'].max() < self.exp_data.x_range[1]:
                lambda_ += [self.exp_data.x_range[1]]
                strength += [0]
            temp = pd.DataFrame({'wavelength': lambda_, 'intensity': strength})
            return temp

        temp_data = get_line_data(self.init_data[['wavelength_ev', 'intensity']])
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

    def set_delta_lambda(self, delta_lambda: float):
        """
        设置展宽时的波长偏移量

        Args:
            delta_lambda: 波长偏移量，单位为 nm
        """
        self.widen_all.set_delta_lambda(delta_lambda)
        self.widen_part.set_delta_lambda(delta_lambda)

    def set_fwhm(self, fwhm: float):
        """
        设置展宽时的半高宽

        Args:
            fwhm: 半高宽，单位为 nm
        """
        self.widen_all.set_fwhm(fwhm)
        self.widen_part.set_fwhm(fwhm)

    def set_temperature(self, temperature: float):
        """
        设置等离子体温度

        Args:
            temperature: 等离子体温度，单位为 eV
        """

        self.widen_all.set_temperature(temperature)
        self.widen_part.set_temperature(temperature)

    def set_cowan_info(self, delta_lambda, fwhm, temperature):
        """
        设置展宽时的参数

        Args:
            delta_lambda: 波长偏移量，单位为 nm
            fwhm: 半高宽，单位为 nm
            temperature: 等离子体温度，单位为 eV
        """
        self.set_delta_lambda(delta_lambda)
        self.set_fwhm(fwhm)
        self.set_temperature(temperature)

    def get_delta_lambda(self) -> float:
        """
        获取展宽时的波长偏移量

        Returns:
            波长偏移量，单位为 nm
        """
        return self.widen_all.delta_lambda

    def get_fwhm(self) -> float:
        """
        获取展宽时的半高宽

        Returns:
            半高宽，单位为 nm
        """
        return self.widen_all.fwhm_value

    def get_temperature(self) -> float:
        """
        获取等离子体温度

        Returns:
            等离子体温度，单位为 eV
        """
        return self.widen_all.temperature

    def get_cowan_info(self) -> (float, float, float):
        """
        获取展宽时的参数

        Returns:
            返回一个元组，包含了波长偏移量、半高宽、等离子体温度
            单位分别为 nm、eV、eV
            Examples: (0.01, 0.5, 25.6)
        """
        return self.get_delta_lambda(), self.get_fwhm(), self.get_temperature()

    def get_init_data(self) -> pd.DataFrame:
        return self.init_data.__deepcopy__()

    def get_average_wavelength(self) -> {str: [float, float]}:
        """
        获取平均波长
        原理见苏老师博士毕业论文 式 (5.1) (5.2)

        Returns:
            返回当前离化度的各个组态的平均波长，数据格式为字典
            键为组态序号（str），值为平均波长（float）
            Examples: {'1_2': [1.0, 2.0], '2_3': [2.0, 3.0]}
        """
        temp_data = {}
        new_data = self.init_data.__deepcopy__()
        # 挑选上能级
        flag = new_data['energy_l'] > new_data['energy_h']
        not_flag = np.bitwise_not(flag)
        temp_1 = new_data['energy_l'][flag]
        temp_2 = new_data['energy_h'][not_flag]
        new_energy = temp_1.combine_first(temp_2)
        new_energy = new_energy.values  # 上能级
        temp_1 = new_data['J_l'][flag]
        temp_2 = new_data['J_h'][not_flag]
        new_J = temp_1.combine_first(temp_2)
        new_J = new_J.values  # 上能及对应的J
        # 添加上能级数据
        new_data['energy'] = new_energy
        new_data['J'] = new_J

        # 按照跃迁正例分开
        data_grouped = new_data.groupby(by=['index_l', 'index_h'])
        for index in data_grouped.groups.keys():
            temp_group = pd.DataFrame(data_grouped.get_group(index))
            f_ij = temp_group['intensity'].values
            g_i = (2 * temp_group['J'].values) + 1
            E_ij = 1239.85 / temp_group['wavelength_ev'].values
            # result 开始计算
            E_UTA = (E_ij * f_ij * g_i).sum() / (f_ij * g_i).sum()
            Delta_E_UTA = np.sqrt((g_i * f_ij * (E_ij - E_UTA) ** 2).sum() / (g_i * f_ij).sum())
            temp_data[f'{index[0]}_{index[1]}'] = [E_UTA, Delta_E_UTA]
        return temp_data

    def get_statistics(self) -> dict:
        spec_path = (PROJECT_PATH() / f'cal_result/{self.name}/Spec.dat').as_posix()
        jenergy_path = (PROJECT_PATH() / f'cal_result/{self.name}/Jenergy-totaa.dat').as_posix()
        eav_path = (PROJECT_PATH() / f'cal_result/{self.name}/Eav.dat').as_posix()
        # Spec.dat 文件读取 =====================================
        spec = pd.read_fwf(spec_path, widths=[1, 11, 5, 3, 1, 8, 13, 5, 3, 1, 8, 13, 12, 8, 9, 8, 10, 9], header=None)
        spec = spec.dropna(axis=1)
        spec.columns = [
            'energy_l', 'J_l', 'index_l', 'configuration_l',
            'energy_h', 'J_h', 'index_h', 'configuration_h',
            'fnu', 'flam', 's2', 'gf', 'alggf', 'ga', 'brnch'
        ]
        # Jenergy-totaa.dat 文件读取 =====================================
        J_energy = pd.read_fwf(jenergy_path, widths=[9, 2, 10], names=['level', 'temp', 'gaa'])
        J_energy = J_energy.drop('temp', axis=1)
        # Eav.dat 文件读取 =====================================
        eav = pd.read_csv(eav_path, sep='\s+', names=['index_l', 'index_h', 'energy'])
        energy_ground = eav['energy'].values[0]
        eav['energy_with_ground'] = (eav['energy'] - energy_ground) * 0.124
        # 开始统计 ==================================================
        eav_2 = eav[eav['index_l'] == 2].__deepcopy__()
        eav_2 = eav_2.reset_index()
        eav_2 = eav_2.drop('index', axis=1)
        # 计算 Gaa
        spec['Gaa'] = np.NaN
        for i, v in enumerate(J_energy['level']):
            index = list(spec[v == spec['energy_h']].index)
            for v_index in index:
                spec.loc[v_index, 'Gaa'] = J_energy['gaa'][i]
        min_energy = spec['energy_l'].min()
        spec['energy_h'] = (spec['energy_h'] - min_energy) * 0.124
        spec['energy_l'] = (spec['energy_l'] - min_energy) * 0.124
        spec['fnu'] = 1239.85 / spec['fnu']  # 化完之后的单位时nm
        grouped_data = spec.groupby(['index_l', 'index_h'])
        info_dict = {}
        for key, v in grouped_data:
            configuration_info = {}

            max_wavelength = v['fnu'].max()
            min_wavelength = v['fnu'].min()
            line_range = {
                'max': max_wavelength,
                'min': min_wavelength,
            }
            configuration_info['wavelength_range'] = line_range

            line_num = v.shape[0]
            configuration_info['line_num'] = line_num

            # max_gf
            max_gf = v['gf'].max()
            configuration_info['max_gf'] = max_gf

            # Sum_gf
            sum_gf = v['gf'].sum()
            configuration_info['sum_gf'] = sum_gf

            # Sum_Ar
            sum_Ar = v['ga'].sum()
            configuration_info['sum_Ar'] = sum_Ar

            # Sum_Aa
            sum_Aa = v['Gaa'].sum()
            configuration_info['sum_Aa'] = sum_Aa

            # sum_G
            sum_G = (2 * v['J_h'] + 1).sum()
            configuration_info['sum_G'] = sum_G

            # ConAverGaSum
            temp_energy = eav_2[eav_2['index_h'] == key[1]]['energy_with_ground'].values[0]
            sum_ConAverGa = (v['gf'] * (1239.85 / v['fnu'] - temp_energy) ** 2).sum()
            configuration_info['sum_ConAverGa'] = sum_ConAverGa

            if sum_gf == 0:
                continue

            # 组态平均自电离几率=真理总自电离/总统计权重
            Aa_ave = sum_Aa / sum_G
            configuration_info['ave_Aa'] = Aa_ave

            # 平均自电离宽度=6.582E-16*组态平均自电离几率
            Ga_ave = 6.582e-16 * Aa_ave
            configuration_info['ave_Ga'] = Ga_ave

            # 能级统计宽度=sqrt(能级统计宽度分子项/总阵子强度),画能级图用
            ConAverGa = np.sqrt(sum_ConAverGa / sum_gf)
            configuration_info['ConAverGa'] = ConAverGa

            # ConEWidth(k)=ConAverGa(k)+AverGa(k)
            ConEWidth = ConAverGa + Ga_ave
            configuration_info['ConEWidth'] = ConEWidth

            # 将 configuration_info 添加到 info_dict 中
            info_dict[key] = configuration_info

        self.info_dict = info_dict
        return info_dict

    def load_class(self, class_info):
        self.name = class_info.name
        self.exp_data.load_class(class_info.exp_data)
        self.init_data = class_info.init_data
        self.plot_path = (PROJECT_PATH() / f'figure/line/{self.name}.html').as_posix()
        self.widen_all.load_class(class_info.widen_all)
        self.widen_part.load_class(class_info.widen_part)
        # start [1.0.0 > 1.0.1]
        if 'info_dict' in class_info.__dict__.keys():
            self.info_dict = class_info.info_dict
        else:
            self.info_dict = {}
        # end
