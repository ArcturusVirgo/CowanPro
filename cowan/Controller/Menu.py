import copy
from pathlib import Path

import pandas as pd
from PySide6.QtWidgets import QFileDialog, QDialog, QPushButton, \
    QHBoxLayout, QDoubleSpinBox, QLabel, QVBoxLayout

from main import VerticalLine, MainWindow
from ..Model import PROJECT_PATH
from ..Tools import ProgressThread


class Menu(MainWindow):
    def show_guides(self):
        """
        显示参考线

        """
        if self.v_line is None:
            x, y = self.ui.exp_web.mapToGlobal(self.ui.exp_web.pos()).toTuple()
            self.v_line = VerticalLine(x, y - 100, self.window().height() - 100)
            self.v_line.show()
            self.ui.show_guides.setText('隐藏参考线')
        else:
            self.v_line.close()
            self.v_line = None
            self.ui.show_guides.setText('显示参考线')

    def export_data(self):
        """
        导出数据

        """

        def save_simulate_data(sim):
            exp_wavelength = sim.exp_data.data['wavelength']
            exp_intensity = sim.exp_data.data['intensity']
            exp_intensity_normalization = sim.exp_data.data['intensity_normalization']
            cal_wavelength = copy.deepcopy(sim.sim_data['wavelength'])
            cal_intensity = copy.deepcopy(sim.sim_data['intensity'])
            cal_intensity_normalization = copy.deepcopy(sim.sim_data['intensity_normalization'])
            datas = pd.DataFrame({
                'exp_wavelength': exp_wavelength,
                'exp_intensity': exp_intensity,
                'exp_intensity_normalization': exp_intensity_normalization,
                'cal_wavelength': cal_wavelength,
                'cal_intensity': cal_intensity,
                'cal_intensity_normalization': cal_intensity_normalization,
            })
            datas.to_csv(path.joinpath(filename_1), index=False)

        path = QFileDialog.getExistingDirectory(self, '选择存储路径', PROJECT_PATH().as_posix())
        if path == '':
            return
        path = Path(path)

        atom_symbol = self.cowan_lists[0][0].in36.atom.symbol
        atom_num = self.cowan_lists[0][0].in36.atom.num

        # 时空分辨
        export_table = []
        for key, value in self.space_time_resolution.simulate_spectral_dict.items():
            filename_1 = f'{key[0]}_{key[1][0]}_simulate_data.csv'
            temp_1 = [key[0],
                      key[1][0],
                      value.temperature,
                      value.electron_density,
                      filename_1]
            if value.temperature is not None and value.electron_density is not None:
                save_simulate_data(value)
                value.init_cowan_list(self.cowan_lists)
                temp = value.get_abu(value.temperature, value.electron_density)
                value.del_cowan_list()
            else:
                temp = [None] * self.cowan_lists[0][0].in36.atom.num
            export_table.append(temp_1 + temp)
        columns = ['时间', '位置', '温度', '电子密度', '模拟光谱'] + [f'{atom_symbol}{i}+' for i in range(atom_num)]
        data = pd.DataFrame(export_table, columns=columns)
        data.to_excel(path.joinpath('space_time_resolution.xlsx'), index=False)

        cowan_info = []
        for cowan_, _ in self.cowan_lists:
            temp = [
                cowan_.name,
                cowan_.coupling_mode,
                cowan_.cal_data.widen_all.delta_lambda,
                cowan_.cal_data.widen_all.fwhm_value,
            ]
            cowan_info.append(temp)
        cowan_info = pd.DataFrame(cowan_info, columns=['名称', '耦合模式', '偏移量', '半高全宽'])
        cowan_info.to_excel(path.joinpath('cowan_info.xlsx'), index=False)

        self.ui.statusbar.showMessage('数据导出完成！')

    def set_xrange(self):
        """
        设置波长范围

        """

        def update_xrange():
            def task():
                self.task_thread.progress.emit(0, 'ready to set range ...')
                x_range = [min_input.value(), max_input.value(), step_input.value()]
                num = int((x_range[1] - x_range[0]) / x_range[2])

                # 设置 info --------------------------------
                self.info['x_range'] = x_range
                # 设置第一页的实验谱线 --------------------------------
                self.task_thread.progress.emit(10, 'self.expdata_1 set range ...')
                if self.expdata_1 is not None:
                    self.expdata_1.set_xrange(x_range)
                # 设置 页面上的 Cowan  --------------------------------
                self.task_thread.progress.emit(20, 'self.cowan set range ...')
                if self.cowan is not None:
                    self.cowan.set_xrange(x_range, num)
                # 设置各个 Cowan  --------------------------------
                self.task_thread.progress.emit(30, 'self.cowan_lists set range ...')
                if self.cowan_lists is not None:
                    self.cowan_lists.set_xrange(x_range, num)
                # 设置第二页的实验谱线  --------------------------------
                self.task_thread.progress.emit(40, 'self.expdata_2 set range ...')
                if self.expdata_2 is not None:
                    self.expdata_2.set_xrange(x_range)
                # 设置叠加谱线 --------------------------------
                self.task_thread.progress.emit(50, 'self.simulate set range ...')
                if self.simulate is not None:
                    self.simulate.set_xrange(x_range, num, self.cowan_lists)
                # 设置实验叠加谱线 --------------------------------
                self.task_thread.progress.emit(100, 'self.space_time_resolution set range ...')
                if self.space_time_resolution is not None:
                    self.space_time_resolution.set_xrange(x_range, num, self.cowan_lists)
                # 完成 --------------------------------
                self.ui.statusbar.showMessage('设置范围成功！')

            dialog.close()
            self.task_thread = ProgressThread(dialog_title='正在设置范围...', range_=(0, 100))
            self.task_thread.set_run(task)
            self.task_thread.start()

        dialog = QDialog()
        label = QLabel('请输入范围以及最小步长：')
        # 最大最小值以及步长
        min_input = QDoubleSpinBox()  # 定义
        max_input = QDoubleSpinBox()
        step_input = QDoubleSpinBox()
        spin_box_list = [min_input, max_input, step_input]
        if self.info['x_range'] is not None:
            min_input.setValue(self.info['x_range'][0])  # 设置初始值
            max_input.setValue(self.info['x_range'][1])
            step_input.setValue(self.info['x_range'][2])
        else:
            min_input.setValue(self.expdata_1.x_range[0])  # 设置初始值
            max_input.setValue(self.expdata_1.x_range[1])
            step_input.setValue(0.01)
        layout_input = QHBoxLayout()
        for spin_box in spin_box_list:
            spin_box.setSuffix('nm')  # 设置单位
            spin_box.setDecimals(3)  # 设置精度
            spin_box.setSingleStep(0.010)  # 设置步长
            layout_input.addWidget(spin_box)
        ok_btn = QPushButton('确认')
        cancel_btn = QPushButton('取消')
        layout_btn = QHBoxLayout()
        layout_btn.addWidget(ok_btn)
        layout_btn.addWidget(cancel_btn)
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addLayout(layout_input)
        layout.addLayout(layout_btn)
        dialog.setLayout(layout)

        cancel_btn.clicked.connect(dialog.close)
        ok_btn.clicked.connect(update_xrange)  # 开始执行

        dialog.exec()

    def reset_xrange(self):
        """
        重置波长范围

        """

        def task():
            self.task_thread.progress.emit(0, 'ready to reset range ...')
            self.info['x_range'] = None
            widen_temperature = self.ui.widen_temp.value()

            # 设置第一页的实验谱线
            self.task_thread.progress.emit(10, 'self.expdata_1 reset range ...')
            if self.expdata_1 is not None:
                self.expdata_1.reset_xrange()
            # 设置 页面上的 Cowan
            self.task_thread.progress.emit(20, 'self.cowan reset range ...')
            if self.cowan is not None:
                self.cowan.reset_xrange()
            # 设置各个 Cowan
            self.task_thread.progress.emit(30, 'self.cowan_lists reset range ...')
            if self.cowan_lists is not None:
                self.cowan_lists.reset_xrange()
            # 设置第二页的实验谱线
            self.task_thread.progress.emit(40, 'self.expdata_2 reset range ...')
            if self.expdata_2 is not None:
                self.expdata_2.reset_xrange()
            # 设置叠加谱线
            self.task_thread.progress.emit(50, 'self.simulate reset range ...')
            if self.simulate is not None:
                self.simulate.reset_xrange(self.cowan_lists)
            # 设置实验叠加谱线
            self.task_thread.progress.emit(100, 'self.space_time_resolution reset range ...')
            if self.space_time_resolution is not None:
                self.space_time_resolution.reset_xrange(self.cowan_lists)

            self.ui.statusbar.showMessage('重置范围成功！')

        self.task_thread = ProgressThread(dialog_title='正在重置范围...', range_=(0, 100))
        self.task_thread.set_run(task)
        self.task_thread.start()

    def export_con_ave_wave(self):
        path = QFileDialog.getExistingDirectory(self, '选择存储路径', PROJECT_PATH().as_posix())
        if path == '':
            return
        path = Path(path)

        data_frames = {}
        names = ['下态序号', '上态序号', '跃迁名称', '平均波长(nm)']
        for cowan_, _ in self.cowan_lists:
            ave_w = cowan_.cal_data.get_average_wavelength()
            temp_1 = []
            temp_2 = []
            temp_3 = []
            temp_4 = []
            for key, value in ave_w.items():
                temp_1.append(int(key.split('_')[0]))
                temp_2.append(int(key.split('_')[1]))
                temp_3.append(
                    self.cowan.in36.get_configuration_name(
                        int(key.split('_')[0]),
                        int(key.split('_')[1])
                    )
                )
                temp_4.append(value)
            # 将数据放在DataFrame中
            data_frames[cowan_.name] = (
                pd.DataFrame({names[0]: temp_1, names[1]: temp_2, names[2]: temp_3, names[3]: temp_4}))
            # 存储
            with pd.ExcelWriter(path.joinpath('组态平均波长.xlsx'), ) as writer:
                for key, value in data_frames.items():
                    value.to_excel(writer, sheet_name=key, index=False)

        self.ui.statusbar.showMessage('导出成功！')
