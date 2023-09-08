import functools

import matplotlib
import numpy as np
import pandas as pd
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QBrush, QColor
from PySide6.QtWidgets import QTableWidgetItem, QListWidgetItem, QTreeWidgetItem

from .cowan import SUBSHELL_SEQUENCE, ANGULAR_QUANTUM_NUM_NAME
from .tools import rainbow_color
from main import MainWindow


class UpdatePage1(MainWindow):
    def update_atom(self):
        # 改变元素选择器
        self.ui.atomic_num.setCurrentIndex(self.atom.num - 1)
        self.ui.atomic_name.setCurrentIndex(self.atom.num - 1)
        self.ui.atomic_symbol.setCurrentIndex(self.atom.num - 1)
        # 改变离化度列表
        self.ui.atomic_ion.clear()
        self.ui.atomic_ion.addItems([str(i) for i in range(self.atom.num)])
        self.ui.atomic_ion.setCurrentIndex(self.atom.ion)
        functools.partial(UpdatePage1.update_atom_ion, self)()

    def update_atom_ion(self):
        # 改变基组态
        self.ui.base_configuration.setText(self.atom.base_configuration)
        # 改变下态列表
        self.ui.low_configuration.clear()
        self.ui.low_configuration.addItems(list(self.atom.electron_arrangement.keys()))
        self.ui.low_configuration.setCurrentIndex(
            len(self.atom.electron_arrangement.keys()) - 1
        )
        # 改变上态列表
        self.ui.high_configuration.clear()
        temp_list = []
        for value in SUBSHELL_SEQUENCE:
            l_ = ANGULAR_QUANTUM_NUM_NAME.index(value[1])
            if value in self.atom.electron_arrangement.keys():
                if self.atom.electron_arrangement[value] != 4 * l_ + 2:
                    temp_list.append(value)
            else:
                temp_list.append(value)
        self.ui.high_configuration.addItems(temp_list)
        self.ui.high_configuration.setCurrentIndex(1)

    def update_in36_configuration(self):
        # 更新表格
        df = pd.DataFrame(
            list(zip(*self.in36.configuration_card))[0],
            columns=['原子序数', '原子状态', '标识符', '空格', '组态'],
            index=list(range(1, len(self.in36.configuration_card) + 1)),
        )
        df['宇称'] = list(zip(*self.in36.configuration_card))[1]
        df = df[['宇称', '原子状态', '组态']]
        self.ui.in36_configuration_view.clear()
        self.ui.in36_configuration_view.setRowCount(df.shape[0])
        self.ui.in36_configuration_view.setColumnCount(df.shape[1])
        self.ui.in36_configuration_view.setHorizontalHeaderLabels(df.columns)
        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                item = QTableWidgetItem(str(df.iloc[i, j]))
                self.ui.in36_configuration_view.setItem(i, j, item)

    def update_in36_control(self):
        for i in range(23):
            eval(f'self.ui.in36_{i + 1}').setText(self.in36.control_card[i].strip(' '))

    def update_in36(self):
        # 更新in36控制卡输入区
        functools.partial(UpdatePage1.update_in36_control, self)()
        # 更新in36组态输入区
        functools.partial(UpdatePage1.update_in36_configuration, self)()

    def update_in2(self):
        in2_input_name = [
            'in2_1',
            'in2_2',
            'in2_3',
            'in2_4',
            'in2_5',
            'in2_6',
            'in2_7',
            'in2_8',
            'in2_9_a',
            'in2_9_b',
            'in2_9_c',
            'in2_9_d',
            'in2_10',
            'in2_11_a',
            'in2_11_b',
            'in2_11_c',
            'in2_11_d',
            'in2_11_e',
            'in2_12',
            'in2_13',
            'in2_14',
            'in2_15',
            'in2_16',
            'in2_17',
            'in2_18',
            'in2_19',
        ]
        for i, n in enumerate(in2_input_name):
            if '11' in n:
                eval(f'self.ui.{n}').setValue(int(self.in2.input_card[i].strip(' ')))
            else:
                eval(f'self.ui.{n}').setText(self.in2.input_card[i].strip(' '))

    def update_history_list(self):
        self.ui.run_history_list.clear()
        for cowan in self.run_history:
            self.ui.run_history_list.addItem(QListWidgetItem(cowan.name))

    def update_selection_list(self):
        self.ui.selection_list.clear()
        self.ui.page2_selection_list.clear()
        for cowan in self.simulate.cowan_list:
            self.ui.selection_list.addItem(QListWidgetItem(cowan.name))
            item = QListWidgetItem(cowan.name)
            item.setCheckState(Qt.CheckState.Checked)
            self.ui.page2_selection_list.addItem(item)

    def update_exp_figure(self):
        self.expdata_1.plot_html()
        self.ui.exp_web.load(QUrl.fromLocalFile(self.expdata_1.plot_path))

    def update_line_figure(self):
        self.cowan.cal_data.plot_line()
        # 加载线状谱
        self.ui.web_cal_line.load(QUrl.fromLocalFile(self.cowan.cal_data.plot_path))

    def update_widen_figure(self):
        self.cowan.cal_data.widen_all.plot_widen()

        if self.ui.crossP.isChecked():
            self.ui.web_cal_widen.load(
                QUrl.fromLocalFile(self.cowan.cal_data.widen_all.plot_path_cross_P)
            )
        elif self.ui.crossNP.isChecked():
            self.ui.web_cal_widen.load(
                QUrl.fromLocalFile(self.cowan.cal_data.widen_all.plot_path_cross_NP)
            )
        elif self.ui.gauss.isChecked():
            self.ui.web_cal_widen.load(
                QUrl.fromLocalFile(self.cowan.cal_data.widen_all.plot_path_gauss)
            )


