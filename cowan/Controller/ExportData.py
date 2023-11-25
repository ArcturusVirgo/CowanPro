import pandas as pd
from PySide6.QtWidgets import QWidget, QFileDialog, QMessageBox, QTableWidgetItem

from main import MainWindow
from ..Tools.Other import print_to_console
from ..Model import PROJECT_PATH, Cowan
from ..View.DataShowWindow import Ui_DataShow


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
        self.ui.stackedWidget.setCurrentIndex(0)

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
        self.ui.export_3_overall.clicked.connect(self.export_st_overall)

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
            for key in self.main_window.space_time_resolution.simulate_spectral_dict.keys():
                add_list.append(f'时间：{key[0]:3>}；位置：{key[1][0]:3>}')
            self.ui.choose_st.addItems(add_list)

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
        key, simulate = self.main_window.space_time_resolution[st_index]
        temperature, electron_density = simulate.get_temperature_and_density()
        info_text = f'温度：{temperature:>.4f}eV  电子密度：{electron_density:>.4e}cm^-3'
        self.ui.st_info.setText(info_text)

    def export_cowan_overall(self):
        print_to_console(
            text='single ionization data export | start >>>',
            color=('green', 'blue'),
            outline_level=0,
            thickness=1
        )
        path = QFileDialog.getExistingDirectory(self, '选择存储路径', PROJECT_PATH().as_posix())

        ion_name = self.ui.choose_ion.currentText()
        cowan: Cowan = self.main_window.cowan_lists.get_cowan_from_name(ion_name)

        # 原始数据导出
        if self.ui.init_res_overall.isChecked():
            print_to_console('exporting init data ...', outline_level=1, end='')
            cowan_init_res = cowan.cal_data.get_init_data()
            cowan_init_res.to_csv(f'{path}/{ion_name}_原始数据.csv', index=False)
            print_to_console('done', outline_level=1)

        # 模拟数据导出
        print_to_console('exporting widen data | start >>>', color=('green', 'yellow'), outline_level=1)
        export_data = pd.DataFrame()
        cowan_init_res = cowan.cal_data.get_init_data()
        widen_all_data = cowan.cal_data.widen_all.get_widen_data()
        if self.ui.line_over_all.isChecked():
            print_to_console('exporting line data ...', outline_level=2, end='')
            export_data['wavelength_line_nm'] = 1239.85 / cowan_init_res['wavelength_ev']
            export_data['intensity_line'] = cowan_init_res['intensity']
            print_to_console('done', outline_level=1)
        if self.ui.gauss_overall.isChecked():
            print_to_console('exporting gauss data ...', outline_level=2, end='')
            export_data['wavelength_gauss_nm'] = widen_all_data['wavelength']
            export_data['intensity_gauss'] = widen_all_data['gauss']
            print_to_console('done', outline_level=1)
        if self.ui.cross_np_overall.isChecked():
            print_to_console('exporting cross_np data ...', outline_level=2, end='')
            export_data['wavelength_cross_np_nm'] = widen_all_data['wavelength']
            export_data['intensity_cross_np'] = widen_all_data['cross_NP']
            print_to_console('done', outline_level=1)
        if self.ui.cross_p_overall.isChecked():
            print_to_console('exporting cross_p data ...', outline_level=2, end='')
            export_data['wavelength_cross_p_nm'] = widen_all_data['wavelength']
            export_data['intensity_cross_p'] = widen_all_data['cross_P']
            print_to_console('done', outline_level=1)
        export_data.to_csv(f'{path}/{ion_name}_模拟数据.csv', index=False)

        print_to_console(
            text='single ionization data export | end',
            color=('green', 'blue'),
            outline_level=0,
            thickness=1
        )

    def export_cowan_configuration(self):
        ion_name = self.ui.choose_ion.currentText()
        if ion_name == '':
            QMessageBox.warning(self, '警告', '请先选择离化度！')
            return
        print_to_console(
            text='single ionization data export (group by configuration) | start >>>',
            color=('green', 'blue'),
            outline_level=0,
            thickness=1
        )

        # 获取需要的数据
        cowan: Cowan = self.main_window.cowan_lists.get_cowan_from_name(ion_name)
        grouped_widen_data = cowan.cal_data.widen_part.get_grouped_widen_data()
        grouped_data = cowan.cal_data.widen_part.get_grouped_data()

        path = QFileDialog.getExistingDirectory(self, '选择存储路径', PROJECT_PATH().as_posix())

        # 原始数据导出
        print_to_console('exporting init data | start >>>', color=('green', 'yellow'), outline_level=1)
        for key, value in grouped_data.items():
            if self.ui.line_con.isChecked():
                print_to_console(f'exporting line data ({key}) ...', outline_level=2, end='')
                value.to_csv(f'{path}/{ion_name}_原始数据_分组后_{key}.csv', index=False)
                print_to_console('done', outline_level=1)
        print_to_console('exporting init data | end', color=('green', 'yellow'), outline_level=1)

        # 按组态
        print_to_console('exporting widen by group data | start >>>', color=('green', 'yellow'), outline_level=1)
        for key, value in grouped_widen_data.items():
            export_data = pd.DataFrame()
            if self.ui.gauss_con.isChecked():
                print_to_console(f'exporting gauss data ({key}) ...', outline_level=2, end='')
                export_data['wavelength_gauss_nm'] = value['wavelength']
                export_data['intensity_gauss'] = value['gauss']
                print_to_console('done', outline_level=1)
            if self.ui.cross_np_con.isChecked():
                print_to_console(f'exporting cross_np data ({key}) ...', outline_level=2, end='')
                export_data['wavelength_cross_np_nm'] = value['wavelength']
                export_data['intensity_cross_np'] = value['cross_NP']
                print_to_console('done', outline_level=1)
            if self.ui.cross_p_con.isChecked():
                print_to_console(f'exporting cross_p data ({key}) ...', outline_level=2, end='')
                export_data['wavelength_cross_p_nm'] = value['wavelength']
                export_data['intensity_cross_p'] = value['cross_P']
                print_to_console('done', outline_level=1)
            export_data.to_csv(f'{path}/{ion_name}_模拟数据_分组后{key}.csv', index=False)
        print_to_console('exporting widen by group data | end', color=('green', 'yellow'), outline_level=1)

        print_to_console(
            text='single ionization data export (group by configuration) | end',
            color=('green', 'blue'),
            outline_level=0,
            thickness=1
        )

    def export_all_cowan(self):
        print_to_console(
            text='all ionization data export | start >>>',
            color=('green', 'blue'),
            outline_level=0,
            thickness=1
        )
        path = QFileDialog.getExistingDirectory(self, '选择存储路径', PROJECT_PATH().as_posix())
        temp_list_1 = []
        temp_list_2 = []
        temp_list_3 = []
        temp_list_4 = []
        for i, (cowan, _) in enumerate(self.main_window.cowan_lists):
            print_to_console(f'exporting {cowan.name} ...', outline_level=1, end='')
            delta_lambda, fwhm, temperature = cowan.cal_data.get_cowan_info()
            temp_list_1.append(f'{cowan.name}')
            temp_list_2.append(delta_lambda)
            temp_list_3.append(fwhm)
            temp_list_4.append(temperature)
            print_to_console('done', outline_level=1)

        export_data = pd.DataFrame({
            '离化度': temp_list_1,
            '偏移(nm)': temp_list_2,
            'FWHM(eV)': temp_list_3,
            '温度(eV)': temp_list_4
        })
        export_data.to_csv(f'{path}/所有离子数据.csv', index=False)

        print_to_console(
            text='all ionization data export | end',
            color=('green', 'blue'),
            outline_level=0,
            thickness=1
        )

    def export_st_overall(self):
        st_index = self.ui.choose_st.currentIndex()
        st_name = self.ui.choose_st.currentText()
        if st_name == '':
            QMessageBox.warning(self, '警告', '请先选择位置时间！')
            return
        print_to_console(
            text='space time resolution data export | start >>>',
            color=('green', 'blue'),
            outline_level=0,
            thickness=1
        )
        key, simulate = self.main_window.space_time_resolution[st_index]
        temperature, electron_density = simulate.get_temperature_and_density()
        if temperature is None or electron_density is None:
            QMessageBox.warning(self, '警告', '该时空分辨谱温度密度未计算，请重新选择！')
            return
        path = QFileDialog.getExistingDirectory(self, '选择存储路径', PROJECT_PATH().as_posix())
        export_data = pd.DataFrame()

        print_to_console('exporting exp data ...', outline_level=1, end='')
        exp_data = simulate.get_exp_data()
        export_data['exp_wavelength_nm'] = exp_data['wavelength']
        export_data['exp_intensity'] = exp_data['intensity']
        export_data['exp_intensity_norm'] = exp_data['intensity_normalization']
        print_to_console('done', outline_level=1)

        print_to_console('exporting sim data ...', outline_level=1, end='')
        sim_data = simulate.get_sim_data()
        export_data['sim_wavelength_nm'] = sim_data['wavelength']
        export_data['sim_intensity'] = sim_data['intensity']
        export_data['sim_intensity_norm'] = sim_data['intensity_normalization']
        print_to_console('done', outline_level=1)
        export_data.to_csv(f'{path}/{st_name}_实验与模拟数据.csv', index=False)

        print_to_console('exporting abu ...', outline_level=1, end='')
        simulate.init_cowan_list(self.main_window.cowan_lists)
        abu_data = simulate.get_abu(*simulate.get_temperature_and_density())
        simulate.del_cowan_list()
        name_list = [i for i in range(len(abu_data))]
        export_data = pd.DataFrame({
            '离化度': name_list,
            '丰度': abu_data
        })
        export_data.to_csv(f'{path}/{st_name}_丰度.csv', index=False)
        print_to_console('done', outline_level=1)

        print_to_console(
            text='space time resolution data export | end',
            color=('green', 'blue'),
            outline_level=0,
            thickness=1
        )


class ExportData(MainWindow):
    def show_export_data_window(self):
        self.export_data_window = DataShowWidget(main_window=self)
        self.export_data_window.show()
