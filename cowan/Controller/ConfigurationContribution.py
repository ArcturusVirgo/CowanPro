import functools
import warnings

import pandas as pd
from PySide6.QtCore import QUrl, Qt
from PySide6.QtGui import QColor, QBrush
from PySide6.QtWidgets import QTreeWidgetItem, QMessageBox

from main import MainWindow
from ..Model import SimulateSpectral
from ..Tools import ProgressThread, get_configuration_add_list


class ConfigurationContribution(MainWindow):
    def comboBox_changed(self, index):
        """
        在下拉框选择时空分辨光谱时

        Args:
            index: 下拉框当前选择索引

        """
        # 设置树状列表
        self.ui.treeWidget.clear()
        self.simulate_page4: SimulateSpectral = \
            self.space_time_resolution.get_simulate_spectral_diagnosed_by_index(index)[1]
        # -------------------------- 更新页面 --------------------------
        functools.partial(UpdateConfigurationContribution.update_treeview, self)()
        functools.partial(UpdateConfigurationContribution.update_exp_figure, self)()

    def plot_con_contribution(self):
        """
        绘制各个组态的贡献

        """
        add_example = get_configuration_add_list(self)
        self.simulate_page4.plot_con_contribution_html(add_example)
        self.ui.webEngineView_2.load(QUrl.fromLocalFile(self.simulate_page4.example_path))

    def plot_ion_contribution(self):
        """
        绘制各个离子的贡献

        """
        add_example = get_configuration_add_list(self)
        self.simulate_page4.plot_ion_contribution_html(add_example, self.ui.page4_consider_popular.isChecked())
        self.ui.webEngineView_2.load(QUrl.fromLocalFile(self.simulate_page4.example_path))

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


class UpdateConfigurationContribution(MainWindow):
    def update_space_time_combobox(self):
        self.ui.comboBox.clear()
        temp_list = []
        for key in self.space_time_resolution.simulate_spectral_dict:
            if (self.space_time_resolution.simulate_spectral_dict[key].temperature is not None
                    or self.space_time_resolution.simulate_spectral_dict[key].electron_density is not None):
                temp_list.append('时间：{}       位置：{}, {}, {}'.format(
                    key[0], key[1][0], key[1][1], key[1][2]))
        self.ui.comboBox.addItems(temp_list)

    def update_treeview(self):
        def task():
            con_data: dict = self.simulate_page4.get_con_contribution()
            for ion_name, ion_value in con_data.items():
                ion_name: str
                ion_value: dict

                parents = QTreeWidgetItem()
                parents.setText(0, ion_name.replace('_', '+'))
                parents.setCheckState(0, Qt.Checked)

                for con_key, con_value in ion_value.items():
                    con_key: str
                    con_value: list
                    data: pd.DataFrame = con_value[0]
                    con_name: str = con_value[1]
                    child = QTreeWidgetItem()
                    child.setCheckState(0, Qt.Checked)
                    index_low, index_high = map(int, con_key.split('_'))
                    child.setText(0, f'{index_low},{index_high} => {con_name}')
                    if data['cross_P'].max() == 0:
                        child.setBackground(0, QBrush(QColor(255, 0, 0)))
                        child.setCheckState(0, Qt.Unchecked)
                    parents.addChild(child)

                self.ui.treeWidget.addTopLevelItem(parents)

        self.task_thread = ProgressThread(dialog_title='正在加载...')
        self.task_thread.set_run(task)
        self.task_thread.start()

    def update_exp_figure(self):
        if self.simulate_page4 is None:
            warnings.warn('第四页实验数据未加载', UserWarning)
            return
        self.simulate_page4.plot_html()
        self.ui.webEngineView.load(QUrl.fromLocalFile(self.simulate_page4.plot_path))
