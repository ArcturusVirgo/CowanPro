import copy
from pathlib import Path
from typing import Optional, List

import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot

from .GlobalVar import PROJECT_PATH


class ExpData:
    def __init__(self, filepath: Path):
        """
        实验数据对象，一般附属于 Cowan、SimulateSpectral 对象

        Args:
            filepath: 实验数据所在的路径
        """
        self.plot_path = (PROJECT_PATH() / 'figure/exp.html').as_posix()  # 实验谱线的绘图路径
        self.filepath: Path = filepath  # 实验数据的路径

        self.init_data: Optional[pd.DataFrame] = None  # 原始的实验数据
        self.data: Optional[pd.DataFrame] = None  # 实验数据
        self.init_xrange = None  # 原始的波长范围
        self.x_range: Optional[List[float]] = None  # 实验数据的波长范围

        self.__read_file()

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
        self.init_data = copy.deepcopy(temp_data)
        self.x_range = [self.data['wavelength'].min(), self.data['wavelength'].max()]
        self.init_xrange = copy.deepcopy(self.x_range)

    def set_xrange(self, x_range: List[float]):
        """
        设置实验数据的波长范围

        Args:
            x_range: 波长范围，单位为 nm

        """
        self.x_range = [x_range[0], x_range[1]]
        self.data = self.init_data[(self.init_data['wavelength'] < self.x_range[1]) &
                                   (self.init_data['wavelength'] > self.x_range[0])]

    def reset_xrange(self):
        """
        重置实验数据的波长范围

        """
        self.set_xrange(self.init_xrange)

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

    def get_exp_data(self) -> pd.DataFrame:
        return self.data.__deepcopy__()

    def load_class(self, class_info):
        self.plot_path = (PROJECT_PATH() / 'figure/exp.html').as_posix()
        self.filepath = class_info.filepath
        # start [无版本号 > 1.0.0]
        if 'init_data' not in class_info.__dict__.keys():
            self.init_data = copy.deepcopy(class_info.data)
        else:
            self.init_data = class_info.init_data
        # end [无版本号 > 1.0.0]
        self.data = class_info.data
        self.init_xrange = class_info.init_xrange
        self.x_range = class_info.x_range
