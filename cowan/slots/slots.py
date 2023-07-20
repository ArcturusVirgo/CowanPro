import copy
import functools
import shutil
from pathlib import Path

import pandas as pd
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QAction, QCursor
from PySide6.QtWidgets import QFileDialog, QTableWidgetItem, QDialog, QTextBrowser, QVBoxLayout, QMenu, QListWidgetItem, \
    QMessageBox

from cowan import PROJECT_PATH
from cowan.cowan import ExpData, Atom, SUBSHELL_SEQUENCE, ANGULAR_QUANTUM_NUM_NAME, In36, In2, Cowan
from main import MainWindow, VerticalLine


class Menu(MainWindow):
    def load_exp_data(self):
        path, types = QFileDialog.getOpenFileName(self, '请选择实验数据', PROJECT_PATH.as_posix(),
                                                  '数据文件(*.txt *.csv)')
        path = Path(path)
        # 将实验数据复制到项目路径下
        if 'csv' in path.name:
            new_path = PROJECT_PATH / f'exp_data.csv'
        elif 'txt' in path.name:
            new_path = PROJECT_PATH / f'exp_data.txt'
        else:
            raise Exception('文件格式错误')
        try:
            shutil.copyfile(path, new_path)
        except shutil.SameFileError:
            pass

        # 更新实验数据
        self.exp_data_1 = ExpData(new_path)
        self.exp_data_1.plot_html()
        # 更新页面
        self.ui.exp_web.load(QUrl.fromLocalFile(self.exp_data_1.plot_path))

    def show_guides(self):
        if self.v_line is None:
            x, y = self.ui.exp_web.mapToGlobal(self.ui.exp_web.pos()).toTuple()
            self.v_line = VerticalLine(x, y - 100, self.window().height() - 100)
            self.v_line.show()
            self.ui.show_guides.setText('隐藏参考线')
        else:
            self.v_line.close()
            self.v_line = None
            self.ui.show_guides.setText('显示参考线')


