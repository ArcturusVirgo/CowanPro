import copy
import shutil
from pathlib import Path

import pandas as pd
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFileDialog, QTableWidgetItem, QDialog, QTextBrowser, QVBoxLayout

from cowan import PROJECT_PATH
from cowan.cowan import ExpData, Atom, SUBSHELL_SEQUENCE, ANGULAR_QUANTUM_NUM_NAME, In36, In2
from main import MainWindow


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
        self.page1_exp_data = ExpData(new_path)


class Page1(MainWindow):
    def atom_num_changed(self, index):
        self.page1_atom = Atom(index + 1, 0)
        Page1.update_atom_obj_about(self)

    def atom_symbol_changed(self, index):
        self.page1_atom = Atom(index + 1, 0)
        Page1.update_atom_obj_about(self)

    def atom_name_changed(self, index):
        self.page1_atom = Atom(index + 1, 0)
        Page1.update_atom_obj_about(self)

    def atom_ion_changed(self, index):
        self.page1_atom = Atom(self.page1_atom.num, index)
        Page1.update_atom_obj_about(self)

    def add_configuration(self):
        if self.page1_in36 is None:
            self.page1_in36 = In36()
            self.page1_in36.atom = copy.deepcopy(self.page1_atom)
        # 如果是自动添加
        if self.ui.auto_write_in36.isChecked():
            # 获取基组态
            low_configuration = self.page1_atom.get_configuration()
            # 获取激发组态
            self.page1_atom.arouse_electron(self.ui.low_configuration.currentText(),
                                            self.ui.high_configuration.currentText())
            high_configuration = self.page1_atom.get_configuration()
            self.page1_atom.revert_to_ground_state()

            # 添加组态
            self.page1_in36.add_configuration(low_configuration)
            self.page1_in36.add_configuration(high_configuration)
        # 如果是手动添加
        elif self.ui.manual_write_in36.isChecked():
            self.page1_in36.add_configuration(self.ui.configuration_edit.text())

        Page1.update_in36_obj_about(self)

    def load_in36(self):
        path, types = QFileDialog.getOpenFileName(self, '请选择in36文件', PROJECT_PATH.as_posix(), '')
        self.page1_in36 = In36()
        self.page1_in36.read_from_file(Path(path))

        self.page1_atom = copy.deepcopy(self.page1_in36.atom)
        Page1.update_atom_obj_about(self)
        Page1.update_in36_obj_about(self)

    def load_in2(self):
        self.page1_in2 = In2()
        path, types = QFileDialog.getOpenFileName(self, '请选择in2文件', PROJECT_PATH.as_posix(), '')
        # 更新in2对象
        self.page1_in2.read_from_file(path)
        Page1.update_in2_obj_about(self)

    def preview_in36(self):
        dialog = QDialog()
        dialog.resize(1000, 500)
        text_browser = QTextBrowser(dialog)
        dialog_layout = QVBoxLayout(dialog)

        dialog_layout.addWidget(text_browser)
        dialog.setLayout(dialog_layout)

        Page1.get_in36_control_card(self)
        in36 = self.page1_in36.get_text()

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

        Page1.get_in2_control_card(self)
        in2 = self.page1_in2.get_text()

        temp = '↓         ↓         ↓         ↓         ↓         ↓         ↓         ↓         \n'
        text_browser.setText(temp + in2)
        text_browser.setStyleSheet('font: 12pt "Consolas";')

        dialog.setWindowModality(Qt.ApplicationModal)

        dialog.exec()

    def get_in36_control_card(self):
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
        self.page1_in36.control_card = temp

    def get_in2_control_card(self):
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
        self.page1_in2.input_card = temp

    def update_atom_obj_about(self):
        # 改变元素选择器
        self.ui.atomic_num.setCurrentIndex(self.page1_atom.num - 1)
        self.ui.atomic_name.setCurrentIndex(self.page1_atom.num - 1)
        self.ui.atomic_symbol.setCurrentIndex(self.page1_atom.num - 1)
        # 改变离化度列表
        self.ui.atomic_ion.clear()
        self.ui.atomic_ion.addItems([str(i) for i in range(self.page1_atom.num)])
        self.ui.atomic_ion.setCurrentIndex(self.page1_atom.ion)
        # 改变基组态
        self.ui.base_configuration.setText(self.page1_atom.base_configuration)
        # 改变激发时的两个组态列表
        self.ui.low_configuration.clear()
        self.ui.low_configuration.addItems(list(self.page1_atom.electron_arrangement.keys()))
        self.ui.high_configuration.clear()
        temp_list = []
        for value in SUBSHELL_SEQUENCE:
            l_ = ANGULAR_QUANTUM_NUM_NAME.index(value[1])
            if value in self.page1_atom.electron_arrangement.keys():
                if self.page1_atom.electron_arrangement[value] != 4 * l_ + 2:
                    temp_list.append(value)
            else:
                temp_list.append(value)
        self.ui.high_configuration.addItems(temp_list)

    def update_in36_obj_about(self):
        # 更新左侧输入区
        for i in range(23):
            eval(f'self.ui.in36_{i + 1}').setText(self.page1_in36.control_card[i].strip(' '))
        # 更新组态
        df = pd.DataFrame(list(zip(*self.page1_in36.configuration_card))[0],
                          columns=['原子序数', '原子状态', '标识符', '空格', '组态'],
                          index=list(range(1, len(self.page1_in36.configuration_card) + 1)))
        df['宇称'] = list(zip(*self.page1_in36.configuration_card))[1]
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

    def update_in2_obj_about(self):
        in2_input_name = ['in2_1', 'in2_2', 'in2_3', 'in2_4', 'in2_5', 'in2_6', 'in2_7', 'in2_8',
                          'in2_9_a', 'in2_9_b', 'in2_9_c', 'in2_9_d',
                          'in2_10',
                          'in2_11_a', 'in2_11_b', 'in2_11_c', 'in2_11_d', 'in2_11_e',
                          'in2_12', 'in2_13', 'in2_14', 'in2_15', 'in2_16', 'in2_17', 'in2_18', 'in2_19', ]
        for i, n in enumerate(in2_input_name):
            if '11' in n:
                eval(f'self.ui.{n}').setValue(int(self.page1_in2.input_card[i].strip(' ')))
            else:
                eval(f'self.ui.{n}').setText(self.page1_in2.input_card[i].strip(' '))
