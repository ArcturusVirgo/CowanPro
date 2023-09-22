from PySide6.QtGui import QAction, QCursor
from PySide6.QtWidgets import (
    QFileDialog,
    QDialog,
    QTextBrowser,
    QVBoxLayout,
    QMenu,
    QMessageBox,
    QListWidget,
    QPushButton,
    QInputDialog,
    QHBoxLayout, QWidget,
)
from .cowan import *
from .global_var import *
from main import MainWindow, VerticalLine
from .update_ui import *


class Menu(MainWindow):
    def load_exp_data(self):
        path, types = QFileDialog.getOpenFileName(
            self, '请选择实验数据', PROJECT_PATH().as_posix(), '数据文件(*.txt *.csv)'
        )
        path = Path(path)
        # 将实验数据复制到项目路径下
        if 'csv' in path.name:
            new_path = PROJECT_PATH() / f'exp_data.csv'
        elif 'txt' in path.name:
            new_path = PROJECT_PATH() / f'exp_data.txt'
        else:
            raise Exception('文件格式错误')
        try:
            shutil.copyfile(path, new_path)
        except shutil.SameFileError:
            pass

        # 更新实验数据
        self.expdata_1 = ExpData(new_path)
        self.expdata_1.plot_html()
        # 更新页面
        self.ui.exp_web.load(QUrl.fromLocalFile(self.expdata_1.plot_path))

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
        functools.partial(UpdatePage1.update_atom, self)()

    def atom_ion_changed(self, index):
        self.atom = Atom(self.ui.atomic_num.currentIndex() + 1, index)
        self.in36 = In36(self.atom)

        # ----------------------------- 更新页面 -----------------------------
        functools.partial(UpdatePage1.update_atom_ion, self)()

    def add_configuration(self):
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
            self.atom.revert_to_ground_state()

            # 添加组态
            self.in36.add_configuration(low_configuration)
            self.in36.add_configuration(high_configuration)
        # 如果是手动添加
        elif self.ui.manual_write_in36.isChecked():
            self.in36.add_configuration(self.ui.configuration_edit.text())

        # ----------------------------- 更新页面 -----------------------------
        functools.partial(UpdatePage1.update_in36_configuration, self)()

    def load_in36(self):
        path, types = QFileDialog.getOpenFileName(
            self, '请选择in36文件', PROJECT_PATH().as_posix(), ''
        )
        if path == '':
            return
        self.in36.read_from_file(Path(path))
        self.atom = copy.deepcopy(self.in36.atom)

        # ----------------------------- 更新页面 -----------------------------
        # 更新原子信息
        functools.partial(UpdatePage1.update_atom, self)()
        # 更新in36
        functools.partial(UpdatePage1.update_in36, self)()

    def load_in2(self):
        path, types = QFileDialog.getOpenFileName(
            self, '请选择in2文件', PROJECT_PATH().as_posix(), ''
        )
        if path == '':
            return
        self.in2.read_from_file(path)
        # ----------------------------- 更新页面 -----------------------------
        functools.partial(UpdatePage1.update_in2, self)()

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
        else:
            return

        # ----------------------------- 更新页面 -----------------------------
        # 更新 in36 组态输入区
        functools.partial(UpdatePage1.update_in36_configuration, self)()
        # 调整当前显示的内容
        self.ui.in36_configuration_view.setCurrentIndex(
            self.ui.in36_configuration_view.model().index(index - 1, 0)
        )

    def configuration_move_down(self):
        index = self.ui.in36_configuration_view.currentIndex().row()
        if 0 <= index <= len(self.in36.configuration_card) - 2:
            self.in36.configuration_move(index, 'down')
        else:
            return

        # ----------------------------- 更新页面 -----------------------------
        # 更新 in36 组态输入区
        functools.partial(UpdatePage1.update_in36_configuration, self)()
        # 调整当前显示的内容
        self.ui.in36_configuration_view.setCurrentIndex(
            self.ui.in36_configuration_view.model().index(index + 1, 0)
        )

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
        if self.in36.configuration_card:  # 如果组态卡不为空
            functools.partial(UpdatePage1.update_in36_configuration, self)()
        else:  # 如果组态卡为空
            self.ui.in36_configuration_view.clear()
            self.ui.in36_configuration_view.setRowCount(0)
            self.ui.in36_configuration_view.setColumnCount(3)
            self.ui.in36_configuration_view.setHorizontalHeaderLabels(
                ['原子序数', '原子状态', '标识符', '空格', '组态']
            )

    def run_cowan(self):
        # -------------------------- 准备工作 --------------------------
        Page1.get_in36_control_card(self, self.in36)
        Page1.get_in2_control_card(self, self.in2)
        name = '{}_{}'.format(self.atom.symbol, self.atom.ion)
        if self.expdata_1 is None:  # 如果没有加载实验数据
            QMessageBox.warning(self, '警告', '请先加载实验数据！')
            return
        coupling_mode = self.ui.coupling_mode.currentIndex() + 1
        # -------------------------- 运行 --------------------------
        self.cowan = Cowan(self.in36, self.in2, name, self.expdata_1, coupling_mode)
        self.cowan.run()
        self.cowan.cal_data.widen_all.delta_lambda = self.ui.offset.value()
        self.cowan.cal_data.widen_part.delta_lambda = self.ui.offset.value()
        self.cowan.cal_data.widen_all.fwhmgauss = lambda x: self.ui.widen_fwhm.value()
        widen_temperature = self.ui.widen_temp.value()
        self.cowan.cal_data.widen_all.widen(temperature=widen_temperature, only_p=False)
        self.cowan.cal_data.widen_part.widen_by_group(temperature=widen_temperature)
        # -------------------------- 画图 --------------------------
        self.cowan.cal_data.plot_line()
        self.cowan.cal_data.widen_all.plot_widen()
        self.cowan.cal_data.widen_part.plot_widen_by_group()
        # -------------------------- 添加到运行历史 --------------------------
        # 如果已经存在，先删除
        index = -1
        for i, cowan_ in enumerate(self.run_history):
            if cowan_.name == self.cowan.name:
                index = i
                break
        if index != -1:
            self.run_history.pop(index)
        self.run_history.append(copy.deepcopy(self.cowan))
        # 如果存在于叠加列表中，就更新它
        for i, cowan_ in enumerate(self.simulate.cowan_list):
            if cowan_.name == self.cowan.name:
                self.simulate.cowan_list[i] = copy.deepcopy(self.cowan)
                break

        # -------------------------- 更新页面 --------------------------
        # 将叠加谱线选择框设为可用
        self.ui.gauss.setEnabled(True)
        self.ui.crossP.setEnabled(True)
        self.ui.crossNP.setEnabled(True)
        # 更新历史记录列表
        functools.partial(UpdatePage1.update_history_list, self)()
        self.ui.run_history_list.setCurrentRow(len(self.run_history) - 1)  # 选中最后一项
        # 线状谱和展宽数据
        functools.partial(UpdatePage1.update_line_figure, self)()
        functools.partial(UpdatePage1.update_widen_figure, self)()

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
        functools.partial(UpdatePage1.update_history_list, self)()

    def add_to_selection(self):
        index = self.ui.run_history_list.currentIndex().row()
        self.simulate.add_cowan(self.run_history[index])

        # -------------------------- 更新页面 --------------------------
        # 更新选择列表
        functools.partial(UpdatePage1.update_selection_list, self)()

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
        functools.partial(UpdatePage1.update_selection_list, self)()

    def load_history(self, *args):
        index = self.ui.run_history_list.currentIndex().row()
        self.cowan = copy.deepcopy(self.run_history[index])
        self.in36 = copy.deepcopy(self.cowan.in36)
        self.in2 = copy.deepcopy(self.cowan.in2)
        self.atom = copy.deepcopy(self.in36.atom)
        self.expdata_1 = copy.deepcopy(self.cowan.exp_data)

        # -------------------------- 更新页面 --------------------------
        # ----- 原子信息 -----
        functools.partial(UpdatePage1.update_atom, self)()
        # ----- in36 -----
        functools.partial(UpdatePage1.update_in36, self)()
        # ----- in2 -----
        functools.partial(UpdatePage1.update_in2, self)()
        # ----- 偏移量 -----
        self.ui.offset.setValue(self.cowan.cal_data.widen_all.delta_lambda)
        # ----- 实验数据 -----
        functools.partial(UpdatePage1.update_exp_figure, self)()
        # ----- 线状谱和展宽 -----
        functools.partial(UpdatePage1.update_line_figure, self)()
        functools.partial(UpdatePage1.update_widen_figure, self)()

    def re_widen(self):
        self.cowan.cal_data.widen_all.delta_lambda = self.ui.offset.value()
        self.cowan.cal_data.widen_part.delta_lambda = self.ui.offset.value()
        self.cowan.cal_data.widen_all.fwhmgauss = lambda x: self.ui.widen_fwhm.value()
        widen_temperature = self.ui.widen_temp.value()
        self.cowan.cal_data.widen_all.widen(widen_temperature, False)
        self.cowan.cal_data.widen_part.widen_by_group(temperature=widen_temperature)
        for i, cowan_ in enumerate(self.run_history):
            if cowan_.name == self.cowan.name:
                self.run_history[i] = copy.deepcopy(self.cowan)
                break
        # 如果存在于叠加列表中，就更新它
        for i, cowan_ in enumerate(self.simulate.cowan_list):
            if cowan_.name == self.cowan.name:
                self.simulate.cowan_list[i] = copy.deepcopy(self.cowan)
                break

        # ------------------------- 更新界面 -------------------------
        functools.partial(UpdatePage1.update_widen_figure, self)()

    def get_in36_control_card(self, in36_obj: In36):
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

    def plot_spectrum(self, *args):
        if self.expdata_2 is None:
            QMessageBox.warning(self, '警告', '请先导入实验数据！')
            return
        else:
            self.simulate.exp_data = copy.deepcopy(self.expdata_2)
        temperature = self.ui.page2_temperature.value()
        density = (
                self.ui.page2_density_base.value()
                * 10 ** self.ui.page2_density_index.value()
        )
        self.simulate.get_simulate_data(temperature, density)

        # -------------------------- 更新页面 --------------------------
        functools.partial(UpdatePage2.update_exp_sim_figure, self)()

    def load_exp_data(self):
        path, types = QFileDialog.getOpenFileName(
            self, '请选择实验数据', PROJECT_PATH().as_posix(), '数据文件(*.txt *.csv)'
        )
        self.expdata_2 = ExpData(Path(path))

        # -------------------------- 更新页面 --------------------------
        self.ui.page2_exp_data_path_name.setText(self.expdata_2.filepath.name)

    def cal_grid(self):
        # 函数定义开始↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
        def update_progress_bar(progress):
            self.ui.page2_progressBar.setValue(int(progress))

        def update_ui(*args):
            # -------------------------- 更新页面 --------------------------
            functools.partial(UpdatePage2.update_grid, self)()
            self.ui.page2_cal_grid.setDisabled(False)

        # 函数定义完成↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

        if self.expdata_2 is None:
            QMessageBox.warning(self, '警告', '请先导入实验数据！')
            return
        else:
            self.simulate.exp_data = copy.deepcopy(self.expdata_2)
        t_range = [
            self.ui.temperature_min.value(),
            self.ui.temperature_max.value(),
            self.ui.temperature_num.value(),
        ]
        ne_range = [
            self.ui.density_min_base.value(),
            self.ui.density_min_index.value(),
            self.ui.density_max_base.value(),
            self.ui.density_max_index.value(),
            self.ui.density_num.value(),
        ]
        self.ui.page2_cal_grid.setDisabled(True)
        self.ui.page2_progressBar.setRange(0, t_range[2] * ne_range[4])
        self.simulated_grid = SimulateGrid(t_range, ne_range, self.simulate)
        self.simulated_grid.change_task('cal')
        self.simulated_grid.start()
        self.simulated_grid.end.connect(update_ui)
        self.simulated_grid.progress.connect(update_progress_bar)

    def grid_list_clicked(self):
        item = self.ui.page2_grid_list.currentItem()
        if not item:
            return
        temperature = self.simulated_grid.t_list[item.column()]
        density = self.simulated_grid.ne_list[item.row()]
        self.simulate = copy.deepcopy(
            self.simulated_grid.grid_data[(temperature, density)]
        )

        # -------------------------- 更新页面 --------------------------
        temp = density.split('e+')
        self.ui.page2_temperature.setValue(eval(temperature))
        self.ui.page2_density_base.setValue(eval(temp[0]))
        self.ui.page2_density_index.setValue(int(temp[1]))
        functools.partial(UpdatePage2.update_exp_sim_figure, self)()

    def st_resolution_recoder(self):
        st_time = self.ui.st_time.text()
        st_space = (
            self.ui.st_space_x.text(),
            self.ui.st_space_y.text(),
            self.ui.st_space_z.text(),
        )
        if self.expdata_2 is None:
            QMessageBox.warning(self, '警告', '请先确定温度和密度！')
            return
        else:
            self.simulate.exp_data = copy.deepcopy(self.expdata_2)
        self.space_time_resolution.add_st((st_time, st_space), self.simulate)

        # -------------------------- 更新页面 --------------------------
        # 第二页
        functools.partial(UpdatePage2.update_space_time_table, self)()
        # 第三页
        functools.partial(UpdatePage3.update_space_time_combobox, self)()
        # 第四页
        functools.partial(UpdatePage4.update_space_time_combobox, self)()

    def plot_exp(self):
        if self.expdata_2 is None:
            QMessageBox.warning(self, '警告', '请先加载实验数据！')
            return

        # -------------------------- 更新页面 --------------------------
        functools.partial(UpdatePage2.update_exp_figure, self)()

    def load_space_time(self):
        path = QFileDialog.getExistingDirectory(
            self, '请选择实验数据所在的文件夹', PROJECT_PATH().as_posix()
        )
        path = Path(path)
        for file_name in path.iterdir():
            loc, tim = file_name.stem.split('_')
            loc = loc.strip('mm')
            tim = tim.strip('ns')
            self.expdata_2 = ExpData(file_name)
            self.simulate.temperature = None
            self.simulate.electron_density = None
            self.simulate.exp_data = copy.deepcopy(self.expdata_2)
            self.space_time_resolution.add_st((tim, (loc, '0', '0')), self.simulate)

        # -------------------------- 更新页面 --------------------------
        # 第二页
        functools.partial(UpdatePage2.update_space_time_table, self)()
        # 第三页
        functools.partial(UpdatePage3.update_space_time_combobox, self)()
        # 第四页
        functools.partial(UpdatePage4.update_space_time_combobox, self)()

    def st_resolution_double_clicked(self, *args):
        # 函数定义开始↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
        def update_grid():
            functools.partial(UpdatePage2.update_grid, self)()
            self.ui.page2_cal_grid.setDisabled(False)
            self.ui.statusbar.showMessage('网格更新完成！')

        # 函数定义结束↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

        index = self.ui.st_resolution_table.currentIndex().row()
        key = list(self.space_time_resolution.simulate_spectral_dict.keys())[index]
        self.simulate = copy.deepcopy(
            self.space_time_resolution.simulate_spectral_dict[key]
        )
        self.expdata_2 = copy.deepcopy(self.simulate.exp_data)
        if self.simulated_grid is not None:
            self.ui.statusbar.showMessage('正在更新网格，请稍后……')
            # QMetaObject.invokeMethod(self.simulated_grid, 'update_similarity')
            self.simulated_grid.change_task('update', self.expdata_2)
            self.simulated_grid.start()
            self.simulated_grid.up_end.connect(update_grid)

        # -------------------------- 更新页面 --------------------------
        self.ui.st_time.setText(key[0])
        self.ui.st_space_x.setText(key[1][0])
        self.ui.page2_exp_data_path_name.setText(self.expdata_2.filepath.name)
        if self.simulate.temperature and self.simulate.electron_density:
            functools.partial(UpdatePage2.update_temperature_density, self)()
            functools.partial(UpdatePage2.update_exp_sim_figure, self)()
        else:
            functools.partial(UpdatePage2.update_exp_figure, self)()

    def choose_peaks(self):
        def add_data():
            if self.simulate is None or self.simulate.exp_data is None:
                minValue = 0
                maxValue = 10
            else:
                minValue = self.simulate.exp_data.x_range[0]
                maxValue = self.simulate.exp_data.x_range[1]
            input_value, okPressed = QInputDialog.getDouble(
                self,
                "请输入",
                "特征波长",
                decimals=3,
                step=0.002,
                maxValue=maxValue,
                minValue=minValue,
            )
            if not okPressed:
                return
            for wave in self.simulate.characteristic_peaks:
                if abs(wave - input_value) < 0.0001:
                    QMessageBox.warning(self, '警告', '该特征波长已存在！')
                    return
            self.simulate.characteristic_peaks.append(input_value)
            self.simulate.characteristic_peaks.sort()
            update_ui()

        def del_data():
            self.simulate.characteristic_peaks.pop(peaks_browser.currentRow())
            update_ui()

        def close_window():
            dialog.close()

        def update_ui():
            peaks_browser.clear()
            peaks_browser.addItems(['{:.4f}'.format(i) for i in self.simulate.characteristic_peaks])

        def show_right_menu():
            right_menu.popup(QCursor.pos())  # 显示右键菜单

        # 创建窗口元素
        dialog = QDialog()
        dialog.resize(200, 300)
        dialog.setWindowModality(Qt.ApplicationModal)
        peaks_browser = QListWidget(dialog)
        peaks_browser.setContextMenuPolicy(Qt.CustomContextMenu)  # 允许使用右键菜单
        add_button = QPushButton('添加', dialog)
        close_button = QPushButton('关闭', dialog)
        add_button.clicked.connect(add_data)
        close_button.clicked.connect(close_window)
        button_layout = QHBoxLayout()
        button_layout.addWidget(add_button)
        button_layout.addWidget(close_button)

        # 设置布局
        dialog_layout = QVBoxLayout(dialog)
        dialog_layout.addWidget(peaks_browser)
        dialog_layout.addLayout(button_layout)
        dialog.setLayout(dialog_layout)

        # 创建右键菜单
        right_menu = QMenu(peaks_browser)
        item_1 = QAction('删除', peaks_browser)
        item_1.triggered.connect(del_data)
        right_menu.addAction(item_1)
        peaks_browser.customContextMenuRequested.connect(show_right_menu)

        update_ui()
        dialog.exec()
        functools.partial(UpdatePage2.update_characteristic_peaks, self)()


