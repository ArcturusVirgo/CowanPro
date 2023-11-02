# 尝试
# class SimulateOfOffset(SimulateSpectral, QtCore.QThread):
#     def __init__(self, old_simulate: SimulateSpectral):
#         super().__init__()
#         self.old_simulate = old_simulate
#         self.cowan_list = old_simulate.cowan_list
#         self.add_or_not = old_simulate.add_or_not
#         self.exp_data = old_simulate.exp_data
#         self.temperature = old_simulate.temperature
#         self.electron_density = old_simulate.electron_density
#         # ===================================
#         self.offset_cal_dict = {}
#         self.offset_config = {}
#         self.sim_data = None
#
#         self.finished.connect(self.update_origin)
#
#     def set_offset_config(self, offsets):
#         """
#
#         Args:
#             offsets: 示例如下
#                 {'Al_4': [-1, 1, 10], 'Al_5': [-1, 1, 10], ...}
#
#         Returns:
#
#         """
#         self.offset_config = offsets
#
#     def run(self):
#         def calculate_all_offsets(offsets_list):
#             all_offsets = list(itertools.product(*offsets_list))
#             return all_offsets
#         params = []
#         for key, value in self.offset_config.items():
#             params.append(np.linspace(value[0], value[1], value[2]))
#
#
#
#         # # 设置偏移量，开始计算
#         # for cowan in self.cowan_list:
#         #     cowan.offset = params[cowan.name]
#         # self.get_simulate_data(temperature=self.temperature, electron_density=self.electron_density)
#
#     def update_origin(self):
#         pass
#
#         # self.old_simulate.cowan_list = old_simulate.cowan_list
#
