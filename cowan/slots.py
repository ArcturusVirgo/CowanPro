from PySide6.QtGui import QAction, QCursor
from PySide6.QtWebEngineCore import QWebEngineSettings, QWebEnginePage
from PySide6.QtWidgets import QFileDialog, QDialog, QTextBrowser, QMenu, QMessageBox, QListWidget, QPushButton, \
    QInputDialog, QHBoxLayout, QCheckBox, QDoubleSpinBox

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from .tools import get_configuration_add_list
from .cowan import *
from .global_var import *
from main import VerticalLine, MainWindow
from .update_ui import *


class Menu(MainWindow):
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
            self.expdata_1.set_range(self.info['x_range'])
        # 更新运行历史的实验数据
        self.cowan_lists.update_exp_data(self.expdata_1)
        self.expdata_1.plot_html()
        # 更新页面
        self.ui.exp_web.load(QUrl.fromLocalFile(self.expdata_1.plot_path))

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

    def set_xrange(self):
        """
        设置波长范围

        """

        def update_xrange():
            def task():
                self.task_thread.progress.emit(0, '准备开始')
                x_range = [min_input.value(), max_input.value()]
                widen_temperature = self.ui.widen_temp.value()
                self.info['x_range'] = x_range
                # 设置第一页的实验谱线
                self.task_thread.progress.emit(10, '设置第一页的实验谱线')
                self.expdata_1.set_range(x_range)
                # 设置 页面上的 Cowan
                self.task_thread.progress.emit(20, '重新展宽页面上的Cowan')
                if self.cowan is not None:
                    # 设置范围
                    self.cowan.exp_data.set_range(x_range)
                    self.cowan.cal_data.widen_all.exp_data.set_range(x_range)
                    self.cowan.cal_data.widen_part.exp_data.set_range(x_range)
                    # 重新展宽
                    self.cowan.cal_data.widen_all.widen(widen_temperature, False)
                # 设置各个 Cowan
                for i, (cowan_, _) in enumerate(self.cowan_lists):
                    self.task_thread.progress.emit(20 + int(i / len(self.cowan_lists.chose_cowan) * 40),
                                                   f'重新展宽{cowan_.name}')
                    # 设置范围
                    cowan_.exp_data.set_range(x_range)
                    cowan_.cal_data.widen_all.exp_data.set_range(x_range)
                    cowan_.cal_data.widen_part.exp_data.set_range(x_range)
                    # 更新展宽参数
                    num = int((x_range[1] - x_range[0]) / (
                        min(self.expdata_1.data['wavelength'].values[1:] - self.expdata_1.data['wavelength'].values[
                                                                           :-1])))
                    cowan_.cal_data.widen_all.n = num
                    cowan_.cal_data.widen_part.n = num
                    # 重新展宽
                    cowan_.cal_data.widen_all.widen(widen_temperature, False)
                # 设置第二页的实验谱线
                self.task_thread.progress.emit(60, '设置第二页的实验谱线')
                if self.expdata_2 is not None:
                    self.expdata_2.set_range(x_range)
                # 设置叠加谱线
                self.task_thread.progress.emit(65, '重新模拟当前光谱')
                if self.simulate is not None:
                    self.simulate.exp_data.set_range(x_range)
                    # 重新模拟
                    self.simulate.init_cowan_list(self.cowan_lists)
                    temperature = self.ui.page2_temperature.value()
                    density = (self.ui.page2_density_base.value() * 10 ** self.ui.page2_density_index.value())
                    self.simulate.get_simulate_data(temperature, density)
                    self.simulate.del_cowan_list()
                # 设置实验叠加谱线
                for i, (key, sim) in enumerate(self.space_time_resolution.simulate_spectral_dict.items()):
                    self.task_thread.progress.emit(
                        65 + int(i / len(self.space_time_resolution.simulate_spectral_dict) * 35),
                        f'重新模拟{key[0]}_{key[1][0]}的光谱')
                    # 设置范围
                    sim.exp_data.set_range(x_range)
                    # 重新模拟
                    if sim.temperature is None or sim.electron_density is None:
                        continue
                    sim.init_cowan_list(self.cowan_lists)
                    sim.get_simulate_data(sim.temperature, sim.electron_density)
                    sim.del_cowan_list()

                self.ui.statusbar.showMessage('设置范围成功！')

            dialog.close()
            self.task_thread = ProgressThread(dialog_title='正在设置范围...', range_=(0, 100))
            self.task_thread.set_run(task)
            self.task_thread.start()

        if self.expdata_1 is None:
            QMessageBox.warning(self.ui, '警告', '实验数据未加载！')
            return
        dialog = QDialog()
        label = QLabel('请输入范围：')
        min_input = QDoubleSpinBox()
        max_input = QDoubleSpinBox()
        layout_input = QHBoxLayout()
        layout_input.addWidget(min_input)
        layout_input.addWidget(max_input)
        ok_btn = QPushButton('确认')
        cancel_btn = QPushButton('取消')
        min_input.setValue(self.expdata_1.init_xrange[0])
        max_input.setValue(self.expdata_1.init_xrange[1])
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
            self.info['x_range'] = None
            widen_temperature = self.ui.widen_temp.value()
            # 设置第一页的实验谱线
            self.task_thread.progress.emit(10, '设置第一页的实验谱线')
            self.expdata_1.reset_range()
            # functools.partial(UpdatePage1.update_exp_figure, self)()
            # 设置 页面上的 Cowan
            self.task_thread.progress.emit(20, '重新展宽页面上的Cowan')
            if self.cowan is not None:
                # 设置范围
                self.cowan.exp_data.reset_range()
                self.cowan.cal_data.widen_all.exp_data.reset_range()
                self.cowan.cal_data.widen_part.exp_data.reset_range()
                # 重新展宽
                self.cowan.cal_data.widen_all.widen(widen_temperature, False)
            # 设置各个 Cowan
            for i, (cowan_, _) in enumerate(self.cowan_lists):
                self.task_thread.progress.emit(20 + int(i / len(self.cowan_lists.chose_cowan) * 40),
                                               f'重新展宽{cowan_.name}')
                # 设置范围
                cowan_.exp_data.reset_range()
                cowan_.cal_data.widen_all.exp_data.reset_range()
                cowan_.cal_data.widen_part.exp_data.reset_range()
                # 更新展宽参数
                cowan_.cal_data.widen_all.n = None
                cowan_.cal_data.widen_part.n = None
                # 重新展宽
                cowan_.cal_data.widen_all.widen(widen_temperature, False)
            # 设置第二页的实验谱线
            self.task_thread.progress.emit(65, '设置第二页的实验谱线')
            if self.expdata_2 is not None:
                self.expdata_2.reset_range()
                # functools.partial(UpdatePage2.update_exp_figure, self)()
            # 设置叠加谱线
            self.task_thread.progress.emit(65, '重新模拟当前光谱')
            if self.simulate is not None:
                self.simulate.exp_data.reset_range()
                # 重新模拟
                self.simulate.init_cowan_list(self.cowan_lists)
                temperature = self.ui.page2_temperature.value()
                density = (self.ui.page2_density_base.value() * 10 ** self.ui.page2_density_index.value())
                self.simulate.get_simulate_data(temperature, density)
                self.simulate.del_cowan_list()
            # 设置实验叠加谱线
            for i, (key, sim) in enumerate(self.space_time_resolution.simulate_spectral_dict.items()):
                self.task_thread.progress.emit(
                    65 + int(i / len(self.space_time_resolution.simulate_spectral_dict) * 35),
                    f'重新模拟{key[0]}_{key[1][0]}的光谱')
                # 设置范围
                sim.exp_data.reset_range()
                # 重新模拟
                if sim.temperature is None or sim.electron_density is None:
                    continue
                sim.init_cowan_list(self.cowan_lists)
                sim.get_simulate_data(sim.temperature, sim.electron_density)
                sim.del_cowan_list()

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
            data_frames[self.cowan.name] = (
                pd.DataFrame({names[0]: temp_1, names[1]: temp_2, names[2]: temp_3, names[3]: temp_4}))
            # 存储
            with pd.ExcelWriter('组态平均波长.xlsx', ) as writer:
                for key, value in data_frames.items():
                    value.to_excel(writer, sheet_name=key, index=False)
        self.ui.statusbar.showMessage('导出成功！')


