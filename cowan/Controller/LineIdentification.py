import copy
import shutil
import warnings
import functools
from pathlib import Path

import pandas as pd
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QAction, QCursor
from PySide6.QtWidgets import QFileDialog, QDialog, QTextBrowser, QVBoxLayout, QMenu, QMessageBox, QTableWidgetItem, \
    QListWidgetItem

from main import MainWindow
from ..Model import (
    PROJECT_PATH,
    ANGULAR_QUANTUM_NUM_NAME, SUBSHELL_SEQUENCE,
    Atom, In36, In2, ExpData, Cowan, CowanThread,
)
from ..View import CustomProgressDialog

from .SpectralSimulation import UpdateSpectralSimulation
from .DataStatistics import UpdateDataStatistics


class LineIdentification(MainWindow):
    def load_exp_data(self):
        """
        第一页，加载实验数据

        Notes:
            1. 选择实验数据文件
            2. 将实验数据文件复制到项目路径下
            3. 更新实验数据范围
            4. 更新运行历史的实验数据
            5. 更新页面

        """
        path, types = QFileDialog.getOpenFileName(self, '请选择实验数据', PROJECT_PATH().as_posix(),
                                                  '数据文件(*.txt *.csv)')
        path = Path(path)
        # 将实验数据复制到项目路径下
        if 'csv' in path.name:
            new_path = PROJECT_PATH() / f'exp_data.csv'
        elif 'txt' in path.name:
            new_path = PROJECT_PATH() / f'exp_data.txt'
        else:
            raise Exception('文件格式错误')
        # 将实验数据拷贝至项目文件夹下
        try:
            shutil.copyfile(path, new_path)
        except shutil.SameFileError:
            pass

        # 更新实验数据
        self.expdata_1 = ExpData(new_path)
        if self.info['x_range'] is None:
            pass
        else:
            self.expdata_1.set_xrange(self.info['x_range'])
        # 更新运行历史的实验数据
        self.cowan_lists.update_exp_data(self.expdata_1)

        functools.partial(UpdateLineIdentification.update_exp_figure, self)()

    def redraw_exp_data(self):
        """
        重绘实验数据

        """
        functools.partial(UpdateLineIdentification.update_exp_figure, self)()

    def atom_changed(self, index):
        """
        当选择的元素改变时

        Args:
            index: 原子下拉框的序号

        """
        self.atom = Atom(index + 1, 0)
        self.in36.set_atom(self.atom)

        # ----------------------------- 更新页面 -----------------------------
        functools.partial(UpdateLineIdentification.update_atom, self)()

    def atom_ion_changed(self, index):
        """
        当离化度改变时
        Args:
            index: 离子下拉框的序号

        """
        self.atom = Atom(self.ui.atomic_num.currentIndex() + 1, index)
        self.in36.set_atom(self.atom)

        # ----------------------------- 更新页面 -----------------------------
        functools.partial(UpdateLineIdentification.update_atom_ion, self)()

    def add_configuration(self):
        """
        添加组态

        """
        # 如果是自动添加
        if self.ui.auto_write_in36.isChecked():
            # 获取基组态
            low_configuration = self.atom.get_configuration()
            # 获取激发组态
            self.atom.arouse_electron(
                self.ui.low_configuration.currentText(),
                self.ui.high_configuration.currentText(),
            )
            high_configuration = self.atom.get_configuration()
            # 将原子的状态恢复到基组态
            self.atom.revert_to_ground_state()

            # 添加组态
            self.in36.add_configuration(low_configuration)
            self.in36.add_configuration(high_configuration)
        # 如果是手动添加
        elif self.ui.manual_write_in36.isChecked():
            self.in36.add_configuration(self.ui.configuration_edit.text())

        # ----------------------------- 更新页面 -----------------------------
        functools.partial(UpdateLineIdentification.update_in36_configuration, self)()

    def load_in36(self):
        """
        加载in36文件

        """
        path, types = QFileDialog.getOpenFileName(self, '请选择in36文件', PROJECT_PATH().as_posix(), '')
        if path == '':
            return
        self.in36 = In36()
        self.in36.read_from_file(Path(path))
        self.atom = copy.deepcopy(self.in36.atom)

        # ----------------------------- 更新页面 -----------------------------
        # 更新原子信息
        functools.partial(UpdateLineIdentification.update_atom, self)()
        # 更新in36
        functools.partial(UpdateLineIdentification.update_in36, self)()

    def load_in2(self):
        """
        加载in2文件

        """
        path, types = QFileDialog.getOpenFileName(
            self, '请选择in2文件', PROJECT_PATH().as_posix(), ''
        )
        if path == '':
            return
        self.in2 = In2()
        self.in2.read_from_file(Path(path))
        # ----------------------------- 更新页面 -----------------------------
        functools.partial(UpdateLineIdentification.update_in2, self)()

    def preview_in36(self):
        """
        预览in36

        """
        dialog = QDialog()
        dialog.resize(1000, 500)
        text_browser = QTextBrowser(dialog)
        dialog_layout = QVBoxLayout(dialog)

        dialog_layout.addWidget(text_browser)
        dialog.setLayout(dialog_layout)

        LineIdentification.get_in36_control_card(self, self.in36)
        in36 = self.in36.get_text()

        temp = '↓>1       ↓>11      ↓>21      ↓>31      ↓>41      ↓>51      ↓>61      ↓>71      \n'
        text_browser.setText(temp + in36)
        text_browser.setStyleSheet('font: 12pt "Consolas";')

        dialog.setWindowModality(Qt.ApplicationModal)

        dialog.exec()

    def preview_in2(self):
        """
        预览in2

        """
        dialog = QDialog()
        dialog.resize(1000, 500)
        text_browser = QTextBrowser(dialog)
        dialog_layout = QVBoxLayout(dialog)

        dialog_layout.addWidget(text_browser)
        dialog.setLayout(dialog_layout)

        LineIdentification.get_in2_control_card(self, self.in2)
        in2 = self.in2.get_text()

        temp = '↓>1       ↓>11      ↓>21      ↓>31      ↓>41      ↓>51      ↓>61      ↓>71      \n'
        text_browser.setText(temp + in2)
        text_browser.setStyleSheet('font: 12pt "Consolas";')

        dialog.setWindowModality(Qt.ApplicationModal)

        dialog.exec()

    def configuration_move_up(self):
        """
        选中组态上移

        """
        index = self.ui.in36_configuration_view.currentIndex().row()
        if 1 <= index <= len(self.in36.configuration_card):
            self.in36.configuration_move(index, 'up')
        else:
            return

        # ----------------------------- 更新页面 -----------------------------
        # 更新 in36 组态输入区
        functools.partial(UpdateLineIdentification.update_in36_configuration, self)()
        # 调整当前选中的内容
        self.ui.in36_configuration_view.setCurrentIndex(
            self.ui.in36_configuration_view.model().index(index - 1, 0)
        )

    def configuration_move_down(self):
        """
        选中组态下移

        """
        index = self.ui.in36_configuration_view.currentIndex().row()
        if 0 <= index <= len(self.in36.configuration_card) - 2:
            self.in36.configuration_move(index, 'down')
        else:
            return

        # ----------------------------- 更新页面 -----------------------------
        # 更新 in36 组态输入区
        functools.partial(UpdateLineIdentification.update_in36_configuration, self)()
        # 调整当前选中的内容
        self.ui.in36_configuration_view.setCurrentIndex(
            self.ui.in36_configuration_view.model().index(index + 1, 0)
        )

    def in2_11_e_value_changed(self, value):
        """
        同步 in2 的斯莱特系数

        Args:
            value: 斯莱特系数 的值

        """
        self.ui.in2_11_a.setValue(value)
        self.ui.in2_11_c.setValue(value)
        self.ui.in2_11_d.setValue(value)

    def auto_write_in36(self):
        """
        自动添加组态

        """
        self.ui.high_configuration.setEnabled(True)
        self.ui.configuration_edit.setEnabled(False)
        self.ui.low_configuration.setEnabled(True)

    def manual_write_in36(self):
        """
        手动添加组态

        """
        self.ui.configuration_edit.setEnabled(True)
        self.ui.low_configuration.setEnabled(False)
        self.ui.high_configuration.setEnabled(False)

    def in36_configuration_view_right_menu(self, *args):
        """
        组态输入区右键菜单

        Args:
            *args:

        """

        def del_configuration():
            """
            删除组态

            """
            index = self.ui.in36_configuration_view.currentIndex().row()
            if index < len(self.in36.configuration_card):
                self.in36.del_configuration(index)

            # ----------------------------- 更新页面 -----------------------------
            # 更新 in36 组态输入区
            if self.in36.configuration_card:  # 如果组态卡不为空
                functools.partial(UpdateLineIdentification.update_in36_configuration, self)()
            else:  # 如果组态卡为空
                self.ui.in36_configuration_view.clear()
                self.ui.in36_configuration_view.setRowCount(0)
                self.ui.in36_configuration_view.setColumnCount(3)
                self.ui.in36_configuration_view.setHorizontalHeaderLabels(
                    ['原子序数', '原子状态', '标识符', '空格', '组态']
                )

        right_menu = QMenu(self.ui.in36_configuration_view)

        # 设置动作
        item_1 = QAction('删除', self.ui.in36_configuration_view)
        item_1.triggered.connect(del_configuration)

        # 添加
        right_menu.addAction(item_1)

        # 显示右键菜单
        right_menu.popup(QCursor.pos())

    def run_cowan(self):
        """
        运行 Cowan

        """

        def cowan_complete():
            """
            Cowan 运行完成后的操作

            """
            # 等待运行结束
            cowan_run.wait()
            # 关闭进度条
            progressDialog.close()
            # 更新原Cowan对象
            cowan_run.update_origin()
            # 设置状态栏
            self.ui.statusbar.showMessage('计算完成！正在展宽，请稍后...')

            # -------------------------- 展宽 --------------------------
            if self.info['x_range'] is None:
                self.cowan.cal_data.widen_all.widen(only_p=False)  # 整体展宽
            else:
                num = int((self.info['x_range'][1] - self.info['x_range'][0]) / self.info['x_range'][2])
                self.cowan.set_xrange(self.info['x_range'], num)
            # self.cowan.cal_data.widen_part.widen_by_group(widen_temperature)  # 部分展宽
            # -------------------------- 添加到运行历史 --------------------------
            self.cowan_lists.add_history(self.cowan)
            # -------------------------- 更新页面 --------------------------
            # 更新历史记录列表
            functools.partial(UpdateLineIdentification.update_history_list, self)()
            # 更新选择列表
            functools.partial(UpdateLineIdentification.update_selection_list, self)()
            self.ui.run_history_list.setCurrentRow(len(self.cowan_lists.cowan_run_history) - 1)  # 选中最后一项
            # 线状谱和展宽数据
            functools.partial(UpdateLineIdentification.update_line_figure, self)()
            functools.partial(UpdateLineIdentification.update_widen_figure, self)()
            self.ui.cowan_now_name.setText(f'当前展示：{self.cowan.name}')
            # 更新展宽配置
            self.ui.offset.setValue(self.cowan.cal_data.widen_all.delta_lambda)
            self.ui.widen_fwhm.setValue(self.cowan.cal_data.widen_all.fwhm_value)
            self.ui.widen_temp.setValue(25.6)

            # -------------------------- 设置状态栏 --------------------------
            self.ui.statusbar.showMessage('展宽完成！')

        def update_progress(val: str):
            """
            更新进度条

            Args:
                val: 进度值

            """
            if val == '0':
                progressDialog.set_label_text('正在计算RCN...')
                progressDialog.set_value(0)
            elif val == '25':
                progressDialog.set_label_text('正在计算RCN2...')
                progressDialog.set_value(25)
            elif val == '50':
                progressDialog.set_label_text('正在计算RCG...')
                progressDialog.set_value(50)
            elif val == '100':
                progressDialog.set_label_text('所有计算均已完成！')
                progressDialog.set_value(100)

        # -------------------------- 准备工作 --------------------------
        # 如果没有加载实验数据
        if self.expdata_1 is None:
            QMessageBox.warning(self, '警告', '请先加载实验数据！')
            return
        # 如果组态卡是空的
        if not self.in36.configuration_card:
            QMessageBox.warning(self, '警告', '请先添加组态！')
            return
        # 从界面读取in36和in2的控制卡
        LineIdentification.get_in36_control_card(self, self.in36)
        LineIdentification.get_in2_control_card(self, self.in2)
        # 获取此次运行的名称
        name = '{}_{}'.format(self.atom.symbol, self.atom.ion)
        # 获取此次运行的耦合模式
        coupling_mode = self.ui.coupling_mode.currentIndex() + 1

        # -------------------------- 运行 --------------------------
        # 运行Cowan
        self.cowan = Cowan(self.in36, self.in2, name, self.expdata_1, coupling_mode)
        cowan_run = CowanThread(self.cowan)
        # ----界面代码
        progressDialog = CustomProgressDialog(dialog_title='正在计算...', range_=(0, 100))
        cowan_run.sub_complete.connect(update_progress)  # 更新进度条
        cowan_run.all_completed.connect(cowan_complete)  # 计算完成

        # ----界面代码
        cowan_run.start()
        progressDialog.show()

    def run_history_list_right_menu(self, *args):
        """
        运行历史列表右键菜单

        Args:
            *args:

        Returns:

        """

        def clear_history():
            """
            清空历史记录

            """
            self.cowan_lists.clear_history()

            # -------------------------- 更新页面 --------------------------
            functools.partial(UpdateLineIdentification.update_history_list, self)()

        def add_to_selection():
            index = self.ui.run_history_list.currentIndex().row()
            self.cowan_lists.add_cowan(list(self.cowan_lists.cowan_run_history.values())[index].name)

            # -------------------------- 更新页面 --------------------------
            # 更新选择列表
            functools.partial(UpdateLineIdentification.update_selection_list, self)()

        # 函数定义结束 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        right_menu = QMenu(self.ui.run_history_list)

        # 设置动作
        item_1 = QAction('添加至库中', self.ui.run_history_list)
        item_1.triggered.connect(add_to_selection)
        item_2 = QAction('清空', self.ui.run_history_list)
        item_2.triggered.connect(clear_history)

        # 添加
        right_menu.addAction(item_1)
        right_menu.addAction(item_2)

        # 显示右键菜单
        right_menu.popup(QCursor.pos())

    def selection_list_right_menu(self, *args):
        """
        选择列表右键菜单

        Args:
            *args:

        """

        def del_selection():
            """
            删除选择列表中的项

            """
            index = self.ui.selection_list.currentIndex().row()
            temp_name = self.cowan_lists.chose_cowan[index]
            self.cowan_lists.del_cowan(temp_name)

            # -------------------------- 更新页面 --------------------------
            functools.partial(UpdateLineIdentification.update_selection_list, self)()

        def sort_selection():
            self.cowan_lists.sort_chose_cowan()
            functools.partial(UpdateLineIdentification.update_selection_list, self)()

        right_menu = QMenu(self.ui.selection_list)

        # 设置动作
        item_1 = QAction('删除', self.ui.selection_list)
        item_1.triggered.connect(del_selection)  # 设置动作
        item_2 = QAction('按照离化度排序', self.ui.selection_list)
        item_2.triggered.connect(sort_selection)

        # 添加
        right_menu.addAction(item_1)
        right_menu.addAction(item_2)

        # 显示右键菜单
        right_menu.popup(QCursor.pos())

    def load_history(self, *args):
        """
        双击运行历史

        Args:
            *args:

        """
        index = self.ui.run_history_list.currentIndex().row()
        self.cowan = copy.deepcopy(list(self.cowan_lists.cowan_run_history.values())[index])
        self.in36 = copy.deepcopy(self.cowan.in36)
        self.in2 = copy.deepcopy(self.cowan.in2)
        self.atom = copy.deepcopy(self.in36.atom)
        self.expdata_1 = copy.deepcopy(self.cowan.exp_data)

        # -------------------------- 更新页面 --------------------------
        self.ui.cowan_now_name.setText(f'当前展示：{self.cowan.name}')
        # ----- 原子信息 -----
        functools.partial(UpdateLineIdentification.update_atom, self)()
        # ----- in36 -----
        functools.partial(UpdateLineIdentification.update_in36, self)()
        # ----- in2 -----
        functools.partial(UpdateLineIdentification.update_in2, self)()
        # ----- 偏移量 -----
        functools.partial(UpdateLineIdentification.update_cowan_info, self)()
        # ----- 实验数据 -----
        functools.partial(UpdateLineIdentification.update_exp_figure, self)()
        # ----- 线状谱和展宽 -----
        functools.partial(UpdateLineIdentification.update_line_figure, self)()
        functools.partial(UpdateLineIdentification.update_widen_figure, self)()

    def re_widen(self):
        """
        重新展宽

        """
        self.cowan.cal_data.set_cowan_info(
            delta_lambda=self.ui.offset.value(),
            fwhm=self.ui.widen_fwhm.value(),
            temperature=self.ui.widen_temp.value()
        )
        self.cowan.cal_data.widen_all.widen(False)

        # -------------------------- 更新历史记录和选择列表 --------------------------
        self.cowan_lists.add_history(self.cowan)

        # ------------------------- 更新界面 -------------------------
        # 更新展宽后图
        functools.partial(UpdateLineIdentification.update_widen_figure, self)()
        # 更新选择列表
        functools.partial(UpdateLineIdentification.update_selection_list, self)()
        # 更新历史记录列表
        functools.partial(UpdateLineIdentification.update_history_list, self)()

    def get_in36_control_card(self, in36_obj: In36):
        """
        将数据存在 in36 对象中

        Args:
            in36_obj: in36 对象

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
        将数据存在 in2 对象中

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


class UpdateLineIdentification(MainWindow):
    def update_atom(self):
        """
        更新 元素选择器
        更新 ；离化度列表
        Returns:

        """
        # 改变元素选择器
        self.ui.atomic_num.setCurrentIndex(self.atom.num - 1)
        self.ui.atomic_name.setCurrentIndex(self.atom.num - 1)
        self.ui.atomic_symbol.setCurrentIndex(self.atom.num - 1)
        # 改变离化度列表
        self.ui.atomic_ion.clear()
        self.ui.atomic_ion.addItems([str(i) for i in range(self.atom.num)])
        self.ui.atomic_ion.setCurrentIndex(self.atom.ion)
        functools.partial(UpdateLineIdentification.update_atom_ion, self)()

    def update_atom_ion(self):
        """
        更新 元素选择区
        更新 组态选择区
        Returns:

        """
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
        if len(self.in36.configuration_card) == 0:
            warnings.warn('in36.configuration_card is None')
            return
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
        """
        更新in36控制卡输入区
        更新in36组态输入区

        Returns:

        """
        # 更新in36控制卡输入区
        functools.partial(UpdateLineIdentification.update_in36_control, self)()
        # 更新in36组态输入区
        functools.partial(UpdateLineIdentification.update_in36_configuration, self)()

    def update_in2(self):
        in2_input_name = ['in2_1', 'in2_2', 'in2_3', 'in2_4', 'in2_5', 'in2_6', 'in2_7', 'in2_8', 'in2_9_a', 'in2_9_b',
                          'in2_9_c', 'in2_9_d', 'in2_10', 'in2_11_a', 'in2_11_b', 'in2_11_c', 'in2_11_d', 'in2_11_e',
                          'in2_12', 'in2_13', 'in2_14', 'in2_15', 'in2_16', 'in2_17', 'in2_18', 'in2_19', ]
        for i, n in enumerate(in2_input_name):
            if '11' in n:
                eval(f'self.ui.{n}').setValue(int(self.in2.input_card[i].strip(' ')))
            else:
                eval(f'self.ui.{n}').setText(self.in2.input_card[i].strip(' '))

    def update_cowan_info(self):
        if self.cowan is None:
            warnings.warn('Cowan 未进行首次计算', UserWarning)
            return
        self.ui.cowan_now_name.setText(f'当前计算：{self.cowan.name}')

        if self.cowan.cal_data is None:
            warnings.warn('Cowan.cal_data 未初始化', UserWarning)
            return
        if self.cowan.cal_data.widen_all is None:  # 需要到该对象！！！
            warnings.warn('Cowan.cal_data.widen_all 未初始化', UserWarning)
            return
        self.ui.offset.setValue(self.cowan.cal_data.get_delta_lambda())
        self.ui.widen_fwhm.setValue(self.cowan.cal_data.get_fwhm())
        self.ui.widen_temp.setValue(self.cowan.cal_data.get_temperature())

    def update_history_list(self):
        self.ui.run_history_list.clear()
        for i, (name, cowan) in enumerate(self.cowan_lists.cowan_run_history.items()):
            item = QListWidgetItem(cowan.name)
            self.ui.run_history_list.addItem(item)

    def update_selection_list(self):
        self.ui.selection_list.clear()
        for cowan, flag in self.cowan_lists:
            self.ui.selection_list.addItem(QListWidgetItem(cowan.name))
        functools.partial(UpdateSpectralSimulation.update_selection_list, self)()
        functools.partial(UpdateDataStatistics.update_ion_select_combox, self)()

    def update_exp_figure(self):
        if self.expdata_1 is None:
            warnings.warn('expdata_1 is None')
            return
        self.expdata_1.plot_html()
        if self.ui.export_plot_data.text() == '关闭导出':
            self.expdata_1.export_plot_data(PROJECT_PATH() / 'plot_data/LineIdentification/exp_data.csv')
        self.ui.exp_web.load(QUrl.fromLocalFile(self.expdata_1.plot_path))

    def update_line_figure(self):
        if self.cowan is None:
            warnings.warn('Cowan未进行首次计算', UserWarning)
            return
        if self.cowan.cal_data is None:
            warnings.warn('Cowan.cal_data 未初始化', UserWarning)
            return

        self.cowan.cal_data.plot_line()
        if self.ui.export_plot_data.text() == '关闭导出':
            self.cowan.cal_data.export_plot_data(PROJECT_PATH() / 'plot_data/LineIdentification/line_data.csv')
        # 加载线状谱
        self.ui.web_cal_line.load(QUrl.fromLocalFile(self.cowan.cal_data.plot_path))

    def update_widen_figure(self):
        if self.cowan is None:
            warnings.warn('Cowan 未进行首次计算', UserWarning)
            return
        if self.cowan.cal_data is None:
            warnings.warn('Cowan.cal_data 未初始化', UserWarning)
            return
        if self.cowan.cal_data.widen_all is None:
            warnings.warn('Cowan.cal_data.widen_all 未初始化', UserWarning)
            return

        self.cowan.cal_data.widen_all.plot_widen()
        if self.ui.export_plot_data.text() == '关闭导出':
            self.cowan.cal_data.widen_all.export_plot_data(
                PROJECT_PATH() / 'plot_data/LineIdentification/widen_data.csv')

        if self.ui.crossP.isChecked():
            self.ui.web_cal_widen.load(QUrl.fromLocalFile(self.cowan.cal_data.widen_all.plot_path_cross_P))
        elif self.ui.crossNP.isChecked():
            self.ui.web_cal_widen.load(QUrl.fromLocalFile(self.cowan.cal_data.widen_all.plot_path_cross_NP))
        elif self.ui.gauss.isChecked():
            self.ui.web_cal_widen.load(QUrl.fromLocalFile(self.cowan.cal_data.widen_all.plot_path_gauss))

    def update_page(self):
        # ----- 原子信息 -----
        functools.partial(UpdateLineIdentification.update_atom, self)()
        # ----- in36 -------
        functools.partial(UpdateLineIdentification.update_in36, self)()
        # ----- in2 -----
        functools.partial(UpdateLineIdentification.update_in2, self)()
        # ----- 偏移量与半高全宽与名字 -----
        functools.partial(UpdateLineIdentification.update_cowan_info, self)()
        # ----- 实验数据画图 -----
        functools.partial(UpdateLineIdentification.update_exp_figure, self)()
        # ----- 线状谱和展宽 -----
        functools.partial(UpdateLineIdentification.update_line_figure, self)()
        functools.partial(UpdateLineIdentification.update_widen_figure, self)()
        # 更新历史记录列表
        functools.partial(UpdateLineIdentification.update_history_list, self)()
        # 更新选择列表
        functools.partial(UpdateLineIdentification.update_selection_list, self)()