class Page1(MainWindow):
    def atom_changed(self, index):
        self.atom = Atom(index + 1, 0)
        self.in36 = In36(self.atom)

        # ----------------------------- 更新页面 -----------------------------
        # 改变元素选择器
        self.ui.atomic_num.setCurrentIndex(self.atom.num - 1)
        self.ui.atomic_name.setCurrentIndex(self.atom.num - 1)
        self.ui.atomic_symbol.setCurrentIndex(self.atom.num - 1)
        # 改变离化度列表
        self.ui.atomic_ion.clear()
        self.ui.atomic_ion.addItems([str(i) for i in range(self.atom.num)])
        self.ui.atomic_ion.setCurrentIndex(self.atom.ion)
        # 改变基组态
        self.ui.base_configuration.setText(self.atom.base_configuration)
        # 改变下态列表
        self.ui.low_configuration.clear()
        self.ui.low_configuration.addItems(list(self.atom.electron_arrangement.keys()))
        self.ui.low_configuration.setCurrentIndex(len(self.atom.electron_arrangement.keys()) - 1)
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

    def atom_ion_changed(self, index):
        self.atom = Atom(self.ui.atomic_num.currentIndex() + 1, index)
        self.in36 = In36(self.atom)

        # ----------------------------- 更新页面 -----------------------------
        # 改变基组态
        self.ui.base_configuration.setText(self.atom.base_configuration)
        # 改变下态列表
        self.ui.low_configuration.clear()
        self.ui.low_configuration.addItems(list(self.atom.electron_arrangement.keys()))
        self.ui.low_configuration.setCurrentIndex(len(self.atom.electron_arrangement.keys()) - 1)
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

    def add_configuration(self):
        # 如果是自动添加
        if self.ui.auto_write_in36.isChecked():
            # 获取基组态
            low_configuration = self.atom.get_configuration()
            # 获取激发组态
            self.atom.arouse_electron(self.ui.low_configuration.currentText(),
                                      self.ui.high_configuration.currentText())
            high_configuration = self.atom.get_configuration()
            self.atom.revert_to_ground_state()

            # 添加组态
            self.in36.add_configuration(low_configuration)
            self.in36.add_configuration(high_configuration)
        # 如果是手动添加
        elif self.ui.manual_write_in36.isChecked():
            self.in36.add_configuration(self.ui.configuration_edit.text())

        # ----------------------------- 更新页面 -----------------------------
        # 更新表格
        df = pd.DataFrame(list(zip(*self.in36.configuration_card))[0],
                          columns=['原子序数', '原子状态', '标识符', '空格', '组态'],
                          index=list(range(1, len(self.in36.configuration_card) + 1)))
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

    def load_in36(self):
        path, types = QFileDialog.getOpenFileName(self, '请选择in36文件', PROJECT_PATH.as_posix(), '')
        if path == '':
            return
        self.in36.read_from_file(Path(path))
        self.atom = copy.deepcopy(self.in36.atom)

        # ----------------------------- 更新页面 -----------------------------
        # 改变元素选择器
        self.ui.atomic_num.setCurrentIndex(self.atom.num - 1)
        self.ui.atomic_name.setCurrentIndex(self.atom.num - 1)
        self.ui.atomic_symbol.setCurrentIndex(self.atom.num - 1)
        # 改变离化度列表
        self.ui.atomic_ion.clear()
        self.ui.atomic_ion.addItems([str(i) for i in range(self.atom.num)])
        self.ui.atomic_ion.setCurrentIndex(self.atom.ion)
        # 改变基组态
        self.ui.base_configuration.setText(self.atom.base_configuration)
        # 改变下态列表
        self.ui.low_configuration.clear()
        self.ui.low_configuration.addItems(list(self.atom.electron_arrangement.keys()))
        self.ui.low_configuration.setCurrentIndex(len(self.atom.electron_arrangement.keys()) - 1)
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
        # 更新in36控制卡输入区
        for i in range(23):
            eval(f'self.ui.in36_{i + 1}').setText(self.in36.control_card[i].strip(' '))
        # 更新in36组态输入区
        df = pd.DataFrame(list(zip(*self.in36.configuration_card))[0],
                          columns=['原子序数', '原子状态', '标识符', '空格', '组态'],
                          index=list(range(1, len(self.in36.configuration_card) + 1)))
        df['宇称'] = list(zip(*self.in36.configuration_card))[1]
        df = df[['宇称', '原子状态', '组态']]
        # 更新表格
        self.ui.in36_configuration_view.clear()
        self.ui.in36_configuration_view.setRowCount(df.shape[0])
        self.ui.in36_configuration_view.setColumnCount(df.shape[1])
        self.ui.in36_configuration_view.setHorizontalHeaderLabels(df.columns)
        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                item = QTableWidgetItem(str(df.iloc[i, j]))
                self.ui.in36_configuration_view.setItem(i, j, item)

    def load_in2(self):
        path, types = QFileDialog.getOpenFileName(self, '请选择in2文件', PROJECT_PATH.as_posix(), '')
        if path == '':
            return
        self.in2.read_from_file(path)
        # ----------------------------- 更新页面 -----------------------------
        in2_input_name = ['in2_1', 'in2_2', 'in2_3', 'in2_4', 'in2_5', 'in2_6', 'in2_7', 'in2_8',
                          'in2_9_a', 'in2_9_b', 'in2_9_c', 'in2_9_d',
                          'in2_10',
                          'in2_11_a', 'in2_11_b', 'in2_11_c', 'in2_11_d', 'in2_11_e',
                          'in2_12', 'in2_13', 'in2_14', 'in2_15', 'in2_16', 'in2_17', 'in2_18', 'in2_19', ]
        for i, n in enumerate(in2_input_name):
            if '11' in n:
                eval(f'self.ui.{n}').setValue(int(self.in2.input_card[i].strip(' ')))
            else:
                eval(f'self.ui.{n}').setText(self.in2.input_card[i].strip(' '))

    def preview_in36(self):
        dialog = QDialog()
        dialog.resize(1000, 500)
        text_browser = QTextBrowser(dialog)
        dialog_layout = QVBoxLayout(dialog)

        dialog_layout.addWidget(text_browser)
        dialog.setLayout(dialog_layout)

        Page1.get_in36_control_card(self, self.in36)
        in36 = self.in36.get_text()

        temp = '↓         ↓         ↓         ↓         ↓         ↓         ↓         ↓         \n'
        text_browser.setText(temp + in36)
        text_browser.setStyleSheet('font: 12pt "Consolas";')

        dialog.setWindowModality(Qt.ApplicationModal)

        dialog.exec()

    def preview_in2(self):
        dialog = QDialog()
        dialog.resize(1000, 500)
        text_browser = QTextBrowser(dialog)
        dialog_layout = QVBoxLayout(dialog)

        dialog_layout.addWidget(text_browser)
        dialog.setLayout(dialog_layout)

        Page1.get_in2_control_card(self, self.in2)
        in2 = self.in2.get_text()

        temp = '↓         ↓         ↓         ↓         ↓         ↓         ↓         ↓         \n'
        text_browser.setText(temp + in2)
        text_browser.setStyleSheet('font: 12pt "Consolas";')

        dialog.setWindowModality(Qt.ApplicationModal)

        dialog.exec()

    def configuration_move_up(self):
        index = self.ui.in36_configuration_view.currentIndex().row()
        if 1 <= index <= len(self.in36.configuration_card):
            self.in36.configuration_move(index, 'up')

            # ----------------------------- 更新页面 -----------------------------
            # 更新 in36 组态输入区
            df = pd.DataFrame(list(zip(*self.in36.configuration_card))[0],
                              columns=['原子序数', '原子状态', '标识符', '空格', '组态'],
                              index=list(range(1, len(self.in36.configuration_card) + 1)))
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
            self.ui.in36_configuration_view.setCurrentIndex(self.ui.in36_configuration_view.model().index(index - 1, 0))

    def configuration_move_down(self):
        index = self.ui.in36_configuration_view.currentIndex().row()
        if 0 <= index <= len(self.in36.configuration_card) - 2:
            self.in36.configuration_move(index, 'down')

            # ----------------------------- 更新页面 -----------------------------
            # 更新 in36 组态输入区
            df = pd.DataFrame(list(zip(*self.in36.configuration_card))[0],
                              columns=['原子序数', '原子状态', '标识符', '空格', '组态'],
                              index=list(range(1, len(self.in36.configuration_card) + 1)))
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
            self.ui.in36_configuration_view.setCurrentIndex(self.ui.in36_configuration_view.model().index(index + 1, 0))

    def in2_11_e_value_changed(self, value):
        self.ui.in2_11_a.setValue(value)
        self.ui.in2_11_c.setValue(value)
        self.ui.in2_11_d.setValue(value)

    def auto_write_in36(self):
        self.ui.high_configuration.setEnabled(True)
        self.ui.configuration_edit.setEnabled(False)
        self.ui.low_configuration.setEnabled(True)

    def manual_write_in36(self):
        self.ui.configuration_edit.setEnabled(True)
        self.ui.low_configuration.setEnabled(False)
        self.ui.high_configuration.setEnabled(False)

    def in36_configuration_view_right_menu(self, *args):
        right_menu = QMenu(self.ui.in36_configuration_view)

        # 设置动作
        item_1 = QAction('删除', self.ui.in36_configuration_view)
        item_1.triggered.connect(functools.partial(Page1.del_configuration, self))

        # 添加
        right_menu.addAction(item_1)

        # 显示右键菜单
        right_menu.popup(QCursor.pos())

    def del_configuration(self):
        index = self.ui.in36_configuration_view.currentIndex().row()
        if index < len(self.in36.configuration_card):
            self.in36.del_configuration(index)

        # ----------------------------- 更新页面 -----------------------------
        # 更新 in36 组态输入区
        if self.in36.configuration_card:
            df = pd.DataFrame(list(zip(*self.in36.configuration_card))[0],
                              columns=['原子序数', '原子状态', '标识符', '空格', '组态'],
                              index=list(range(1, len(self.in36.configuration_card) + 1)))
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
        else:
            self.ui.in36_configuration_view.clear()
            self.ui.in36_configuration_view.setRowCount(0)
            self.ui.in36_configuration_view.setColumnCount(3)
            self.ui.in36_configuration_view.setHorizontalHeaderLabels(
                ['原子序数', '原子状态', '标识符', '空格', '组态'])

    def run_cowan(self):
        # -------------------------- 准备工作 --------------------------
        Page1.get_in36_control_card(self, self.in36)
        Page1.get_in2_control_card(self, self.in2)
        name = '{}_{}'.format(self.atom.symbol, self.atom.ion)
        if self.exp_data_1 is None:  # 如果没有加载实验数据
            QMessageBox.warning(self, '警告', '请先加载实验数据！')
            return
        coupling_mode = self.ui.coupling_mode.currentIndex() + 1
        # -------------------------- 运行 --------------------------
        self.cowan = Cowan(self.in36, self.in2, name, self.exp_data_1, coupling_mode)
        self.cowan.run()
        self.cowan.cal_data.widen_all.delta_lambda = self.ui.offset.value()
        self.cowan.cal_data.widen_all.widen(
            temperature=25.6,
            only_p=False)
        # -------------------------- 画图 --------------------------
        self.cowan.cal_data.plot_line()
        self.cowan.cal_data.widen_all.plot_widen()
        # -------------------------- 添加到运行历史 --------------------------
        # 如果已经存在，先删除
        index = -1
        for i, cowan in enumerate(self.run_history):
            if cowan.name == self.cowan.name:
                index = i
                break
        if index != -1:
            self.run_history.pop(index)
        self.run_history.append(copy.deepcopy(self.cowan))
        # 如果存在于叠加列表中，就更新它
        for i, cowan in enumerate(self.simulate.cowan_list):
            if cowan.name == self.cowan.name:
                self.simulate.cowan_list[i] = copy.deepcopy(self.cowan)
                break

        # -------------------------- 更新页面 --------------------------
        # 将叠加谱线选择框设为可用
        self.ui.gauss.setEnabled(True)
        self.ui.crossP.setEnabled(True)
        self.ui.crossNP.setEnabled(True)
        # 更新历史记录列表
        self.ui.run_history_list.clear()
        for cowan in self.run_history:
            self.ui.run_history_list.addItem(QListWidgetItem(cowan.name))
        self.ui.run_history_list.setCurrentRow(len(self.run_history) - 1)
        # 加载线状谱
        self.ui.web_cal_line.load(QUrl.fromLocalFile(self.cowan.cal_data.plot_path))
        # 加载展宽数据
        if self.ui.crossP.isChecked():
            self.ui.web_cal_widen.load(QUrl.fromLocalFile(self.cowan.cal_data.widen_all.plot_path_cross_P))
        elif self.ui.crossNP.isChecked():
            self.ui.web_cal_widen.load(QUrl.fromLocalFile(self.cowan.cal_data.widen_all.plot_path_cross_NP))
        elif self.ui.gauss.isChecked():
            self.ui.web_cal_widen.load(QUrl.fromLocalFile(self.cowan.cal_data.widen_all.plot_path_gauss))

    def run_history_list_right_menu(self, *args):
        right_menu = QMenu(self.ui.run_history_list)

        # 设置动作
        item_1 = QAction('添加至库中', self.ui.run_history_list)
        item_1.triggered.connect(functools.partial(Page1.add_to_selection, self))
        item_2 = QAction('清空', self.ui.run_history_list)
        item_2.triggered.connect(functools.partial(Page1.clear_history, self))

        # 添加
        right_menu.addAction(item_1)
        right_menu.addAction(item_2)

        # 显示右键菜单
        right_menu.popup(QCursor.pos())

    def clear_history(self):
        self.run_history = []

        # -------------------------- 更新页面 --------------------------
        self.ui.run_history_list.clear()
        for cowan in self.run_history:
            self.ui.run_history.addItem(QListWidgetItem(cowan.name))

    def add_to_selection(self):
        index = self.ui.run_history.currentIndex().row()
        self.simulate.add_cowan(self.run_history[index])

        # -------------------------- 更新页面 --------------------------
        # 更新历史记录列表
        self.ui.run_history_list.clear()
        for cowan in self.run_history:
            self.ui.run_history.addItem(QListWidgetItem(cowan.name))
        # 更新选择列表
        self.ui.selection_list.clear()
        self.ui.page2_selection_list.clear()
        for cowan in self.simulate.cowan_list:
            self.ui.selection_list.addItem(QListWidgetItem(cowan.name))
            item = QListWidgetItem(cowan.name)
            item.setCheckState(Qt.CheckState.Checked)
            self.ui.page2_selection_list.addItem(item)

    def selection_list_right_menu(self, *args):
        right_menu = QMenu(self.ui.selection_list)

        # 设置动作
        item_1 = QAction('删除', self.ui.selection_list)
        item_1.triggered.connect(functools.partial(Page1.del_selection, self))

        # 添加
        right_menu.addAction(item_1)

        # 显示右键菜单
        right_menu.popup(QCursor.pos())

    def del_selection(self):
        index = self.ui.selection_list.currentIndex().row()
        self.simulate.cowan_list.pop(index)

        # -------------------------- 更新页面 --------------------------
        self.ui.selection_list.clear()
        self.ui.page2_selection_list.clear()
        for cowan in self.simulate.cowan_list:
            self.ui.selection_list.addItem(QListWidgetItem(cowan.name))
            item = QListWidgetItem(cowan.name)
            item.setCheckState(Qt.CheckState.Checked)
            self.ui.page2_selection_list.addItem(item)

    def load_history(self, *args):
        index = self.ui.run_history_list.currentIndex().row()
        self.cowan = copy.deepcopy(self.run_history[index])
        self.in36 = copy.deepcopy(self.cowan.in36)
        self.in2 = copy.deepcopy(self.cowan.in2)
        self.atom = copy.deepcopy(self.in36.atom)
        self.exp_data_1 = copy.deepcopy(self.cowan.exp_data)

        # -------------------------- 更新页面 --------------------------
        # ----- 原子信息 -----
        # 改变元素选择器
        self.ui.atomic_num.setCurrentIndex(self.atom.num - 1)
        self.ui.atomic_name.setCurrentIndex(self.atom.num - 1)
        self.ui.atomic_symbol.setCurrentIndex(self.atom.num - 1)
        # 改变离化度列表
        self.ui.atomic_ion.clear()
        self.ui.atomic_ion.addItems([str(i) for i in range(self.atom.num)])
        self.ui.atomic_ion.setCurrentIndex(self.atom.ion)
        # 改变基组态
        self.ui.base_configuration.setText(self.atom.base_configuration)
        # 改变下态列表
        self.ui.low_configuration.clear()
        self.ui.low_configuration.addItems(list(self.atom.electron_arrangement.keys()))
        self.ui.low_configuration.setCurrentIndex(len(self.atom.electron_arrangement.keys()) - 1)
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
        # ----- in36 -----
        # 更新in36控制卡输入区
        for i in range(23):
            eval(f'self.ui.in36_{i + 1}').setText(self.in36.control_card[i].strip(' '))
        # 更新in36组态输入区
        df = pd.DataFrame(list(zip(*self.in36.configuration_card))[0],
                          columns=['原子序数', '原子状态', '标识符', '空格', '组态'],
                          index=list(range(1, len(self.in36.configuration_card) + 1)))
        df['宇称'] = list(zip(*self.in36.configuration_card))[1]
        df = df[['宇称', '原子状态', '组态']]
        # 更新表格
        self.ui.in36_configuration_view.clear()
        self.ui.in36_configuration_view.setRowCount(df.shape[0])
        self.ui.in36_configuration_view.setColumnCount(df.shape[1])
        self.ui.in36_configuration_view.setHorizontalHeaderLabels(df.columns)
        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                item = QTableWidgetItem(str(df.iloc[i, j]))
                self.ui.in36_configuration_view.setItem(i, j, item)
        # ----- in2 -----
        in2_input_name = ['in2_1', 'in2_2', 'in2_3', 'in2_4', 'in2_5', 'in2_6', 'in2_7', 'in2_8',
                          'in2_9_a', 'in2_9_b', 'in2_9_c', 'in2_9_d',
                          'in2_10',
                          'in2_11_a', 'in2_11_b', 'in2_11_c', 'in2_11_d', 'in2_11_e',
                          'in2_12', 'in2_13', 'in2_14', 'in2_15', 'in2_16', 'in2_17', 'in2_18', 'in2_19', ]
        for i, n in enumerate(in2_input_name):
            if '11' in n:
                eval(f'self.ui.{n}').setValue(int(self.in2.input_card[i].strip(' ')))
            else:
                eval(f'self.ui.{n}').setText(self.in2.input_card[i].strip(' '))
        # ----- 实验数据 -----
        self.exp_data_1.plot_html()
        self.ui.exp_web.load(QUrl.fromLocalFile(self.exp_data_1.plot_path))
        # ----- 偏移量 -----
        self.ui.offset.setValue(self.cowan.cal_data.widen_all.delta_lambda)
        # ----- 线状谱和展宽 -----
        self.cowan.cal_data.plot_line()
        self.cowan.cal_data.widen_all.plot_widen()
        # 加载线状谱
        self.ui.web_cal_line.load(QUrl.fromLocalFile(self.cowan.cal_data.plot_path))
        # 加载展宽数据
        if self.ui.crossP.isChecked():
            self.ui.web_cal_widen.load(QUrl.fromLocalFile(self.cowan.cal_data.widen_all.plot_path_cross_P))
        elif self.ui.crossNP.isChecked():
            self.ui.web_cal_widen.load(QUrl.fromLocalFile(self.cowan.cal_data.widen_all.plot_path_cross_NP))
        elif self.ui.gauss.isChecked():
            self.ui.web_cal_widen.load(QUrl.fromLocalFile(self.cowan.cal_data.widen_all.plot_path_gauss))

    def offset_changed(self):
        self.cowan.cal_data.widen_all.delta_lambda = self.ui.offset.value()
        self.cowan.cal_data.widen_all.widen(25.6, False)
        for i, cowan in enumerate(self.run_history):
            if cowan.name == self.cowan.name:
                self.run_history[i] = copy.deepcopy(self.cowan)
                break
        # 如果存在于叠加列表中，就更新它
        for i, cowan in enumerate(self.simulate.cowan_list):
            if cowan.name == self.cowan.name:
                self.simulate.cowan_list[i] = copy.deepcopy(self.cowan)
                break

        # ------------------------- 更新界面 -------------------------
        self.cowan.cal_data.widen_all.plot_widen()
        # 加载展宽数据
        if self.ui.crossP.isChecked():
            self.ui.web_cal_widen.load(QUrl.fromLocalFile(self.cowan.cal_data.widen_all.plot_path_cross_P))
        elif self.ui.crossNP.isChecked():
            self.ui.web_cal_widen.load(QUrl.fromLocalFile(self.cowan.cal_data.widen_all.plot_path_cross_NP))
        elif self.ui.gauss.isChecked():
            self.ui.web_cal_widen.load(QUrl.fromLocalFile(self.cowan.cal_data.widen_all.plot_path_gauss))

    def get_in36_control_card(self, in36_obj: In36):
        """
        将数据存在 cowan.in36 对象中
        Returns:

        """
        v0 = '{:>1}'.format(self.ui.in36_1.text())
        v1 = '{:>1}'.format(self.ui.in36_2.text())
        v2 = '{:>1}'.format(self.ui.in36_3.text())
        v3 = '{:>2}'.format(self.ui.in36_4.text())
        v4 = '{:>1}'.format(self.ui.in36_5.text())
        v5 = '{:>2}'.format(self.ui.in36_6.text())
        v6 = '{:>2}'.format(self.ui.in36_7.text())
        v7 = '{:>3}'.format(self.ui.in36_8.text())
        v8 = '{:>2}'.format(self.ui.in36_9.text())
        v9 = '{:>5}'.format(self.ui.in36_10.text())
        v10 = '{:>10}'.format(self.ui.in36_11.text())
        v11 = '{:>10}'.format(self.ui.in36_12.text())
        v12 = '{:>2}'.format(self.ui.in36_13.text())
        v13 = '{:>2}'.format(self.ui.in36_14.text())
        v14 = '{:>1}'.format(self.ui.in36_15.text())
        v15 = '{:>1}'.format(self.ui.in36_16.text())
        v16 = '{:>2}'.format(self.ui.in36_17.text())
        v17 = '{:>2}'.format(self.ui.in36_18.text())
        v18 = '{:>5}'.format(self.ui.in36_19.text())
        v19 = '{:>5}'.format(self.ui.in36_20.text())
        v20 = '{:>5}'.format(self.ui.in36_21.text())
        v21 = '{:>5}'.format(self.ui.in36_22.text())
        v22 = '{:>5}'.format(self.ui.in36_23.text())
        temp = []
        for i in range(23):
            temp.append(eval(f'v{i}'))
        in36_obj.control_card = temp

    def get_in2_control_card(self, in2_obj: In2):
        """
        将数据存在 page1_in2 对象中
        Returns:

        """
        v0 = '{:>5}'.format(self.ui.in2_1.text())
        v1 = '{:>2}'.format(self.ui.in2_2.text())
        v2 = '{:>1}'.format(self.ui.in2_3.text())
        v3 = '{:>2}'.format(self.ui.in2_4.text())
        v4 = '{:>1}'.format(self.ui.in2_5.text())
        v5 = '{:>2}'.format(self.ui.in2_6.text())
        v6 = '{:>7}'.format(self.ui.in2_7.text())
        v7 = '{:>1}'.format(self.ui.in2_8.text())

        v8 = '{:>8}'.format(self.ui.in2_9_a.text())
        v9 = '{:>8}'.format(self.ui.in2_9_b.text())
        v10 = '{:>8}'.format(self.ui.in2_9_c.text())
        v11 = '{:>4}'.format(self.ui.in2_9_d.text())

        v12 = '{:>1}'.format(self.ui.in2_10.text())

        v13 = '{:>2}'.format(self.ui.in2_11_a.text())
        v14 = '{:>2}'.format(self.ui.in2_11_b.text())
        v15 = '{:>2}'.format(self.ui.in2_11_c.text())
        v16 = '{:>2}'.format(self.ui.in2_11_d.text())
        v17 = '{:>2}'.format(self.ui.in2_11_e.text())

        v18 = '{:>5}'.format(self.ui.in2_12.text())
        v19 = '{:>5}'.format(self.ui.in2_13.text())
        v20 = '{:>1}'.format(self.ui.in2_14.text())
        v21 = '{:>1}'.format(self.ui.in2_15.text())
        v22 = '{:>1}'.format(self.ui.in2_16.text())
        v23 = '{:>1}'.format(self.ui.in2_17.text())
        v24 = '{:>1}'.format(self.ui.in2_18.text())
        v25 = '{:>5}'.format(self.ui.in2_19.text())
        temp = []
        for i in range(26):
            temp.append(eval(f'v{i}'))
        in2_obj.input_card = temp


class Page2(MainWindow):
    def selection_list_changed(self, *args):
        for i in range(self.ui.page2_selection_list.count()):
            # 取出列表项
            item = self.ui.page2_selection_list.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                self.simulate.add_or_not[i] = True
            else:
                self.simulate.add_or_not[i] = False

    def plot_spectrum(self):
        if self.simulate.exp_data is None:
            QMessageBox.warning(self, '警告', '请先导入实验数据！')
            return
        temperature = self.ui.page2_temperature.value()
        density = self.ui.page2_density_base.value() * 10 ** self.ui.page2_density_index.value()
        self.simulate.get_simulate_data(temperature, density)
        self.simulate.plot_html()

        self.ui.page2_add_spectrum_web.load(QUrl.fromLocalFile(self.simulate.plot_path))

    def load_exp_data(self):
        path, types = QFileDialog.getOpenFileName(self, '请选择实验数据', PROJECT_PATH.as_posix(),
                                                  '数据文件(*.txt *.csv)')
        self.simulate.exp_data = [ExpData(Path(path)), Path(path)]

        # 更新界面
        self.ui.page2_exp_data_path_name.setText(Path(path).name)