class Page1(MainWindow):
    def atom_changed(self, index):
        """
        当选择的元素改变时

        Args:
            index: 原子下拉框的序号

        """
        self.atom = Atom(index + 1, 0)
        self.in36.set_atom(self.atom)

        # ----------------------------- 更新页面 -----------------------------
        functools.partial(UpdatePage1.update_atom, self)()

    def atom_ion_changed(self, index):
        """
        当离化度改变时
        Args:
            index: 离子下拉框的序号

        """
        self.atom = Atom(self.ui.atomic_num.currentIndex() + 1, index)
        self.in36.set_atom(self.atom)

        # ----------------------------- 更新页面 -----------------------------
        functools.partial(UpdatePage1.update_atom_ion, self)()

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
        functools.partial(UpdatePage1.update_in36_configuration, self)()

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
        functools.partial(UpdatePage1.update_atom, self)()
        # 更新in36
        functools.partial(UpdatePage1.update_in36, self)()

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
        functools.partial(UpdatePage1.update_in2, self)()

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

        Page1.get_in36_control_card(self, self.in36)
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

        Page1.get_in2_control_card(self, self.in2)
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
        functools.partial(UpdatePage1.update_in36_configuration, self)()
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
        functools.partial(UpdatePage1.update_in36_configuration, self)()
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
                functools.partial(UpdatePage1.update_in36_configuration, self)()
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
            self.cowan.cal_data.widen_all.widen(temperature=25.6, only_p=False)  # 整体展宽
            # self.cowan.cal_data.widen_part.widen_by_group(widen_temperature)  # 部分展宽
            # -------------------------- 添加到运行历史 --------------------------
            self.cowan_lists.add_history(self.cowan)
            # -------------------------- 更新页面 --------------------------
            # 更新历史记录列表
            functools.partial(UpdatePage1.update_history_list, self)()
            # 更新选择列表
            functools.partial(UpdatePage1.update_selection_list, self)()
            self.ui.run_history_list.setCurrentRow(len(self.cowan_lists.cowan_run_history) - 1)  # 选中最后一项
            # 线状谱和展宽数据
            functools.partial(UpdatePage1.update_line_figure, self)()
            functools.partial(UpdatePage1.update_widen_figure, self)()
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
        Page1.get_in36_control_card(self, self.in36)
        Page1.get_in2_control_card(self, self.in2)
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
            functools.partial(UpdatePage1.update_history_list, self)()

        def add_to_selection():
            index = self.ui.run_history_list.currentIndex().row()
            self.cowan_lists.add_cowan(list(self.cowan_lists.cowan_run_history.values())[index].name)

            # -------------------------- 更新页面 --------------------------
            # 更新选择列表
            functools.partial(UpdatePage1.update_selection_list, self)()

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
            self.cowan_lists.del_cowan(index)

            # -------------------------- 更新页面 --------------------------
            functools.partial(UpdatePage1.update_selection_list, self)()

        right_menu = QMenu(self.ui.selection_list)

        # 设置动作
        item_1 = QAction('删除', self.ui.selection_list)
        item_1.triggered.connect(del_selection)

        # 添加
        right_menu.addAction(item_1)

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
        functools.partial(UpdatePage1.update_atom, self)()
        # ----- in36 -----
        functools.partial(UpdatePage1.update_in36, self)()
        # ----- in2 -----
        functools.partial(UpdatePage1.update_in2, self)()
        # ----- 偏移量 -----
        self.ui.offset.setValue(self.cowan.cal_data.widen_all.delta_lambda)
        self.ui.widen_fwhm.setValue(self.cowan.cal_data.widen_all.fwhm_value)
        # ----- 实验数据 -----
        functools.partial(UpdatePage1.update_exp_figure, self)()
        # ----- 线状谱和展宽 -----
        functools.partial(UpdatePage1.update_line_figure, self)()
        functools.partial(UpdatePage1.update_widen_figure, self)()

    def re_widen(self):
        """
        重新展宽

        """
        self.cowan.cal_data.set_delta_lambda(self.ui.offset.value())
        # self.cowan.cal_data.widen_all.delta_lambda = self.ui.offset.value()
        # self.cowan.cal_data.widen_part.delta_lambda = self.ui.offset.value()
        self.cowan.cal_data.set_fwhm(self.ui.widen_fwhm.value())
        # self.cowan.cal_data.widen_all.fwhm_value = self.ui.widen_fwhm.value()
        # self.cowan.cal_data.widen_part.fwhm_value = self.ui.widen_fwhm.value()
        widen_temperature = self.ui.widen_temp.value()
        self.cowan.cal_data.widen_all.widen(widen_temperature, False)
        # self.cowan.cal_data.widen_part.widen_by_group(temperature=widen_temperature)

        # -------------------------- 更新历史记录和选择列表 --------------------------
        self.cowan_lists.add_history(self.cowan)

        # ------------------------- 更新界面 -------------------------
        # 更新展宽后图
        functools.partial(UpdatePage1.update_widen_figure, self)()
        # 更新选择列表
        functools.partial(UpdatePage1.update_selection_list, self)()
        # 更新历史记录列表
        functools.partial(UpdatePage1.update_history_list, self)()

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