class Page3(MainWindow):
    def plot_by_times(self):
        temp = self.ui.location_select.currentText().strip('(').strip(')')
        x, y, z = temp.split(',')
        x, y, z = x.strip(), y.strip(), z.strip()

        self.space_time_resolution.plot_change_by_time((x, y, z))
        self.ui.webEngineView_3.load(
            QUrl.fromLocalFile(self.space_time_resolution.change_by_time_path)
        )

    def plot_by_locations(self):
        t = self.ui.time_select.currentText()

        self.space_time_resolution.plot_change_by_location(t)
        self.ui.webEngineView_4.load(
            QUrl.fromLocalFile(self.space_time_resolution.change_by_location_path)
        )

    def plot_by_space_time(self):
        variable_index = self.ui.variable_select.currentIndex()

        self.space_time_resolution.plot_change_by_space_time(variable_index)
        self.ui.webEngineView_5.load(
            QUrl.fromLocalFile(self.space_time_resolution.change_by_space_time_path)
        )


class Page4(MainWindow):
    def comboBox_changed(self, index):
        # 设置树状列表
        self.ui.treeWidget.clear()
        self.simulate_page4: SimulateSpectral = copy.deepcopy(
            list(self.space_time_resolution.simulate_spectral_dict.values())[index]
        )
        # -------------------------- 更新页面 --------------------------
        functools.partial(UpdatePage4.update_treeview, self)()
        functools.partial(UpdatePage4.update_exp_figure, self)()

    def plot_example(self):
        add_example = []
        for i in range(self.ui.treeWidget.topLevelItemCount()):
            parent = self.ui.treeWidget.topLevelItem(i)
            if parent.checkState(0) == Qt.Checked:
                add_example.append([True, []])
            else:
                add_example.append([False, []])
            for j in range(parent.childCount()):
                child = parent.child(j)
                if child.checkState(0) == Qt.Checked:
                    add_example[i][1].append(True)
                else:
                    add_example[i][1].append(False)

        self.simulate_page4.plot_example_html(add_example)
        self.ui.webEngineView_2.load(
            QUrl.fromLocalFile(self.simulate_page4.example_path)
        )

    @staticmethod
    def tree_item_changed(self, item, column):
        if item.checkState(0) == Qt.Checked:
            for i in range(item.childCount()):
                item.child(i).setCheckState(0, Qt.Checked)
        else:
            for i in range(item.childCount()):
                item.child(i).setCheckState(0, Qt.Unchecked)
