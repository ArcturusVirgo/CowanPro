from PySide6.QtWidgets import QAbstractItemView

from cowan.cowan import *
from cowan.slots import *
from cowan.ui import *


class VerticalLine(QWidget):
    def __init__(self, x, y, height):
        super().__init__()
        self.ui = Ui_reference_line_window()
        self.ui.setupUi(self)
        self.dragPos = None
        self.ui.label.setMouseTracking(True)
        self.setGeometry(x, y, 100, height)

        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPosition().toPoint()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + (event.globalPosition().toPoint() - self.dragPos))
            self.dragPos = event.globalPosition().toPoint()
            event.accept()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_main_window()
        self.ui.setupUi(self)

        self.v_line = None

        # 第一页使用
        self.atom: Optional[Atom] = Atom(1, 0)
        self.in36: Optional[In36] = In36(self.atom)
        self.in2: Optional[In2] = In2()
        self.expdata_1: Optional[ExpData] = None

        self.run_history: List[Cowan] = []
        self.cowan: Optional[Cowan] = None

        self.expdata_2: Optional[ExpData] = None
        self.simulated_grid: Optional[SimulateGrid] = None
        self.simulate: Optional[SimulateSpectral] = SimulateSpectral()
        self.simulate_page4: Optional[SimulateSpectral] = None
        self.space_time_resolution = SpaceTimeResolution()

        # 测试
        # self.test()
        # self.load_Ge()

        # 初始化
        self.init()
        self.bind_slot()

        self.ui.navigation.setCurrentRow(2)

    def test(self):
        PROJECT_PATH = Path('F:/Cowan/Al')
        delta = {3: 0.05, 4: -0.04, 5: 0.0, 6: 0.05}

        for i in range(3, 7):
            self.atom = Atom(1, 0)
            self.in36 = In36(self.atom)
            self.in36.read_from_file(PROJECT_PATH / f'in36_{i}')
            self.in2 = In2()
            self.expdata_1 = ExpData(PROJECT_PATH / './exp_data.csv')
            self.cowan = Cowan(self.in36, self.in2, f'Al_{i}', self.expdata_1, 1)
            self.cowan.run()
            self.cowan.cal_data.widen_all.delta_lambda = delta[i]
            self.cowan.cal_data.widen_all.widen(25.6, False)
            self.run_history.append(copy.deepcopy(self.cowan))
            self.simulate.add_cowan(self.cowan)
        self.simulate.exp_data = copy.deepcopy(self.expdata_1)
        for x in range(5):
            for time in range(5):
                temp = 20 + np.random.random() * 30
                dishu = np.random.random() * 10
                zhishu = 17 + np.random.random() * 4
                den = dishu * 10**zhishu
                self.simulate.get_simulate_data(temp, den)
                self.space_time_resolution.add_st(
                    (str(time), (str(x), '0', '0')), self.simulate
                )

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

        # ----- 历史数据 -----
        # 更新历史记录列表
        functools.partial(UpdatePage1.update_history_list, self)()
        # 更新选择列表
        functools.partial(UpdatePage1.update_selection_list, self)()

        # --------------- 第二页
        self.expdata_2 = ExpData(PROJECT_PATH / 'exp_data.csv')
        # 更新界面
        self.ui.page2_exp_data_path_name.setText(self.expdata_2.filepath.name)
        # 时空分辨表格
        self.ui.st_resolution_table.clear()
        self.ui.st_resolution_table.setRowCount(
            len(self.space_time_resolution.simulate_spectral_dict)
        )
        self.ui.st_resolution_table.setColumnCount(5)
        self.ui.st_resolution_table.setHorizontalHeaderLabels(
            ['时间', '位置', '温度', '密度', '实验谱']
        )
        for i, (key, value) in enumerate(
            self.space_time_resolution.simulate_spectral_dict.items()
        ):
            item1 = QTableWidgetItem(key[0])
            item2 = QTableWidgetItem(f'({key[1][0]}, {key[1][1]}, {key[1][2]})')
            item3 = QTableWidgetItem('{:.3f}'.format(value.temperature))
            item4 = QTableWidgetItem('{:.3e}'.format(value.electron_density))
            item5 = QTableWidgetItem(value.exp_data.filepath.name)
            self.ui.st_resolution_table.setItem(i, 0, item1)
            self.ui.st_resolution_table.setItem(i, 1, item2)
            self.ui.st_resolution_table.setItem(i, 2, item3)
            self.ui.st_resolution_table.setItem(i, 3, item4)
            self.ui.st_resolution_table.setItem(i, 4, item5)

        # --------------- 第三页
        # 更新第三页元素
        self.ui.location_select.clear()
        temp_times = []
        temp_locations = []
        for key in self.space_time_resolution.simulate_spectral_dict:
            temp_times.append(key[0])
            temp_locations.append(key[1])
        temp_times = set(temp_times)
        temp_locations = set(temp_locations)
        temp_locations = [f'({key[0]}, {key[1]}, {key[2]})' for key in temp_locations]
        self.ui.location_select.addItems(temp_locations)
        self.ui.time_select.addItems(temp_times)

        # --------------- 第四页
        self.ui.comboBox.clear()
        temp_list = []
        for key in self.space_time_resolution.simulate_spectral_dict:
            temp_list.append(f'时间：{key[0]}    位置：{key[1][0]}, {key[1][1]}, {key[1][2]}')
        self.ui.comboBox.addItems(temp_list)
        Page4.comboBox_changed(self, 0)

    def load_Ge(self):
        PROJECT_PATH = Path('F:/Cowan/Ge')
        folder_path = Path(r'E:\研究生工作\科研工作\2023_08_08_Ge等离子体光谱\计算数据')
        self.expdata_1 = ExpData(Path(r'F:\Cowan\Ge\0.4mm.csv'))
        for path in folder_path.iterdir():
            self.atom = Atom(1, 0)
            self.in36 = In36(self.atom)
            self.in36.read_from_file(path / f'in36')
            self.in2 = In2()
            self.in2.read_from_file(path / f'in2')
            name = path.name.split('Ge')[-1].strip('+')
            self.cowan = Cowan(self.in36, self.in2, f'Ge_{name}', self.expdata_1, 1)
            self.cowan.cal_data = CalData(f'Ge_{name}', self.expdata_1)
            self.cowan.cal_data.widen_all.widen(25.6, False)
            self.run_history.append(copy.deepcopy(self.cowan))
            self.simulate.add_cowan(self.cowan)

        # for p in Path(r'F:\Cowan\Ge\exp_data').iterdir():
        #     x, time = p.stem.split('_')
        #     x = x.strip('mm')
        #     time = time.strip('ns')
        #     temp = 20 + np.random.random() * 30
        #     dishu = np.random.random() * 10
        #     zhishu = 17 + np.random.random() * 4
        #     den = dishu * 10 ** zhishu
        #     self.simulate.exp_data = copy.deepcopy(ExpData(p))
        #     self.simulate.get_simulate_data(temp, den)
        #     self.space_time_resolution.add_st((str(time), (str(x), '0', '0')), self.simulate)

        # -------------------------- 更新页面 --------------------------
        # ----- 原子信息 -----
        # 改变元素选择器
        self.ui.atomic_num.setCurrentIndex(self.atom.num - 1)
        self.ui.atomic_name.setCurrentIndex(self.atom.num - 1)
        self.ui.atomic_symbol.setCurrentIndex(self.atom.num - 1)
        # 改变离化度列表
        self.ui.atomic_ion.clear()
        self.ui.atomic_ion.addItems([str(i) for i in range(self.atom.num)])
        self.ui.atomic_ion.setCurrentIndex(self.atom.ion)
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
        # ----- in36 -----
        # 更新in36控制卡输入区
        for i in range(23):
            eval(f'self.ui.in36_{i + 1}').setText(self.in36.control_card[i].strip(' '))
        # 更新in36组态输入区
        df = pd.DataFrame(
            list(zip(*self.in36.configuration_card))[0],
            columns=['原子序数', '原子状态', '标识符', '空格', '组态'],
            index=list(range(1, len(self.in36.configuration_card) + 1)),
        )
        df['宇称'] = list(zip(*self.in36.configuration_card))[1]
        df = df[['宇称', '原子状态', '组态']]
        # 更新表格
        self.ui.in36_configuration_view.clear()
        self.ui.in36_configuration_view.setRowCount(df.shape[0])
        self.ui.in36_configuration_view.setColumnCount(df.shape[1])
        self.ui.in36_configuration_view.setHorizontalHeaderLabels(df.columns)
        for i in range(df.shape[0]):
            for j in range(df.shape[1]):
                item = QTableWidgetItem(str(df.iloc[i, j]))
                self.ui.in36_configuration_view.setItem(i, j, item)
        # ----- in2 -----
        in2_input_name = [
            'in2_1',
            'in2_2',
            'in2_3',
            'in2_4',
            'in2_5',
            'in2_6',
            'in2_7',
            'in2_8',
            'in2_9_a',
            'in2_9_b',
            'in2_9_c',
            'in2_9_d',
            'in2_10',
            'in2_11_a',
            'in2_11_b',
            'in2_11_c',
            'in2_11_d',
            'in2_11_e',
            'in2_12',
            'in2_13',
            'in2_14',
            'in2_15',
            'in2_16',
            'in2_17',
            'in2_18',
            'in2_19',
        ]
        for i, n in enumerate(in2_input_name):
            if '11' in n:
                eval(f'self.ui.{n}').setValue(int(self.in2.input_card[i].strip(' ')))
            else:
                eval(f'self.ui.{n}').setText(self.in2.input_card[i].strip(' '))
        # ----- 实验数据 -----
        self.expdata_1.plot_html()
        self.ui.exp_web.load(QUrl.fromLocalFile(self.expdata_1.plot_path))
        # ----- 偏移量 -----
        self.ui.offset.setValue(self.cowan.cal_data.widen_all.delta_lambda)
        # ----- 线状谱和展宽 -----
        self.cowan.cal_data.plot_line()
        self.cowan.cal_data.widen_all.plot_widen()
        # 加载线状谱
        self.ui.web_cal_line.load(QUrl.fromLocalFile(self.cowan.cal_data.plot_path))
        # 加载展宽数据
        if self.ui.crossP.isChecked():
            self.ui.web_cal_widen.load(
                QUrl.fromLocalFile(self.cowan.cal_data.widen_all.plot_path_cross_P)
            )
        elif self.ui.crossNP.isChecked():
            self.ui.web_cal_widen.load(
                QUrl.fromLocalFile(self.cowan.cal_data.widen_all.plot_path_cross_NP)
            )
        elif self.ui.gauss.isChecked():
            self.ui.web_cal_widen.load(
                QUrl.fromLocalFile(self.cowan.cal_data.widen_all.plot_path_gauss)
            )
        # ----- 历史数据 -----
        # 更新历史记录列表
        self.ui.run_history_list.clear()
        for c in self.run_history:
            self.ui.run_history_list.addItem(QListWidgetItem(c.name))
        # 更新选择列表
        self.ui.selection_list.clear()
        self.ui.page2_selection_list.clear()
        for c in self.simulate.cowan_list:
            self.ui.selection_list.addItem(QListWidgetItem(c.name))
            item = QListWidgetItem(c.name)
            item.setCheckState(Qt.CheckState.Checked)
            self.ui.page2_selection_list.addItem(item)

        # --------------- 第二页
        self.expdata_2 = ExpData(Path(r'F:\Cowan\Ge\0.4mm.csv'))
        # 更新界面
        self.ui.page2_exp_data_path_name.setText(self.expdata_2.filepath.name)
        # 时空分辨表格
        self.ui.st_resolution_table.clear()
        self.ui.st_resolution_table.setRowCount(
            len(self.space_time_resolution.simulate_spectral_dict)
        )
        self.ui.st_resolution_table.setColumnCount(5)
        self.ui.st_resolution_table.setHorizontalHeaderLabels(
            ['时间', '位置', '温度', '密度', '实验谱']
        )
        for i, (key, value) in enumerate(
            self.space_time_resolution.simulate_spectral_dict.items()
        ):
            item1 = QTableWidgetItem(key[0])
            item2 = QTableWidgetItem(f'({key[1][0]}, {key[1][1]}, {key[1][2]})')
            item3 = QTableWidgetItem('{:.3f}'.format(value.temperature))
            item4 = QTableWidgetItem('{:.3e}'.format(value.electron_density))
            item5 = QTableWidgetItem(value.exp_data.filepath.name)
            self.ui.st_resolution_table.setItem(i, 0, item1)
            self.ui.st_resolution_table.setItem(i, 1, item2)
            self.ui.st_resolution_table.setItem(i, 2, item3)
            self.ui.st_resolution_table.setItem(i, 3, item4)
            self.ui.st_resolution_table.setItem(i, 4, item5)

        # --------------- 第三页
        # 更新第三页元素
        self.ui.location_select.clear()
        temp_times = []
        temp_locations = []
        for key in self.space_time_resolution.simulate_spectral_dict:
            temp_times.append(key[0])
            temp_locations.append(key[1])
        temp_times = set(temp_times)
        temp_locations = set(temp_locations)
        temp_locations = [f'({key[0]}, {key[1]}, {key[2]})' for key in temp_locations]
        self.ui.location_select.addItems(temp_locations)
        self.ui.time_select.addItems(temp_times)

        # --------------- 第四页
        self.ui.comboBox.clear()
        temp_list = []
        for key in self.space_time_resolution.simulate_spectral_dict:
            temp_list.append(f'时间：{key[0]}    位置：{key[1][0]}, {key[1][1]}, {key[1][2]}')
        self.ui.comboBox.addItems(temp_list)
        if temp_list:
            Page4.comboBox_changed(self, 0)

    def init(self):
        # 给元素选择器设置初始值
        self.ui.atomic_num.addItems(list(map(str, ATOM.keys())))
        self.ui.atomic_symbol.addItems(list(zip(*ATOM.values()))[0])
        self.ui.atomic_name.addItems(list(zip(*ATOM.values()))[1])
        # in36组态表格相关设置
        self.ui.in36_configuration_view.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )  # 设置行选择模式
        self.ui.in36_configuration_view.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )  # 设置表格列宽自适应

        self.ui.page2_grid_list.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )  # 设置表格不可编辑
        self.ui.page2_grid_list.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )  # 设置表格列宽自适应

        self.ui.st_resolution_table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )  # 设置表格不可编辑
        self.ui.st_resolution_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )  # 设置表格列宽自适应
        # 设置右键菜单
        self.ui.in36_configuration_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.run_history_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.selection_list.setContextMenuPolicy(Qt.CustomContextMenu)
        # 设置单选
        self.ui.page2_grid_list.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        # 隐藏树控件的标题
        self.ui.treeWidget.header().hide()
        # 第三页 时空分辨表格设置
        self.ui.st_resolution_table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )  # 设置行选择模式

    def bind_slot(self):
        # 设置左侧列表与右侧页面切换之间的关联
        self.ui.navigation.currentRowChanged.connect(
            self.ui.stackedWidget.setCurrentIndex
        )

        # ------------------------------- 菜单栏 -------------------------------
        # self.ui.save_project.triggered.connect(self.slot_save_project)
        # self.ui.exit_project.triggered.connect(self.slot_exit_project)
        self.ui.load_exp_data.triggered.connect(
            functools.partial(Menu.load_exp_data, self)
        )  # 加载实验数据
        self.ui.show_guides.triggered.connect(
            functools.partial(Menu.show_guides, self)
        )  # 显示参考线

        # ------------------------------- 第一页 -------------------------------
        # 元素选择 - 下拉框
        self.ui.atomic_num.activated.connect(
            functools.partial(Page1.atom_changed, self)
        )  # 原子序数
        self.ui.atomic_symbol.activated.connect(
            functools.partial(Page1.atom_changed, self)
        )  # 元素符号
        self.ui.atomic_name.activated.connect(
            functools.partial(Page1.atom_changed, self)
        )  # 元素名称
        self.ui.atomic_ion.activated.connect(
            functools.partial(Page1.atom_ion_changed, self)
        )  # 离化度
        # 按钮
        self.ui.add_configuration.clicked.connect(
            functools.partial(Page1.add_configuration, self)
        )  # 添加组态
        self.ui.load_in36.clicked.connect(
            functools.partial(Page1.load_in36, self)
        )  # 加载in36文件
        self.ui.load_in2.clicked.connect(
            functools.partial(Page1.load_in2, self)
        )  # 加载in2文件
        self.ui.preview_in36.clicked.connect(
            functools.partial(Page1.preview_in36, self)
        )  # 预览in36
        self.ui.preview_in2.clicked.connect(
            functools.partial(Page1.preview_in2, self)
        )  # 预览in2
        self.ui.configuration_move_down.clicked.connect(
            functools.partial(Page1.configuration_move_down, self)
        )  # 组态下移
        self.ui.configuration_move_up.clicked.connect(
            functools.partial(Page1.configuration_move_up, self)
        )  # 组态上移
        self.ui.run_cowan.clicked.connect(
            functools.partial(Page1.run_cowan, self)
        )  # 运行Cowan
        # 单选框
        self.ui.auto_write_in36.clicked.connect(
            functools.partial(Page1.auto_write_in36, self)
        )  # 自动生成in36
        self.ui.manual_write_in36.clicked.connect(
            functools.partial(Page1.manual_write_in36, self)
        )  # 手动输入in36
        self.ui.gauss.clicked.connect(  # 线状谱展宽成gauss
            lambda: self.ui.web_cal_widen.load(
                QUrl.fromLocalFile(self.cowan.cal_data.widen_all.plot_path_gauss)
            )
        )
        self.ui.crossP.clicked.connect(  # 线状谱展宽成crossP
            lambda: self.ui.web_cal_widen.load(
                QUrl.fromLocalFile(self.cowan.cal_data.widen_all.plot_path_cross_P)
            )
        )
        self.ui.crossNP.clicked.connect(  # 线状谱展宽成crossNP
            lambda: self.ui.web_cal_widen.load(
                QUrl.fromLocalFile(self.cowan.cal_data.widen_all.plot_path_cross_NP)
            )
        )
        # 输入框
        self.ui.in2_11_e.valueChanged.connect(
            functools.partial(Page1.in2_11_e_value_changed, self)
        )  # in2 11 e
        # 右键菜单
        self.ui.in36_configuration_view.customContextMenuRequested.connect(
            functools.partial(Page1.in36_configuration_view_right_menu, self)
        )  # 组态显示卡的右键菜单
        self.ui.run_history_list.customContextMenuRequested.connect(
            functools.partial(Page1.run_history_list_right_menu, self)
        )  # 运行历史
        self.ui.selection_list.customContextMenuRequested.connect(
            functools.partial(Page1.selection_list_right_menu, self)
        )  # 叠加离子
        # 双击操作
        self.ui.run_history_list.itemDoubleClicked.connect(
            functools.partial(Page1.load_history, self)
        )  # 加载库中的项目
        # 数字选择框
        self.ui.update_offect.clicked.connect(
            functools.partial(Page1.offset_changed, self)
        )  # 偏移

        # ------------------------------- 第二页 -------------------------------
        # 按钮
        self.ui.page2_plot_spectrum.clicked.connect(
            functools.partial(Page2.plot_spectrum, self)
        )  # 绘制模拟谱
        self.ui.page2_load_exp_data.clicked.connect(
            functools.partial(Page2.load_exp_data, self)
        )  # 加载实验数据
        self.ui.page2_cal_grid.clicked.connect(
            functools.partial(Page2.cal_grid, self)
        )  # 计算网格
        self.ui.recoder.clicked.connect(
            functools.partial(Page2.st_resolution_recoder, self)
        )  # 记录
        self.ui.plot_exp_2.clicked.connect(
            functools.partial(Page2.plot_exp, self)
        )  # 绘制实验谱
        self.ui.load_space_time.clicked.connect(
            functools.partial(Page2.load_space_time, self)
        )  # 批量加载时空分辨光谱
        # 单机操作
        self.ui.page2_grid_list.itemSelectionChanged.connect(
            functools.partial(Page2.grid_list_clicked, self)
        )  # 网格列表
        # 双击操作
        self.ui.st_resolution_table.itemDoubleClicked.connect(
            functools.partial(Page2.st_resolution_double_clicked, self)
        )  # 加载库中的项目

        # 列表
        self.ui.page2_selection_list.itemChanged.connect(
            functools.partial(Page2.selection_list_changed, self)
        )  # 选择列表

        # ------------------------------- 第三页 -------------------------------
        # 按钮
        self.ui.td_by_t.clicked.connect(
            functools.partial(Page3.plot_by_times, self)
        )  # 绘制模拟谱
        self.ui.td_by_s.clicked.connect(
            functools.partial(Page3.plot_by_locations, self)
        )  # 绘制模拟谱
        self.ui.td_by_st.clicked.connect(
            functools.partial(Page3.plot_by_space_time, self)
        )  # 绘制模拟谱

        # ------------------------------- 第四页 -------------------------------
        # 按钮
        self.ui.pushButton.clicked.connect(
            functools.partial(Page4.plot_example, self)
        )  # 绘制模拟谱
        # 下拉框
        self.ui.comboBox.activated.connect(
            functools.partial(Page4.comboBox_changed, self)
        )  # 选择列表
        # tree view
        self.ui.treeWidget.itemChanged.connect(
            functools.partial(Page4.tree_item_changed, self)
        )  # 选择列表


if __name__ == '__main__':
    app = QApplication([])
    # window = LoginWindow()  # 启动登陆页面
    window = MainWindow()  # 启动主界面
    window.show()
    app.exec()
