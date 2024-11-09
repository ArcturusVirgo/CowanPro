import pandas as pd
from PySide6.QtWidgets import QWidget, QFileDialog, QMessageBox, QTableWidgetItem

from main import MainWindow
from ..Tools import console_logger, dataframe_append_series
from ..Model import PROJECT_PATH, Cowan, SimulateSpectral
from ..View import Ui_DataShow


class DataShowWidget(QWidget):
    """
    数据展示窗口
    """

    def __init__(self, main_window: MainWindow):
        super().__init__()
        self.ui = Ui_DataShow()
        self.ui.setupUi(self)

        self.main_window = main_window

        self.bind_slot()
        self.choose_page_index(0)

    def bind_slot(self):
        self.ui.cowan_change.clicked.connect(lambda: self.choose_page_index(0))
        self.ui.all_cowan_change.clicked.connect(lambda: self.choose_page_index(1))
        self.ui.st_change.clicked.connect(lambda: self.choose_page_index(2))
        self.ui.all_st_change.clicked.connect(lambda: self.choose_page_index(3))

        self.ui.choose_ion.currentIndexChanged.connect(self.choose_ion_changed)
        self.ui.export_1_overall.clicked.connect(self.export_cowan_overall)
        self.ui.export_1_con.clicked.connect(self.export_cowan_configuration)
        self.ui.export_2.clicked.connect(self.export_all_cowan)
        self.ui.choose_st.currentIndexChanged.connect(self.choose_space_time_changed)
        self.ui.export_3_overall.clicked.connect(self.export_space_time_overall)
        self.ui.export_3_con.clicked.connect(self.export_space_time_configuration)
        self.ui.export_4.clicked.connect(self.export_all_space_time)

    def choose_page_index(self, index):
        if index == 0:
            self.ui.choose_ion.clear()
            add_list = [i.name for i, _ in self.main_window.cowan_lists]
            self.ui.choose_ion.addItems(add_list)
        if index == 1:
            self.ui.all_cowan_info_table.clear()
            self.ui.all_cowan_info_table.setRowCount(len(self.main_window.cowan_lists.chose_cowan))
            self.ui.all_cowan_info_table.setColumnCount(4)
            self.ui.all_cowan_info_table.setHorizontalHeaderLabels(['离化度', '偏移', 'FWHM', '温度'])
            for i, (cowan, _) in enumerate(self.main_window.cowan_lists):
                delta_lambda, fwhm, temperature = cowan.cal_data.get_cowan_info()
                self.ui.all_cowan_info_table.setItem(i, 0, QTableWidgetItem(cowan.name))
                self.ui.all_cowan_info_table.setItem(i, 1, QTableWidgetItem(f'{delta_lambda:.4f}nm'))
                self.ui.all_cowan_info_table.setItem(i, 2, QTableWidgetItem(f'{fwhm:.4f}eV'))
                self.ui.all_cowan_info_table.setItem(i, 3, QTableWidgetItem(f'{temperature:.4f}eV'))
        if index == 2:
            self.ui.choose_st.clear()
            add_list = []
            for key, simulate in self.main_window.space_time_resolution:
                simulate: SimulateSpectral
                if simulate.get_temperature_and_density() == (None, None):
                    continue
                add_list.append(f'时间：{key[0]:3>}；位置：{key[1][0]:3>}')
            self.ui.choose_st.addItems(add_list)
        if index == 3:
            self.ui.st_info_table.clear()
            self.ui.st_info_table.setRowCount(len(self.main_window.space_time_resolution.simulate_spectral_dict.keys()))
            self.ui.st_info_table.setColumnCount(4)
            self.ui.st_info_table.setHorizontalHeaderLabels(['时间', '位置', '温度(eV)', '密度(cm^-3)'])
            for i, (key, simulate) in enumerate(self.main_window.space_time_resolution):
                simulate: SimulateSpectral
                if simulate.get_temperature_and_density() == (None, None):
                    continue
                temperature, electron_density = simulate.get_temperature_and_density()
                self.ui.st_info_table.setItem(i, 0, QTableWidgetItem(f'{key[0]:3>}'))
                self.ui.st_info_table.setItem(i, 1, QTableWidgetItem(f'{key[1][0]:3>}'))
                self.ui.st_info_table.setItem(i, 2, QTableWidgetItem(f'{temperature:.4f}'))
                self.ui.st_info_table.setItem(i, 3, QTableWidgetItem(f'{electron_density:.4e}'))
        self.ui.stackedWidget.setCurrentIndex(index)

    def choose_ion_changed(self, *args):
        ion_name = self.ui.choose_ion.currentText()
        if ion_name == '':
            return
        cowan: Cowan = self.main_window.cowan_lists.get_cowan_from_name(ion_name)
        delta_lambda, fwhm, temperature = cowan.cal_data.get_cowan_info()
        info_text = f'偏移：{delta_lambda:>.4f}nm  FWHM：{fwhm:>.4f}eV  温度：{temperature:>.4f}eV'
        self.ui.ion_info.setText(info_text)

    def choose_space_time_changed(self, *args):
        st_index = self.ui.choose_st.currentIndex()
        if st_index == -1:
            return
        simulate = self.main_window.space_time_resolution.get_simulate_spectral_diagnosed_by_index(st_index)[1]
        temperature, electron_density = simulate.get_temperature_and_density()
        info_text = f'温度：{temperature:>.4f}eV  电子密度：{electron_density:>.4e}cm^-3'
        self.ui.st_info.setText(info_text)

    def export_cowan_overall(self):
        console_logger.info('single ionization data export started')

        path = QFileDialog.getExistingDirectory(self, '选择存储路径', PROJECT_PATH().as_posix())

        ion_name = self.ui.choose_ion.currentText()
        cowan: Cowan = self.main_window.cowan_lists.get_cowan_from_name(ion_name)

        # 原始数据导出
        if self.ui.init_res_overall.isChecked():
            cowan_init_res = cowan.cal_data.get_init_data()
            cowan_init_res.to_csv(f'{path}/【单个离子】【{ion_name}】【整体】原始数据.csv', index=False)

        # 模拟数据导出
        if (
                self.ui.line_over_all.isChecked() or
                self.ui.gauss_overall.isChecked() or
                self.ui.cross_np_overall.isChecked() or
                self.ui.cross_p_overall.isChecked()
        ):
            export_data = pd.DataFrame()
            cowan_init_res = cowan.cal_data.get_init_data()
            widen_all_data = cowan.cal_data.widen_all.get_widen_data()
            if self.ui.line_over_all.isChecked():
                export_data = dataframe_append_series(export_data, 1239.85 / cowan_init_res['wavelength_ev'],
                                                      'wavelength_line_nm')
                export_data = dataframe_append_series(export_data, cowan_init_res['intensity'], 'intensity_line')
            if self.ui.gauss_overall.isChecked():
                export_data = dataframe_append_series(export_data, widen_all_data['wavelength'], 'wavelength_gauss_nm')
                export_data = dataframe_append_series(export_data, widen_all_data['gauss'], 'intensity_gauss')
            if self.ui.cross_np_overall.isChecked():
                export_data = dataframe_append_series(export_data, widen_all_data['wavelength'],
                                                      'wavelength_cross_np_nm')
                export_data = dataframe_append_series(export_data, widen_all_data['cross_NP'], 'intensity_cross_np')
            if self.ui.cross_p_overall.isChecked():
                export_data = dataframe_append_series(export_data, widen_all_data['wavelength'],
                                                      'wavelength_cross_p_nm')
                export_data = dataframe_append_series(export_data, widen_all_data['cross_P'], 'intensity_cross_p')
            # 【单个离子】【Al_3】【整体】展宽数据
            export_data.to_csv(f'{path}/【单个离子】【{ion_name}】【整体】展宽数据.csv', index=False)

        console_logger.info('single ionization data export completed')

    def export_cowan_configuration(self):
        ion_name = self.ui.choose_ion.currentText()
        if ion_name == '':
            QMessageBox.warning(self, '警告', '请先选择离化度！')
            return
        # 获取需要的数据
        cowan: Cowan = self.main_window.cowan_lists.get_cowan_from_name(ion_name)
        grouped_widen_data = cowan.cal_data.widen_part.get_grouped_widen_data()
        if grouped_widen_data is None:
            QMessageBox.warning(self, '警告', '请重新展宽该离化度')
            return
        grouped_data = cowan.cal_data.widen_part.get_grouped_data()

        console_logger.info('single ionization data export (group by configuration) started')

        path = QFileDialog.getExistingDirectory(self, '选择存储路径', PROJECT_PATH().as_posix())
        # 原始数据导出
        if self.ui.init_res_con.isChecked():
            for key, value in grouped_data.items():
                # 【单个离子】【Al_3】【按组态分组】【1_1】原始数据
                value.to_csv(f'{path}/【单个离子】【{ion_name}】【按组态分组】【{key}】原始数据.csv', index=False)

        # 高斯积分
        if self.ui.gauss_integral.isChecked():
            export_data = cowan.cal_data.widen_part.get_gauss_integral()
            export_data.to_csv(f'{path}/【单个离子】【{ion_name}】【按组态分组】高斯积分.csv', index=False)

        # 按组态
        if (
                self.ui.line_con.isChecked() or
                self.ui.gauss_con.isChecked() or
                self.ui.cross_np_con.isChecked() or
                self.ui.cross_p_con.isChecked()
        ):
            for key, value in grouped_widen_data.items():
                export_data = pd.DataFrame()
                if self.ui.line_con.isChecked():
                    export_data = dataframe_append_series(export_data, 1239.85 / grouped_data[key]['wavelength_ev'],
                                                          'wavelength_line_nm')
                    export_data = dataframe_append_series(export_data, grouped_data[key]['intensity'], 'intensity_line')
                if self.ui.gauss_con.isChecked():
                    export_data = dataframe_append_series(export_data, value['wavelength'], 'wavelength_gauss_nm')
                    export_data = dataframe_append_series(export_data, value['gauss'], 'intensity_gauss')
                if self.ui.cross_np_con.isChecked():
                    export_data = dataframe_append_series(export_data, value['wavelength'], 'wavelength_cross_np_nm')
                    export_data = dataframe_append_series(export_data, value['cross_NP'], 'intensity_cross_np')
                if self.ui.cross_p_con.isChecked():
                    export_data = dataframe_append_series(export_data, value['wavelength'], 'wavelength_cross_p_nm')
                    export_data = dataframe_append_series(export_data, value['cross_P'], 'intensity_cross_p')
                export_data.to_csv(f'{path}/【单个离子】【{ion_name}】【按组态分组】【{key}】展宽数据.csv', index=False
                                   )
        console_logger.info('single ionization data export (group by configuration) completed')

    def export_all_cowan(self):
        console_logger.info('all ionization data export started')
        path = QFileDialog.getExistingDirectory(self, '选择存储路径', PROJECT_PATH().as_posix())
        temp_list_1 = []
        temp_list_2 = []
        temp_list_3 = []
        temp_list_4 = []
        for i, (cowan, _) in enumerate(self.main_window.cowan_lists):
            delta_lambda, fwhm, temperature = cowan.cal_data.get_cowan_info()
            temp_list_1.append(f'{cowan.name}')
            temp_list_2.append(delta_lambda)
            temp_list_3.append(fwhm)
            temp_list_4.append(temperature)

        export_data = pd.DataFrame({
            '离化度': temp_list_1,
            '偏移(nm)': temp_list_2,
            'FWHM(eV)': temp_list_3,
            '温度(eV)': temp_list_4
        })
        export_data.to_csv(f'{path}/【所有离子】信息.csv', index=False)

        console_logger.info('all ionization data export completed')

    def export_space_time_overall(self):
        st_index = self.ui.choose_st.currentIndex()
        st_name = self.ui.choose_st.currentText()
        if st_name == '':
            QMessageBox.warning(self, '警告', '请先选择位置时间！')
            return

        key, simulate = self.main_window.space_time_resolution.get_simulate_spectral_diagnosed_by_index(st_index)
        simulate: SimulateSpectral

        console_logger.info('space time resolution data export started')
        path = QFileDialog.getExistingDirectory(self, '选择存储路径', PROJECT_PATH().as_posix())

        if (
                self.ui.exp_data.isChecked() or
                self.ui.sim_data.isChecked()
        ):
            export_data = pd.DataFrame()

            if self.ui.exp_data.isChecked():
                exp_data = simulate.get_exp_data()
                export_data = dataframe_append_series(export_data, exp_data['wavelength'], 'exp_wavelength_nm')
                export_data = dataframe_append_series(export_data, exp_data['intensity'], 'exp_intensity')
                export_data = dataframe_append_series(export_data, exp_data['intensity_normalization'],
                                                      'exp_intensity_norm')
            if self.ui.sim_data.isChecked():
                sim_data = simulate.get_sim_data()
                export_data = dataframe_append_series(export_data, sim_data['wavelength'], 'sim_wavelength_nm')
                export_data = dataframe_append_series(export_data, sim_data['intensity'], 'sim_intensity')
                export_data = dataframe_append_series(export_data, sim_data['intensity_normalization'],
                                                      'sim_intensity_norm')
            export_data.to_csv(f'{path}/【单个时空分辨光谱】【{key[0]}-{key[1][0]}】实验光谱与模拟光谱.csv', index=False)

        if self.ui.ion_abu.isChecked():
            abu_data_dict = simulate.get_abundance()
            for atom_name, abu_data in abu_data_dict.items():

                name_list = [i for i in range(len(abu_data))]
                export_data = pd.DataFrame({
                    '离化度': name_list,
                    '丰度': abu_data
                })
                export_data.to_csv(f'{path}/【单个时空分辨光谱】【{atom_name}】【{key[0]}-{key[1][0]}】各离子丰度.csv', index=False)

        console_logger.info('space time resolution data export completed')

    def export_space_time_configuration(self):
        st_index = self.ui.choose_st.currentIndex()
        st_name = self.ui.choose_st.currentText()
        if st_name == '':
            QMessageBox.warning(self, '警告', '请先选择位置时间！')
            return
        st_key, simulate = self.main_window.space_time_resolution.get_simulate_spectral_diagnosed_by_index(st_index)
        simulate: SimulateSpectral
        ion_contribution: dict = simulate.get_ion_contribution()

        console_logger.info('space time resolution grouped data export started')

        path = QFileDialog.getExistingDirectory(self, '选择存储路径', PROJECT_PATH().as_posix())
        if self.ui.ion_widen.isChecked() or self.ui.ion_widen_abu.isChecked():
            for key, value in ion_contribution.items():
                key: str
                value: pd.DataFrame  # wavelength intensity intensity_with_population
                if self.ui.ion_widen.isChecked() and self.ui.ion_widen_abu.isChecked():
                    export_data = value
                elif self.ui.ion_widen.isChecked():
                    export_data = value[['wavelength', 'intensity']]
                elif self.ui.ion_widen_abu.isChecked():
                    export_data = value[['wavelength', 'intensity_with_population']]
                else:
                    raise ValueError('未知错误！')
                export_data.to_csv(
                    f'{path}/【单个时空分辨光谱】【{st_key[0]}-{st_key[1][0]}】【离子贡献】【{key}】展宽数据.csv', index=False
                )

        console_logger.info('space time resolution grouped data export completed')

    def export_all_space_time(self):
        console_logger.info('all space time resolution data export started')

        path = QFileDialog.getExistingDirectory(self, '选择存储路径', PROJECT_PATH().as_posix())
        data_list = []
        self.ui.st_info_table.setHorizontalHeaderLabels(['时间', '位置', '温度(eV)', '密度(cm^-3)'])
        for i, (key, simulate) in enumerate(self.main_window.space_time_resolution.simulate_spectral_dict.items()):
            space_ = f'{key[1][0]:3>}'
            time_ = f'{key[0]:3>}'
            temperature, electron_density = simulate.get_temperature_and_density()
            data_list.append([time_, space_, temperature, electron_density])
        export_data = pd.DataFrame(data_list, columns=['时间', '位置', '温度(eV)', '密度(cm^-3)'])
        export_data.to_csv(f'{path}/【所有时空分辨光谱】信息.csv', index=False)

        console_logger.info('all space time resolution data export completed')


