import copy
import functools
import warnings
from pathlib import Path

from matplotlib import pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QColor, QAction, QCursor, QBrush
from PySide6.QtWidgets import QFileDialog, QMessageBox, QMenu, QInputDialog, QCheckBox, QVBoxLayout, QWidget, \
    QListWidget, QPushButton, QHBoxLayout, QListWidgetItem, QTableWidgetItem, QTableWidget, QDialog, QSpinBox, \
    QHeaderView, QComboBox, QSpacerItem, QSizePolicy

from main import MainWindow
from ..Model import (
    PROJECT_PATH,
    ExpData, SimulateGrid, SimulateGridThread, SimulateSpectral,
)
from ..Tools import ProgressThread, rainbow_color
from ..View import CustomProgressDialog
from .EvolutionaryProcess import UpdateEvolutionaryProcess
from .ConfigurationContribution import UpdateConfigurationContribution


class SpectralSimulation(MainWindow):
    def selection_list_changed(self, *args):
        """
        选择列表改变时

        Args:
            *args:

        """
        for i in range(self.ui.page2_selection_list.count()):
            # 取出列表项
            item = self.ui.page2_selection_list.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                self.cowan_lists.add_or_not[i] = True
            else:
                self.cowan_lists.add_or_not[i] = False

    def load_exp_data(self):
        """
        加载实验数据

        """
        path, types = QFileDialog.getOpenFileName(self, '请选择实验数据', PROJECT_PATH().as_posix(),
                                                  '数据文件(*.txt *.csv)')
        self.expdata_2 = ExpData(Path(path))
        # 如果设置了波长范围，就使用新的波长范围
        if self.info['x_range'] is not None:
            self.expdata_2.set_xrange(self.info['x_range'])

        # -------------------------- 更新页面 --------------------------
        functools.partial(UpdateSpectralSimulation.update_page2_exp_data_path, self)()

    def plot_exp(self):
        """
        导入实验数据后，绘制实验数据

        """
        if self.expdata_2 is None:
            QMessageBox.warning(self, '警告', '请先加载实验数据！')
            return

        # -------------------------- 更新页面 --------------------------
        functools.partial(UpdateSpectralSimulation.update_exp_figure, self)()

    def plot_spectrum(self, *args):
        """
        模拟光谱，绘制实验数据和模拟数据

        Args:
            *args:

        """
        if self.expdata_2 is None:  # 如果没有导入实验数据
            QMessageBox.warning(self, '警告', '请先导入实验数据！')
            return
        if not self.cowan_lists.chose_cowan:  # 如果没有添加Cowan计算结果
            QMessageBox.warning(self, '警告', '请先添加计算结果！')
            return
        self.simulate: SimulateSpectral

        temperature = self.ui.page2_temperature.value()
        density = (self.ui.page2_density_base.value() * 10 ** self.ui.page2_density_index.value())
        self.simulate.set_exp_obj(self.expdata_2)  # 设置实验数据
        flag = self.simulate.init_cowan_list(self.cowan_lists)  # 初始化 cowan 对象
        if not flag:
            QMessageBox.warning(self, '警告', '请先设置元素比例！')
            return
        self.simulate.set_threading(False)
        self.simulate.set_temperature_and_density(temperature, density)
        self.simulate.simulate_spectral()
        self.simulate.cal_con_contribution()

        # -------------------------- 更新页面 --------------------------
        functools.partial(UpdateSpectralSimulation.update_exp_sim_figure, self)()

    def cal_grid(self):
        """
        计算网格

        """

        # 函数定义开始↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
        def update_progress_bar(progress):
            """
            更新进度条

            Args:
                progress: 进度值

            """
            progressDialog.set_label_text('计算进度：')
            progressDialog.set_value(int(progress))

        def update_ui(*args):
            """
            计算完成后的操作

            Args:
                *args:

            """
            simulated_grid_run.wait()
            simulated_grid_run.update_origin()
            self.simulate.del_cowan_list()
            # -------------------------- 更新页面 --------------------------
            functools.partial(UpdateSpectralSimulation.update_grid, self)()
            progressDialog.close()
            self.ui.page2_cal_grid.setEnabled(True)
            self.ui.statusbar.showMessage('计算完成！')

        # 函数定义完成↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

        self.simulate: SimulateSpectral
        if self.expdata_2 is None:
            QMessageBox.warning(self, '警告', '请先导入实验数据！')
            return
        if not self.cowan_lists.chose_cowan:
            QMessageBox.warning(self, '警告', '请先添加计算结果！')
            return

        # 准备阶段
        t_range = [
            self.ui.temperature_min.value(),
            self.ui.temperature_max.value(),
            self.ui.temperature_num.value()
        ]
        ne_range = [
            self.ui.density_min_base.value(),
            self.ui.density_min_index.value(),
            self.ui.density_max_base.value(),
            self.ui.density_max_index.value(),
            self.ui.density_num.value()
        ]
        self.simulate.exp_data = copy.deepcopy(self.expdata_2)
        flag = self.simulate.init_cowan_list(self.cowan_lists)
        if not flag:
            QMessageBox.warning(self, '警告', '请先设置元素比例！')
            return
        self.simulate.set_threading(True)
        self.simulated_grid = SimulateGrid(t_range, ne_range, self.simulate)
        self.simulated_grid.change_task('cal')
        simulated_grid_run = SimulateGridThread(self.simulated_grid)
        # ----界面代码
        progressDialog = CustomProgressDialog(dialog_title='正在计算...', range_=(0, 100))
        simulated_grid_run.progress.connect(update_progress_bar)
        simulated_grid_run.end.connect(update_ui)

        simulated_grid_run.start()
        progressDialog.show()
        self.ui.page2_cal_grid.setEnabled(False)

    def grid_list_clicked(self):
        """
        点击网格，加载对应温度密度的模拟光谱

        """
        item = self.ui.page2_grid_list.currentItem()
        if not item:
            return
        temperature = self.simulated_grid.t_list[item.column()]
        density = self.simulated_grid.ne_list[item.row()]
        if (temperature, density) not in self.simulated_grid.grid_data:
            warnings.warn('计算出现错误，没有该温度密度下的结果！')
            return
        self.simulate: SimulateSpectral = copy.deepcopy(self.simulated_grid.grid_data[(temperature, density)])

        # -------------------------- 更新页面 --------------------------
        temp = density.split('e+')
        self.ui.page2_temperature.setValue(eval(temperature))
        self.ui.page2_density_base.setValue(eval(temp[0]))
        self.ui.page2_density_index.setValue(int(temp[1]))
        functools.partial(UpdateSpectralSimulation.update_exp_sim_figure, self)()

    def st_resolution_recoder(self):
        """
        记录时空分辨光谱

        """
        if self.simulate.get_con_contribution() is None:
            QMessageBox.warning(self, '警告', '请再次进行模拟后再进行添加')
            return
        self.simulate: SimulateSpectral

        st_time = self.ui.st_time.text()
        st_space = (
            self.ui.st_space_x.text(),
            self.ui.st_space_y.text(),
            self.ui.st_space_z.text(),
        )
        self.space_time_resolution.add_st((st_time, st_space), self.simulate)

        # -------------------------- 更新页面 --------------------------
        # 第二页
        functools.partial(UpdateSpectralSimulation.update_space_time_table, self)()
        # 第三页
        functools.partial(UpdateEvolutionaryProcess.update_space_time_combobox, self)()
        # 第四页
        functools.partial(UpdateConfigurationContribution.update_space_time_combobox, self)()

    def load_space_time(self):
        """
        批量导入时空分辨光谱

        """
        path = QFileDialog.getExistingDirectory(
            self, '请选择实验数据所在的文件夹', PROJECT_PATH().as_posix()
        )
        path = Path(path)
        for i, file_name in enumerate(path.iterdir()):
            if 'csv' not in file_name.suffix:
                continue
            if '_' in file_name.stem:
                loc, tim = file_name.stem.split('_')
                loc = loc.strip('mm')
                tim = tim.strip('ns')
            else:
                loc = f'-{i + 1}'
                tim = f'-{i + 1}'
            self.expdata_2 = ExpData(file_name)
            if self.info['x_range'] is not None:
                self.expdata_2.set_xrange(self.info['x_range'])
            simulate = SimulateSpectral()
            simulate.set_exp_obj(ExpData(Path(file_name)))
            self.space_time_resolution.add_st((tim, (loc, '0', '0')), simulate)

        # -------------------------- 更新页面 --------------------------
        # 第二页
        functools.partial(UpdateSpectralSimulation.update_space_time_table, self)()

    def st_resolution_clicked(self, *args):
        """
        加载时空分辨光谱，更新相似度网格

        Args:
            *args:

        """

        # 函数定义开始↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
        def update_grid():
            simulated_grid_run.wait()
            progressDialog.close()
            simulated_grid_run.update_origin()
            functools.partial(UpdateSpectralSimulation.update_grid, self)()

            self.ui.statusbar.showMessage('更新网格完成！')

        # 函数定义结束↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

        index = self.ui.st_resolution_table.currentIndex().row()
        key = list(self.space_time_resolution.simulate_spectral_dict.keys())[index]
        self.simulate = copy.deepcopy(self.space_time_resolution.simulate_spectral_dict[key])
        self.expdata_2 = copy.deepcopy(self.simulate.exp_data)
        if self.simulated_grid is not None and self.ui.update_similarity.isChecked():
            self.simulated_grid.change_task('update', self.expdata_2)
            self.simulate.set_characteristic_peaks(self.simulate.characteristic_peaks)
            simulated_grid_run = SimulateGridThread(self.simulated_grid)
            progressDialog = CustomProgressDialog(dialog_title='正在更新网格...')
            progressDialog.set_label_text('正在更新网格，请稍后……')
            simulated_grid_run.up_end.connect(update_grid)
            simulated_grid_run.start()
            progressDialog.show()

        # -------------------------- 更新页面 --------------------------
        # 更新温度密度
        functools.partial(UpdateSpectralSimulation.update_temperature_density, self)()
        # 更新实验谱线路径
        functools.partial(UpdateSpectralSimulation.update_page2_exp_data_path, self)()
        # 更新时空位置
        functools.partial(UpdateSpectralSimulation.update_space_time_loc, self)(key[0], key[1][0])
        # 更新谱峰个数
        functools.partial(UpdateSpectralSimulation.update_characteristic_peaks, self)()
        if self.simulate.temperature and self.simulate.electron_density:
            functools.partial(UpdateSpectralSimulation.update_temperature_density, self)()
            functools.partial(UpdateSpectralSimulation.update_exp_sim_figure, self)()
        else:
            functools.partial(UpdateSpectralSimulation.update_exp_figure, self)()
        functools.partial(UpdateSpectralSimulation.update_space_time_table, self)()
        # 将选中的整行的背景色改为黄色
        for i in range(self.ui.st_resolution_table.columnCount()):
            self.ui.st_resolution_table.item(index, i).setBackground(QColor(255, 255, 0))

    def st_resolution_right_menu(self, *args):
        """
        时空分辨光谱右键菜单

        Args:
            *args:

        """

        def del_st_item():
            """
           删除时空分辨光谱

            """
            index = self.ui.st_resolution_table.currentIndex().row()
            key = list(self.space_time_resolution.simulate_spectral_dict.keys())[index]
            self.space_time_resolution.del_st(key)

            # -------------------------- 更新页面 --------------------------
            # 第二页
            functools.partial(UpdateSpectralSimulation.update_space_time_table, self)()
            # 第三页
            functools.partial(UpdateEvolutionaryProcess.update_space_time_combobox, self)()
            # 第四页
            functools.partial(UpdateConfigurationContribution.update_space_time_combobox, self)()

        # 函数定义结束 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        right_menu = QMenu(self.ui.st_resolution_table)

        # 设置动作
        item_1 = QAction('删除', self.ui.st_resolution_table)
        item_1.triggered.connect(del_st_item)

        # 添加
        right_menu.addAction(item_1)

        # 显示右键菜单
        right_menu.popup(QCursor.pos())

    def choose_peaks(self):
        """
        选择特征波长

        """

        def add_data():
            if self.expdata_2 is None:
                QMessageBox.warning(self, '警告', '请先导入实验数据！')
                return
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
            if not okPressed:  # 如果没有输入值，就直接返回
                dialog.activateWindow()
                update_ui()
                return
            for wave in temp_peaks_wavelength:
                if abs(wave - input_value) < 0.0001:
                    QMessageBox.warning(self, '警告', '该特征波长已存在！')
                    dialog.activateWindow()
                    update_ui()
                    return

            # 更新特征波长
            temp_peaks_wavelength.append(input_value)
            temp_peaks_wavelength.sort()
            # 更新界面
            dialog.activateWindow()
            update_ui()

        def del_data():
            temp_peaks_wavelength.pop(peaks_browser.currentRow())
            update_ui()

        def close_window():
            if len(temp_peaks_wavelength) < 2:
                QMessageBox.warning(self, '警告', '最少的峰个数是两个！')
                dialog.activateWindow()
                return
            # 更新当前对象的特征波长
            self.simulate.set_characteristic_peaks(temp_peaks_wavelength)
            # 更新网格的特征波长以及相似度
            if self.simulated_grid is not None:  # 如果网格已经计算过
                for sim in self.simulated_grid.grid_data.values():
                    sim: SimulateSpectral
                    sim.set_characteristic_peaks(temp_peaks_wavelength)
                    sim.cal_spectrum_similarity()  # 重新计算相似度
            # 更新时空分辨光谱的特征波长
            if all_changed.isChecked():
                for sim in self.space_time_resolution.simulate_spectral_dict.values():
                    sim: SimulateSpectral
                    sim.set_characteristic_peaks(temp_peaks_wavelength)
            functools.partial(UpdateSpectralSimulation.update_characteristic_peaks, self)()
            dialog.close()

        def update_ui():
            peaks_browser.clear()
            peaks_browser.addItems(['{:.4f}'.format(i) for i in temp_peaks_wavelength])

        def show_right_menu():
            right_menu.popup(QCursor.pos())  # 显示右键菜单

        def double_clicked():
            index = peaks_browser.currentRow()
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
                value=temp_peaks_wavelength[index]
            )
            if not okPressed:
                return
            temp_peaks_wavelength[index] = input_value
            temp_peaks_wavelength.sort()
            dialog.activateWindow()
            update_ui()

        # -------------------------- 主逻辑开始 --------------------------
        temp_peaks_wavelength = copy.deepcopy(self.simulate.characteristic_peaks)

        # 创建窗口元素
        dialog = QWidget()
        dialog.resize(200, 300)
        peaks_browser = QListWidget(dialog)
        peaks_browser.setContextMenuPolicy(Qt.CustomContextMenu)  # 允许使用右键菜单
        add_button = QPushButton('添加', dialog)
        close_button = QPushButton('确认', dialog)
        all_changed = QCheckBox('全部改变', dialog)
        add_button.clicked.connect(add_data)
        close_button.clicked.connect(close_window)
        peaks_browser.doubleClicked.connect(double_clicked)

        button_layout = QHBoxLayout()
        button_layout.addWidget(add_button)
        button_layout.addWidget(close_button)

        # 设置布局
        dialog_layout = QVBoxLayout(dialog)
        dialog_layout.addWidget(peaks_browser)
        dialog_layout.addWidget(all_changed)
        dialog_layout.addLayout(button_layout)
        dialog.setLayout(dialog_layout)

        # 创建右键菜单
        right_menu = QMenu(peaks_browser)
        item_1 = QAction('删除', peaks_browser)
        item_1.triggered.connect(del_data)
        right_menu.addAction(item_1)
        peaks_browser.customContextMenuRequested.connect(show_right_menu)

        update_ui()
        dialog.show()

    def show_abu(self):
        """
        显示丰度

        """

        def update_ui():
            """
            更新界面

            """
            ax.clear()
            y_list = self.simulate.abundance[combo_box.currentText()]
            x_list = [str(i) for i in range(len(y_list))]
            ax.bar(x_list, y_list)

            max_y = max(y_list)
            for x_, y_ in zip(x_list, y_list):
                ax.text(x_, y_, '{:.4f}'.format(y_), ha='center', va='bottom', fontsize=10, rotation=45)
            ax.set_ylim(0, max_y * 1.2)
            ax.set_title('${:2}$\n${:.4f}\\enspace eV \\quad and \\quad {:.4e}\\enspace cm^{{-3}}$'.format(
                combo_box.currentText(),
                *self.simulate.get_temperature_and_density()))

            canvas.draw()

        # -------------------------- 主逻辑开始 --------------------------
        if self.simulate is None:
            QMessageBox.warning(self, '警告', '请先模拟光谱！')
            return

        # 创建窗口元素
        fig = plt.figure()
        ax = fig.add_subplot(111)
        widget = QWidget()
        canvas = FigureCanvas(fig)
        combo_box = QComboBox(widget)
        combo_box.addItems(list(self.simulate.abundance.keys()))
        combo_box.currentIndexChanged.connect(update_ui)
        # 设置布局
        combo_box_layout = QHBoxLayout()
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        combo_box_layout.addItem(spacer)
        combo_box_layout.addWidget(combo_box)
        layout = QVBoxLayout(widget)
        layout.addWidget(canvas)
        layout.addLayout(combo_box_layout)

        update_ui()
        widget.show()
        widget.closeEvent = lambda x: widget.close()

    def adjust_element_ratio(self):
        def update_element_ratio(*args):
            values = {}
            for key_, spin in spin_box_dict.items():
                values[key_] = spin.value()
            if sum(values.values()) != 100:
                QMessageBox.warning(self, '警告', '元素比例之和不是100！')
                return
            self.simulate.element_ratio = values
            dialog.close()
            # -------------------------- 更新页面 --------------------------
            functools.partial(UpdateSpectralSimulation.update_element_ratio, self)()
            self.ui.statusbar.showMessage('元素比例设置成功！')

        def update_ui():
            ratio_table.setRowCount(len(element_ratio))
            ratio_table.setColumnCount(2)
            ratio_table.setHorizontalHeaderLabels(['元素', '比例'])
            ratio_table.setVerticalHeaderLabels(element_ratio.keys())
            for i_, (key_, value_) in enumerate(element_ratio.items()):
                item1 = QTableWidgetItem(key_)
                item2 = spin_box_dict[key_]
                ratio_table.setItem(i_, 0, item1)
                ratio_table.setCellWidget(i_, 1, item2)

        # -------------------------- 主逻辑开始 --------------------------
        # 获取元素比例
        element_ratio = copy.deepcopy(self.simulate.element_ratio)
        for cowan, add_or_not in self.cowan_lists:
            if cowan.in36.atom.symbol not in element_ratio:
                element_ratio[cowan.in36.atom.symbol] = 1
        if len(element_ratio) != len(self.simulate.element_ratio):
            now_count = len(element_ratio)
            single_element_percent = int(100 / now_count)
            percent = [single_element_percent for _ in range(now_count)]
            percent[-1] = 100 - single_element_percent * (now_count - 1)
            for i, (key, value) in enumerate(zip(element_ratio.keys(), percent)):
                element_ratio[key] = percent[i]
            self.simulate.element_ratio = element_ratio

        # 创建窗口元素
        dialog = QDialog()
        dialog.resize(200, 300)

        ratio_table = QTableWidget(dialog)
        ratio_table.verticalHeader().setVisible(False)  # 隐藏左侧的垂直表头
        ratio_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)  # 根据窗口大小调整列宽
        spin_box_dict = {}
        for key in element_ratio.keys():
            spin_box = QSpinBox()
            spin_box.setRange(0, 100)
            spin_box.setValue(element_ratio[key])
            spin_box_dict[key] = spin_box
        cancel_button = QPushButton('取消', dialog)
        cancel_button.clicked.connect(dialog.close)
        ok_button = QPushButton('确认', dialog)
        ok_button.clicked.connect(update_element_ratio)

        # 设置布局
        button_layout = QHBoxLayout()
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        dialog_layout = QVBoxLayout(dialog)
        dialog_layout.addWidget(ratio_table)
        dialog_layout.addLayout(button_layout)
        dialog.setLayout(dialog_layout)

        update_ui()
        dialog.exec()

    def cowan_obj_update(self):
        """
        更新 cowan 对象，重新模拟时空分辨光谱

        """

        def task():
            sum_num = len(self.space_time_resolution.simulate_spectral_dict.keys())
            progressing = 0
            for key, sim in self.space_time_resolution.simulate_spectral_dict.items():
                progressing += 1
                self.task_thread.progress.emit(int(progressing / sum_num * 100), str(key))
                if sim.temperature is None or sim.electron_density is None:
                    continue
                sim.init_cowan_list(self.cowan_lists)
                sim.simulate_spectral()
                sim.del_cowan_list()

        # 使用Qt多线程运行task
        self.task_thread = ProgressThread(dialog_title='正在应用Cowan的变化...', range_=(0, 100))
        self.task_thread.set_run(task)
        self.task_thread.progress_dialog.set_prompt_words('正在重新模拟xxx的光谱，请稍后……')
        self.task_thread.start()