class Page2(MainWindow):
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
        if self.info['x_range'] is None:
            pass
        else:
            self.expdata_2.set_range(self.info['x_range'])

        # -------------------------- 更新页面 --------------------------
        self.ui.page2_exp_data_path_name.setText(self.expdata_2.filepath.name)

    def plot_exp(self):
        """
        导入实验数据后，绘制实验数据

        """
        if self.expdata_2 is None:
            QMessageBox.warning(self, '警告', '请先加载实验数据！')
            return

        # -------------------------- 更新页面 --------------------------
        functools.partial(UpdatePage2.update_exp_figure, self)()

    def plot_spectrum(self, *args):
        """
        绘制叠加光谱

        Args:
            *args:

        """
        if self.expdata_2 is None:
            QMessageBox.warning(self, '警告', '请先导入实验数据！')
            return
        if not self.cowan_lists.chose_cowan:
            QMessageBox.warning(self, '警告', '请先添加计算结果！')
            return
        temperature = self.ui.page2_temperature.value()
        density = (self.ui.page2_density_base.value() * 10 ** self.ui.page2_density_index.value())
        self.simulate.exp_data = copy.deepcopy(self.expdata_2)
        self.simulate.init_cowan_list(self.cowan_lists)
        self.simulate.get_simulate_data(temperature, density)
        self.simulate.del_cowan_list()

        # -------------------------- 更新页面 --------------------------
        functools.partial(UpdatePage2.update_exp_sim_figure, self)()

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
            functools.partial(UpdatePage2.update_grid, self)()
            progressDialog.close()
            self.ui.page2_cal_grid.setEnabled(True)
            self.ui.statusbar.showMessage('计算完成！')

        # 函数定义完成↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

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
        self.simulate.init_cowan_list(self.cowan_lists)
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
        self.simulate = copy.deepcopy(self.simulated_grid.grid_data[(temperature, density)])

        # -------------------------- 更新页面 --------------------------
        temp = density.split('e+')
        self.ui.page2_temperature.setValue(eval(temperature))
        self.ui.page2_density_base.setValue(eval(temp[0]))
        self.ui.page2_density_index.setValue(int(temp[1]))
        functools.partial(UpdatePage2.update_exp_sim_figure, self)()

    def st_resolution_recoder(self):
        """
        记录时空分辨光谱

        """
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
        self.simulate.del_cowan_list()
        self.space_time_resolution.add_st((st_time, st_space), self.simulate)

        # -------------------------- 更新页面 --------------------------
        # 第二页
        functools.partial(UpdatePage2.update_space_time_table, self)()
        # 第三页
        functools.partial(UpdatePage3.update_space_time_combobox, self)()
        # 第四页
        functools.partial(UpdatePage4.update_space_time_combobox, self)()

    def load_space_time(self):
        """
        批量导入时空分辨光谱

        """
        path = QFileDialog.getExistingDirectory(
            self, '请选择实验数据所在的文件夹', PROJECT_PATH().as_posix()
        )
        path = Path(path)
        for file_name in path.iterdir():
            loc, tim = file_name.stem.split('_')
            loc = loc.strip('mm')
            tim = tim.strip('ns')
            self.expdata_2 = ExpData(file_name)
            if self.info['x_range'] is None:
                pass
            else:
                self.expdata_2.set_range(self.info['x_range'])
            simulate = SimulateSpectral()
            simulate.load_exp_data(Path(file_name))
            self.space_time_resolution.add_st((tim, (loc, '0', '0')), simulate)

        # -------------------------- 更新页面 --------------------------
        # 第二页
        functools.partial(UpdatePage2.update_space_time_table, self)()

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
            functools.partial(UpdatePage2.update_grid, self)()

            self.ui.statusbar.showMessage('更新网格完成！')

        # 函数定义结束↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

        index = self.ui.st_resolution_table.currentIndex().row()
        key = list(self.space_time_resolution.simulate_spectral_dict.keys())[index]
        self.simulate = copy.deepcopy(self.space_time_resolution.simulate_spectral_dict[key])
        self.expdata_2 = copy.deepcopy(self.simulate.exp_data)
        if self.simulated_grid is not None:
            self.simulated_grid.change_task('update', self.expdata_2)
            simulated_grid_run = SimulateGridThread(self.simulated_grid)
            progressDialog = CustomProgressDialog(dialog_title='正在更新网格...')
            progressDialog.set_label_text('正在更新网格，请稍后……')
            simulated_grid_run.up_end.connect(update_grid)
            simulated_grid_run.start()
            progressDialog.show()

        # -------------------------- 更新页面 --------------------------
        self.ui.st_time.setText(key[0])
        self.ui.st_space_x.setText(key[1][0])
        self.ui.page2_exp_data_path_name.setText(self.expdata_2.filepath.name)
        if self.simulate.temperature and self.simulate.electron_density:
            functools.partial(UpdatePage2.update_temperature_density, self)()
            functools.partial(UpdatePage2.update_exp_sim_figure, self)()
        else:
            functools.partial(UpdatePage2.update_exp_figure, self)()
        functools.partial(UpdatePage2.update_space_time_table, self)()
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
            functools.partial(UpdatePage2.update_space_time_table, self)()
            # 第三页
            functools.partial(UpdatePage3.update_space_time_combobox, self)()
            # 第四页
            functools.partial(UpdatePage4.update_space_time_combobox, self)()

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
            if not okPressed:
                return
            for wave in self.simulate.characteristic_peaks:
                if abs(wave - input_value) < 0.0001:
                    QMessageBox.warning(self, '警告', '该特征波长已存在！')
                    return
            self.simulate.characteristic_peaks.append(input_value)
            self.simulate.characteristic_peaks.sort()
            dialog.activateWindow()
            update_ui()

        def del_data():
            self.simulate.characteristic_peaks.pop(peaks_browser.currentRow())
            update_ui()

        def close_window():
            if all_changed.isChecked():
                for sim in self.space_time_resolution.simulate_spectral_dict.values():
                    sim.characteristic_peaks = copy.deepcopy(self.simulate.characteristic_peaks)
            functools.partial(UpdatePage2.update_characteristic_peaks, self)()
            dialog.close()

        def update_ui():
            peaks_browser.clear()
            peaks_browser.addItems(['{:.4f}'.format(i) for i in self.simulate.characteristic_peaks])

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
                value=self.simulate.characteristic_peaks[index]
            )
            if not okPressed:
                return
            self.simulate.characteristic_peaks[index] = input_value
            self.simulate.characteristic_peaks.sort()
            dialog.activateWindow()
            update_ui()

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
            if checkbox.isChecked():
                temper = self.ui.page2_temperature.value()
                density = (self.ui.page2_density_base.value() * 10 ** self.ui.page2_density_index.value())
                self.simulate.init_cowan_list(self.cowan_lists)
                y_list = self.simulate.get_abu(temper, density)
                self.simulate.del_cowan_list()
            else:
                y_list = self.simulate.abundance

            if checkbox.isChecked():  # 显示全部
                x_list = [str(i) for i in range(len(y_list))]
                ax.bar(x_list, y_list)
            else:  # 显示选中的
                x_list = [key.split('_')[-1] for key in self.cowan_lists.chose_cowan]
                ax.bar(x_list, y_list)

            for x_, y_ in zip(x_list, y_list):
                ax.text(x_, y_, '{:.2f}'.format(y_), ha='center', va='bottom', fontsize=10)
            ax.set_title('${:2}$\n${:.2f}\\enspace eV \\quad and \\quad {}*10^{{{}}}\\enspace cm^{{-3}}$'.format(
                self.cowan_lists.chose_cowan[0].split('_')[0],
                self.ui.page2_temperature.value(),
                self.ui.page2_density_base.value(),
                self.ui.page2_density_index.value()))

            canvas.draw()

        if self.simulate is None:
            QMessageBox.warning(self, '警告', '请先模拟光谱！')
            return

        fig = plt.figure()
        ax = fig.add_subplot(111)

        widget = QDialog()
        canvas = FigureCanvas(fig)
        checkbox = QCheckBox('显示全部', widget)
        layout = QVBoxLayout(widget)
        layout.addWidget(canvas)
        layout.addWidget(checkbox)
        checkbox.clicked.connect(update_ui)

        update_ui()
        widget.exec()

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
                te, ne = sim.temperature, sim.electron_density
                sim.init_cowan_list(self.cowan_lists)
                sim.get_simulate_data(te, ne)
                sim.del_cowan_list()

        # 使用Qt多线程运行task
        self.task_thread = ProgressThread(dialog_title='正在应用Cowan的变化...', range_=(0, 100))
        self.task_thread.set_run(task)
        self.task_thread.progress_dialog.set_prompt_words('正在重新模拟xxx的光谱，请稍后……')
        self.task_thread.start()


