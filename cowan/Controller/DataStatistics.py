import copy
import functools
import warnings

from PySide6.QtWidgets import QTableWidgetItem

from main import MainWindow
from ..Model import Cowan


class DataStatistics(MainWindow):
    def ion_selected(self, index):
        self.cowan_page5: Cowan = copy.deepcopy(self.cowan_lists[index][0])
        self.cowan_page5.cal_data.get_statistics()
        functools.partial(UpdateDataStatistics.update_statistics_table, self)()


class UpdateDataStatistics(MainWindow):
    def update_statistics_table(self):
        if self.cowan_page5 is None:
            warnings.warn('cowan_page5 is None')
            return
        name_list = ['index_l', 'index_h', 'name', 'min(nm)', 'max(nm)', 'n', 'sum_gf', 'sum_Ar', 'sum_Aa', 'ave_Aa', 'ave_Ga',
                     'ConAverGa', 'ConEWidth']
        self.ui.statistical_table.clear()
        self.ui.statistical_table.setRowCount(len(self.cowan_page5.cal_data.info_dict.keys()))
        self.ui.statistical_table.setColumnCount(len(name_list))
        self.ui.statistical_table.setHorizontalHeaderLabels(name_list)
        for i, (key, value) in enumerate(self.cowan_page5.cal_data.info_dict.items()):
            item_0 = QTableWidgetItem(str(key[0]))
            item_1 = QTableWidgetItem(str(key[1]))
            name = self.cowan_page5.in36.get_configuration_name(key[0], key[1])
            item_2 = QTableWidgetItem(name)
            item_3 = QTableWidgetItem('{:>7.3f}'.format(value['wavelength_range']['min']))
            item_4 = QTableWidgetItem('{:>7.3f}'.format(value['wavelength_range']['max']))
            item_5 = QTableWidgetItem('{:>4d}'.format(value['line_num']))
            item_6 = QTableWidgetItem('{:>7.3f}'.format(value['sum_gf']))
            item_7 = QTableWidgetItem('{:>10.2e}'.format(value['sum_Ar']))
            item_8 = QTableWidgetItem('{:>10.2e}'.format(value['sum_Aa']))
            item_9 = QTableWidgetItem('{:>10.2e}'.format(value['ave_Aa']))
            item_10 = QTableWidgetItem('{:>7.3f}'.format(value['ave_Ga']))
            item_11 = QTableWidgetItem('{:>10.3f}'.format(value['ConAverGa']))
            item_12 = QTableWidgetItem('{:>10.3f}'.format(value['ConEWidth']))
            self.ui.statistical_table.setItem(i, 0, item_0)
            self.ui.statistical_table.setItem(i, 1, item_1)
            self.ui.statistical_table.setItem(i, 2, item_2)
            self.ui.statistical_table.setItem(i, 3, item_3)
            self.ui.statistical_table.setItem(i, 4, item_4)
            self.ui.statistical_table.setItem(i, 5, item_5)
            self.ui.statistical_table.setItem(i, 6, item_6)
            self.ui.statistical_table.setItem(i, 7, item_7)
            self.ui.statistical_table.setItem(i, 8, item_8)
            self.ui.statistical_table.setItem(i, 9, item_9)
            self.ui.statistical_table.setItem(i, 10, item_10)
            self.ui.statistical_table.setItem(i, 11, item_11)
            self.ui.statistical_table.setItem(i, 12, item_12)

    def update_ion_select_combox(self):
        self.ui.page5_ion_select.clear()
        for cowan, flag in self.cowan_lists:
            self.ui.page5_ion_select.addItem(cowan.name)
