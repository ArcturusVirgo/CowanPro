import copy
from typing import List, Tuple

import numpy as np
import plotly.graph_objs as go
from plotly.offline import plot

from .GlobalVar import PROJECT_PATH
from .SimulateSpectral import SimulateSpectral
from .CowanList import CowanList


class SpaceTimeResolution:
    def __init__(self):
        """
        用于存储空间时间分辨光谱
        """
        # 模拟光谱数据对象 列表
        self.simulate_spectral_dict: List[str:SimulateSpectral] = {}

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

    def set_xrange(self, x_range, num, cowan_lists: CowanList):
        for key, sim in self.simulate_spectral_dict.items():
            sim.set_xrange(x_range, num, cowan_lists)

    def reset_xrange(self, cowan_lists: CowanList):
        for key, sim in self.simulate_spectral_dict.items():
            sim.reset_xrange(cowan_lists)

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
                if (time, (space, '0', '0')) not in self.simulate_spectral_dict:
                    temp_t_res.append(None)
                    temp_d_res.append(None)
                    continue
                temp_t_res.append(
                    self.simulate_spectral_dict[(time, (space, '0', '0'))].temperature
                )
                temp_d_res.append(np.log10(  # 指数坐标
                    self.simulate_spectral_dict[
                        (time, (space, '0', '0'))
                    ].electron_density
                ))
            t_res.append(temp_t_res)
            d_res.append(temp_d_res)

        if var_index == 0:
            trace1 = go.Heatmap(x=spaces, y=times, z=t_res)
        else:
            trace1 = go.Heatmap(x=spaces, y=times, z=d_res)
        data = [trace1]
        layout = go.Layout(
            margin=go.layout.Margin(b=15, l=60, r=0, t=0),
            # coloraxis={
            #     'type': 'log',
            # }
        )
        fig = go.Figure(data=data, layout=layout)
        plot(fig, filename=self.change_by_space_time_path, auto_open=False)

    def get_simulate_spectral_diagnosed_by_index(self, index):
        """
        获取已诊断的所有对象的索引获取数据
        Args:
            index:

        Returns:

        """
        temp_list = []
        for key, value in self.simulate_spectral_dict.items():
            key: tuple
            value: SimulateSpectral
            if value.get_temperature_and_density() == (None, None):
                continue
            temp_list.append([copy.deepcopy(key), copy.deepcopy(value)])
        return temp_list[index]

    def __getitem__(self, index) -> Tuple[str, SimulateSpectral]:
        return (list(self.simulate_spectral_dict.keys())[index],
                list(self.simulate_spectral_dict.values())[index])

    def __iter__(self):
        return iter(self.simulate_spectral_dict.items())

    def load_class(self, class_info):
        for (ok, ov), (nk, nv) in zip(self.simulate_spectral_dict.items(), class_info.simulate_spectral_dict.items()):
            ov.load_class(nv)
            self.simulate_spectral_dict[nk] = ov

        self.change_by_time_path = (PROJECT_PATH().joinpath('figure/change/by_time.html').as_posix())
        self.change_by_location_path = (PROJECT_PATH().joinpath('figure/change/by_location.html').as_posix())
        self.change_by_space_time_path = (PROJECT_PATH().joinpath('figure/change/by_space_time.html').as_posix())