class Page3(MainWindow):
    def plot_by_times(self):
        """
        绘制温度密度随时间变化的图

        """
        temp = self.ui.location_select.currentText().strip('(').strip(')')
        x, y, z = temp.split(',')
        x, y, z = x.strip(), y.strip(), z.strip()

        self.space_time_resolution.plot_change_by_time((x, y, z))
        self.ui.webEngineView_3.load(QUrl.fromLocalFile(self.space_time_resolution.change_by_time_path))

    def plot_by_locations(self):
        """
        绘制温度密度随位置变化的图

        """
        t = self.ui.time_select.currentText()

        self.space_time_resolution.plot_change_by_location(t)
        self.ui.webEngineView_4.load(
            QUrl.fromLocalFile(self.space_time_resolution.change_by_location_path)
        )

    def plot_by_space_time(self):
        """
        绘制温度密度随时间位置变化的二维图

        """
        variable_index = self.ui.variable_select.currentIndex()

        self.space_time_resolution.plot_change_by_space_time(variable_index)
        self.ui.webEngineView_5.load(
            QUrl.fromLocalFile(self.space_time_resolution.change_by_space_time_path)
        )


class Page4(MainWindow):
    def comboBox_changed(self, index):
        """
        在下拉框选择时空分辨光谱时
        Args:
            index: 下拉框当前选择索引

        """
        # 设置树状列表
        self.ui.treeWidget.clear()
        temp_list = []
        for key, value in self.space_time_resolution.simulate_spectral_dict.items():
            if value.temperature is None or value.electron_density is None:
                continue
            temp_list.append(copy.deepcopy(value))
        self.simulate_page4: SimulateSpectral = temp_list[index]
        self.simulate_page4.init_cowan_list(self.cowan_lists)
        # -------------------------- 更新页面 --------------------------
        functools.partial(UpdatePage4.update_treeview, self)()
        functools.partial(UpdatePage4.update_exp_figure, self)()

    def plot_con_contribution(self):
        """
        绘制各个组态的贡献

        """
        add_example = get_configuration_add_list(self)
        for cowan_, _ in self.cowan_lists:
            if cowan_.cal_data.widen_part.grouped_widen_data is None:
                cowan_.cal_data.widen_part.widen_by_group(temperature=self.ui.widen_temp.value())
        self.simulate_page4.init_cowan_list(self.cowan_lists)
        self.simulate_page4.plot_con_contribution_html(add_example)
        self.ui.webEngineView_2.load(QUrl.fromLocalFile(self.simulate_page4.example_path))
        self.simulate_page4.del_cowan_list()

    def plot_ion_contribution(self):
        """
        绘制各个离子的贡献

        """
        add_example = get_configuration_add_list(self)
        for cowan_, _ in self.cowan_lists:
            if cowan_.cal_data.widen_part.grouped_widen_data is None:
                cowan_.cal_data.widen_part.widen_by_group(temperature=self.ui.widen_temp.value())
        self.simulate_page4.init_cowan_list(self.cowan_lists)
        self.simulate_page4.plot_ion_contribution_html(add_example, self.ui.page4_consider_popular.isChecked())
        self.ui.webEngineView_2.load(QUrl.fromLocalFile(self.simulate_page4.example_path))
        self.simulate_page4.del_cowan_list()

    @staticmethod
    def tree_item_changed(self, item, column):
        """
        树状列表项改变时

        Args:
            self:
            item:
            column:

        """
        if item.parent() is None:
            if item.checkState(0) == Qt.Checked:
                for i in range(item.childCount()):
                    if item.child(i).background(0).color().getRgb()[0] == 255:
                        item.child(i).setCheckState(0, Qt.Unchecked)
                    else:
                        item.child(i).setCheckState(0, Qt.Checked)
            else:
                for i in range(item.childCount()):
                    item.child(i).setCheckState(0, Qt.Unchecked)
        else:
            if item.checkState(0) == Qt.Checked:
                item.parent().setCheckState(0, Qt.Checked)
            else:
                for i in range(item.parent().childCount()):
                    if item.parent().child(i).checkState(0) == Qt.Checked:
                        break
                else:
                    item.parent().setCheckState(0, Qt.Unchecked)
