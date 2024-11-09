import os
import copy
import functools
from concurrent.futures import ProcessPoolExecutor

import numpy as np
from PySide6 import QtCore
from PySide6.QtCore import Signal

from .SimulateSpectral import SimulateSpectral
from .. import console_logger


class SimulateGrid:
    def __init__(self, temperature, density, simulate: SimulateSpectral):
        """
        用于存储模拟光谱的网格数据

        Args:
            temperature: 温度范围 [开始 结束 个数]
            density: 密度范围 [开始底数 开始指数 结束底数 结束指数 个数]
            simulate: 要模拟的simulate对象
        """
        super().__init__()
        self.task = 'cal'
        self.use_multiprocess = True
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

    def load_class(self, class_info):
        self.task = class_info.task
        if class_info.update_exp is None:
            self.update_exp = class_info.update_exp
        else:
            self.update_exp.load_class(class_info.update_exp)
        if hasattr(class_info, 'use_multiprocess'):
            self.use_multiprocess = class_info.use_multiprocess
        else:
            self.use_multiprocess = True
        self.simulate.load_class(class_info.simulate)
        self.temperature_tuple = class_info.temperature_tuple
        self.density_tuple = class_info.density_tuple
        self.t_num = class_info.t_num
        self.ne_num = class_info.ne_num

        self.t_list = class_info.t_list
        self.ne_list = class_info.ne_list

        self.grid_data = class_info.grid_data


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
        self.use_multiprocess = old_grid.use_multiprocess
        self.update_exp = old_grid.update_exp

        self.simulate = copy.deepcopy(old_grid.simulate)
        self.temperature_tuple = old_grid.temperature_tuple
        self.density_tuple = old_grid.density_tuple
        self.t_num: int = old_grid.t_num
        self.ne_num: int = old_grid.ne_num

        self.t_list = old_grid.t_list
        self.ne_list = old_grid.ne_list

        self.grid_data = old_grid.grid_data

        self.finished.connect(self.update_origin)

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
            simulate_: SimulateSpectral = f.result()
            simulate_.del_cowan_list()
            self.grid_data[(t, ne)] = simulate_
            self.progress.emit(str(int(current_progress / self.t_num / self.ne_num * 100)))

        self.grid_data = {}
        current_progress = 0
        if self.use_multiprocess:
            # 多线程
            console_logger.info('use multiprocess to simulate grid data.')
            pool = ProcessPoolExecutor(os.cpu_count() - 1)
            for temperature in self.t_list:
                for density in self.ne_list:
                    simulate = copy.deepcopy(self.simulate)
                    simulate.set_temperature_and_density(eval(temperature), eval(density))
                    simulate.con_contribution = None  # 清空组态贡献
                    future = pool.submit(simulate.simulate_spectral)
                    future.add_done_callback(functools.partial(callback, temperature, density))
            pool.shutdown()
        else:
            # 单线程
            console_logger.info('use single process to simulate grid data.')
            for temperature in self.t_list:
                for density in self.ne_list:
                    simulate = copy.deepcopy(self.simulate)
                    simulate.set_temperature_and_density(eval(temperature), eval(density))
                    simulate.con_contribution = None  # 清空组态贡献
                    simulate.simulate_spectral()
                    simulate.del_cowan_list()
                    self.grid_data[(temperature, density)] = simulate

                    current_progress += 1
                    self.progress.emit(str(int(current_progress / self.t_num / self.ne_num * 100)))

        # 发送结束信号
        self.end.emit(0)

    def update_similarity(self, exp_obj):
        """
        更新网格数据的相似度

        Args:
            exp_obj: 实验光谱对象

        """
        for key, value in self.grid_data.items():
            self.simulate = copy.deepcopy(value)
            self.simulate.exp_data = copy.deepcopy(exp_obj)
            self.simulate.cal_spectrum_similarity()
            self.grid_data[key] = copy.deepcopy(self.simulate)
        self.up_end.emit(0)

    def update_origin(self):
        """
        更新原始的网格数据

        """
        self.old_grid.grid_data = self.grid_data