class UpdateSpectralSimulation(MainWindow):
    def update_selection_list(self):
        self.ui.page2_selection_list.clear()
        for cowan, flag in self.cowan_lists:
            item = QListWidgetItem(cowan.name)
            if flag:
                item.setCheckState(Qt.CheckState.Checked)
            else:
                item.setCheckState(Qt.CheckState.Unchecked)
            self.ui.page2_selection_list.addItem(item)

    def update_page2_exp_data_path(self):
        if self.expdata_2 is None:
            warnings.warn('第二页实验数据未加载', UserWarning)
            return
        self.ui.page2_exp_data_path_name.setText(self.expdata_2.filepath.name)

    def update_space_time_loc(self, time, x_loc):
        if self.simulate is None:
            warnings.warn('simulate obj is None')
            return
        if self.simulate.temperature is None or self.simulate.electron_density is None:
            warnings.warn('simulate.temperature or simulate.electron_density is None')
            return

        self.ui.st_time.setText(str(time))
        self.ui.st_space_x.setText(str(x_loc))

    def update_exp_sim_figure(self):
        if self.simulate is None:
            warnings.warn('simulate obj is None')
            return
        if self.simulate.temperature is None or self.simulate.electron_density is None:
            warnings.warn('simulate.temperature or simulate.electron_density is None')
            return

        if self.ui.show_peaks.isChecked():
            self.simulate.plot_html(show_point=True)
        else:
            self.simulate.plot_html()
        self.ui.page2_add_spectrum_web.load(QUrl.fromLocalFile(self.simulate.plot_path))

    def update_exp_figure(self):
        if self.expdata_2 is None:
            warnings.warn('第二页实验数据未加载', UserWarning)
            return
        # 更新界面
        self.expdata_2.plot_html()
        self.ui.page2_add_spectrum_web.load(QUrl.fromLocalFile(self.expdata_2.plot_path))

    def update_grid(self):
        if self.simulated_grid is None:
            warnings.warn('simulated_grid is None')
            return
        if len(self.simulated_grid.grid_data) == 0:
            warnings.warn('simulated_grid 字典中没有 sim 对象')
            return

        self.ui.page2_grid_list.clear()
        self.ui.page2_grid_list.setRowCount(self.simulated_grid.ne_num)
        self.ui.page2_grid_list.setColumnCount(self.simulated_grid.t_num)
        self.ui.page2_grid_list.setHorizontalHeaderLabels(self.simulated_grid.t_list)
        self.ui.page2_grid_list.setVerticalHeaderLabels(self.simulated_grid.ne_list)
        # self.simulated_grid.grid_data 是一个字典
        sim_max = max(
            self.simulated_grid.grid_data.values(), key=lambda x: x.spectrum_similarity
        ).spectrum_similarity
        for t in self.simulated_grid.t_list:
            for ne in self.simulated_grid.ne_list:
                if (t, ne) not in self.simulated_grid.grid_data.keys():
                    warnings.warn(f'({t}, {ne}) not in self.simulated_grid.grid_data')
                    continue
                similarity = self.simulated_grid.grid_data[(t, ne)].spectrum_similarity
                item = QTableWidgetItem('{:.4f}'.format(similarity))
                item.setBackground(QBrush(QColor(*rainbow_color(similarity / sim_max))))
                self.ui.page2_grid_list.setItem(
                    self.simulated_grid.ne_list.index(ne),
                    self.simulated_grid.t_list.index(t),
                    item, )

    def update_space_time_table(self):
        self.ui.st_resolution_table.clear()
        self.ui.st_resolution_table.setRowCount(
            len(self.space_time_resolution.simulate_spectral_dict))
        self.ui.st_resolution_table.setColumnCount(5)
        self.ui.st_resolution_table.setHorizontalHeaderLabels(['时间', '位置', '温度', '密度', '实验谱'])
        for i, (key, value) in enumerate(self.space_time_resolution.simulate_spectral_dict.items()):
            item1 = QTableWidgetItem(key[0])
            item2 = QTableWidgetItem(f'({key[1][0]}, {key[1][1]}, {key[1][2]})')
            if '-' in key[0] and '-' in key[1][0] and key[0] == key[1][0]:
                item1.setBackground(QBrush(QColor(255, 0, 0)))
                item2.setBackground(QBrush(QColor(255, 0, 0)))
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
        if self.simulate is None:
            warnings.warn('simulate obj is None')
            return
        if self.simulate.temperature is None or self.simulate.electron_density is None:
            warnings.warn('simulate.temperature or simulate.electron_density is None')
            return

        self.ui.page2_temperature.setValue(self.simulate.temperature)
        temp = '{:.2e}'.format(self.simulate.electron_density)
        base = eval(temp.split('e+')[0])
        index = int(temp.split('e+')[1])
        self.ui.page2_density_base.setValue(base)
        self.ui.page2_density_index.setValue(index)

    def update_characteristic_peaks(self):
        if self.simulate is None:
            warnings.warn('simulate obj is None')
            return

        if self.simulate.characteristic_peaks is None:
            self.ui.peaks_label.setText('未指定')
        self.ui.peaks_label.setText(f'{len(self.simulate.characteristic_peaks)}个')
        functools.partial(UpdateSpectralSimulation.update_grid, self)()

    def update_element_ratio(self):
        text_1 = ':'.join(list(self.simulate.element_ratio.keys()))
        text_2 = ':'.join([str(int(i)) for i in self.simulate.element_ratio.values()])
        self.ui.ratio_text.setText(f'{text_1}={text_2}')

    def update_page(self):
        # ----- 选择列表 -----
        functools.partial(UpdateSpectralSimulation.update_selection_list, self)()
        # ----- 实验数据的文件名 -----
        functools.partial(UpdateSpectralSimulation.update_page2_exp_data_path, self)()
        # ----- 时空分辨光谱的时间和空间位置 -----
        functools.partial(UpdateSpectralSimulation.update_space_time_loc, self)(1, 1)
        # ----- 实验数据 -----
        functools.partial(UpdateSpectralSimulation.update_exp_figure, self)()
        # ----- 第二页的密度温度 -----
        functools.partial(UpdateSpectralSimulation.update_temperature_density, self)()
        functools.partial(UpdateSpectralSimulation.update_exp_sim_figure, self)()
        # ----- 时空分辨表格 -----
        functools.partial(UpdateSpectralSimulation.update_space_time_table, self)()
        # ----- 更新谱峰个数 -----
        functools.partial(UpdateSpectralSimulation.update_characteristic_peaks, self)()
        # 更新网格
        functools.partial(UpdateSpectralSimulation.update_grid, self)()
        # 更新元素比例
        functools.partial(UpdateSpectralSimulation.update_element_ratio, self)()