class ExportData(MainWindow):
    def show_export_data_window(self):
        self.export_data_window = DataShowWidget(main_window=self)
        self.export_data_window.show()

    def export_statistics_table(self):
        if self.cowan_page5 is None:
            QMessageBox.warning(self, '警告', '请先选择离化度！')
            return
        console_logger.info('exporting statistics table started')

        path = QFileDialog.getExistingDirectory(self, '选择存储路径', PROJECT_PATH().as_posix())
        name_list = ['index_l', 'index_h', 'name', 'min(nm)', 'max(nm)', 'n', 'sum_gf', 'sum_Ar', 'sum_Aa', 'ave_Aa',
                     'ave_Ga',
                     'ConAverGa', 'ConEWidth']
        data_list = []
        for i, (key, value) in enumerate(self.cowan_page5.cal_data.info_dict.items()):
            temp_list = [
                key[0],
                key[1],
                self.cowan_page5.in36.get_configuration_name(key[0], key[1]),
                value['wavelength_range']['min'],
                value['wavelength_range']['max'],
                value['line_num'],
                value['sum_gf'],
                value['sum_Ar'],
                value['sum_Aa'],
                value['ave_Aa'],
                value['ave_Ga'],
                value['ConAverGa'],
                value['ConEWidth']
            ]
            data_list.append(temp_list)
        export_data = pd.DataFrame(data_list, columns=name_list)
        export_data.to_csv(f'{path}/{self.cowan_page5.name}_统计数据.csv', index=False)

        console_logger.info('exporting statistics table completed')
