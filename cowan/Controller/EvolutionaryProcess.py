from PySide6.QtCore import QUrl

from main import MainWindow


class EvolutionaryProcess(MainWindow):
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


class UpdateEvolutionaryProcess(MainWindow):
    def update_space_time_combobox(self):
        self.ui.location_select.clear()
        self.ui.time_select.clear()
        temp_times = []
        temp_locations = []
        for key in self.space_time_resolution.simulate_spectral_dict:
            if (self.space_time_resolution.simulate_spectral_dict[key].temperature is not None
                    or self.space_time_resolution.simulate_spectral_dict[key].electron_density is not None):
                temp_times.append(key[0])
                temp_locations.append(key[1])
        temp_times = set(temp_times)
        temp_locations = set(temp_locations)
        temp_times = [f'{key}' for key in temp_times]
        temp_locations = [f'({key[0]}, {key[1]}, {key[2]})' for key in temp_locations]
        self.ui.location_select.addItems(temp_locations)
        self.ui.time_select.addItems(temp_times)