class UpdatePage2(MainWindow):
    def update_exp_sim_figure(self):
        self.simulate.plot_html()
        self.ui.page2_add_spectrum_web.load(QUrl.fromLocalFile(self.simulate.plot_path))

    def update_exp_figure(self):
        # 更新界面
        self.expdata_2.plot_html()
        self.ui.page2_add_spectrum_web.load(QUrl.fromLocalFile(self.expdata_2.plot_path))

    def update_grid(self):
        self.ui.page2_grid_list.clear()
        self.ui.page2_grid_list.setRowCount(self.simulated_grid.ne_num)
        self.ui.page2_grid_list.setColumnCount(self.simulated_grid.t_num)
        self.ui.page2_grid_list.setHorizontalHeaderLabels(self.simulated_grid.t_list)
        self.ui.page2_grid_list.setVerticalHeaderLabels(self.simulated_grid.ne_list)
        sim_max = max(
            self.simulated_grid.grid_data.values(), key=lambda x: x.spectrum_similarity
        ).spectrum_similarity
        for t in self.simulated_grid.t_list:
            for ne in self.simulated_grid.ne_list:
                similarity = self.simulated_grid.grid_data[(t, ne)].spectrum_similarity
                item = QTableWidgetItem('{:.4f}'.format(similarity))
                item.setBackground(QBrush(QColor(*rainbow_color(similarity / sim_max))))
                self.ui.page2_grid_list.setItem(
                    self.simulated_grid.ne_list.index(ne),
                    self.simulated_grid.t_list.index(t),
                    item,
                )

    def update_space_time_table(self):
        self.ui.st_resolution_table.clear()
        self.ui.st_resolution_table.setRowCount(
            len(self.space_time_resolution.simulate_spectral_dict)
        )
        self.ui.st_resolution_table.setColumnCount(5)
        self.ui.st_resolution_table.setHorizontalHeaderLabels(
            ['时间', '位置', '温度', '密度', '实验谱']
        )
        for i, (key, value) in enumerate(
            self.space_time_resolution.simulate_spectral_dict.items()
        ):
            item1 = QTableWidgetItem(key[0])
            item2 = QTableWidgetItem(f'({key[1][0]}, {key[1][1]}, {key[1][2]})')
            if value.temperature is not None and value.electron_density is not None:
                item3 = QTableWidgetItem('{:.3f}'.format(value.temperature))
                item4 = QTableWidgetItem('{:.3e}'.format(value.electron_density))
            else:
                item3 = QTableWidgetItem('None')
                item3.setBackground(QBrush(QColor(255, 0, 0)))
                item4 = QTableWidgetItem('None')
                item4.setBackground(QBrush(QColor(255, 0, 0)))
            item5 = QTableWidgetItem(value.exp_data.filepath.name)
            self.ui.st_resolution_table.setItem(i, 0, item1)
            self.ui.st_resolution_table.setItem(i, 1, item2)
            self.ui.st_resolution_table.setItem(i, 2, item3)
            self.ui.st_resolution_table.setItem(i, 3, item4)
            self.ui.st_resolution_table.setItem(i, 4, item5)

    def update_temperature_density(self):
        self.ui.page2_temperature.setValue(self.simulate.temperature)
        temp = '{:.2e}'.format(self.simulate.electron_density)
        base = eval(temp.split('e+')[0])
        index = eval(temp.split('e+')[1])
        self.ui.page2_density_base.setValue(base)
        self.ui.page2_density_index.setValue(index)


class UpdatePage3(MainWindow):
    def update_space_time_combobox(self):
        self.ui.location_select.clear()
        self.ui.time_select.clear()
        temp_times = []
        temp_locations = []
        for key in self.space_time_resolution.simulate_spectral_dict:
            if (
                self.space_time_resolution.simulate_spectral_dict[key].temperature
                is not None
                or self.space_time_resolution.simulate_spectral_dict[
                    key
                ].electron_density
                is not None
            ):
                temp_times.append(key[0])
                temp_locations.append(key[1])
        temp_times = set(temp_times)
        temp_locations = set(temp_locations)
        temp_times = [f'{key}' for key in temp_times]
        temp_locations = [f'({key[0]}, {key[1]}, {key[2]})' for key in temp_locations]
        self.ui.location_select.addItems(temp_locations)
        self.ui.time_select.addItems(temp_times)


class UpdatePage4(MainWindow):
    def update_space_time_combobox(self):
        self.ui.comboBox.clear()
        temp_list = []
        for key in self.space_time_resolution.simulate_spectral_dict:
            if (
                self.space_time_resolution.simulate_spectral_dict[key].temperature
                is not None
                or self.space_time_resolution.simulate_spectral_dict[
                    key
                ].electron_density
                is not None
            ):
                temp_list.append(
                    '时间：{}       位置：{}, {}, {}'.format(
                        key[0], key[1][0], key[1][1], key[1][2]
                    )
                )
        self.ui.comboBox.addItems(temp_list)

    def update_treeview(self):
        for c in self.simulate_page4.cowan_list:
            c.cal_data.widen_part.widen_by_group()

            parents = QTreeWidgetItem()
            parents.setText(0, c.name.replace('_', '+'))
            parents.setCheckState(0, Qt.Checked)
            self.ui.treeWidget.addTopLevelItem(parents)

            for example in c.cal_data.widen_part.grouped_widen_data:
                child = QTreeWidgetItem()
                child.setCheckState(0, Qt.Checked)
                index_low, index_high = map(int, example.split('_'))
                child.setText(0, c.in36.get_configuration_name(index_low, index_high))
                parents.addChild(child)

    def update_exp_figure(self):
        self.simulate_page4.plot_html()
        self.ui.webEngineView.load(QUrl.fromLocalFile(self.simulate_page4.plot_path))
