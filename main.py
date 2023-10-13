import functools
import shelve
import sys

from PySide6.QtWebEngineCore import QWebEnginePage
from PySide6.QtWidgets import QAbstractItemView
from pympler import asizeof

from cowan import *


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


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_login_window()
        self.ui.setupUi(self)
        self.WORKING_PATH = Path.cwd()

        self.project_data: dict = {}
        self.temp_path: str = ''
        self.main_window: Optional[MainWindow] = None

        self.init_UI()

    def init_UI(self):
        # 打开并读取文件
        file_path = self.WORKING_PATH / 'projects.json'
        if not file_path.exists():
            file_path.touch()
            file_path.write_text('{}', encoding='utf-8')
        self.project_data = json.loads(file_path.read_text())

        # 设置列表
        self.update_project_list()
        self.bind_slot()

    def bind_slot(self):
        self.ui.create_project.clicked.connect(self.slot_create_project)
        self.ui.delete_project.clicked.connect(self.slot_delete_project)
        self.ui.back.clicked.connect(self.slot_back)
        self.ui.new_project.clicked.connect(self.slot_new_project)
        self.ui.select_path.clicked.connect(self.slot_select_path)
        self.ui.project_path.textChanged.connect(self.slot_project_path_changed)
        self.ui.project_list.itemDoubleClicked.connect(self.slot_project_path_item_double_clicked)

    def slot_create_project(self):
        # 创建项目
        name = self.ui.project_name.text()
        path_ = self.ui.project_path.text()
        if name == '' or path_ == '':
            QMessageBox.critical(self, '错误', '项目名称和路径不能为空！')
            return
        if name in self.project_data.keys():
            QMessageBox.critical(self, '错误', '项目名称已存在！')
            return
        # 获取项目名称和路径
        path_ = path_.replace('/', '\\')
        self.project_data[name] = {'path': path_}
        self.update_project_list()

        # 如果目录不存在，就创建
        path_ = Path(path_)
        old_path = self.WORKING_PATH / 'init_file'
        shutil.copytree(old_path, path_)

        self.hide()
        self.main_window = MainWindow(path_)
        self.main_window.show()

    def slot_delete_project(self):
        # 删除项目
        key = self.ui.project_list.currentIndex().data()
        path_ = Path(self.project_data[key]['path'])
        shutil.rmtree(path_)
        self.project_data.pop(key)
        self.update_project_list()

    def slot_back(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def slot_new_project(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def slot_select_path(self):
        self.temp_path = QFileDialog.getExistingDirectory(self, '选择项目路径', './')
        self.ui.project_path.setText(self.temp_path)

    def slot_project_path_changed(self):
        name = self.ui.project_path.text().split('/')[-1]
        if name == '':
            name = self.ui.project_path.text().split('/')[-2]
        self.ui.project_name.setText(name)

    def slot_project_path_item_double_clicked(self, index):
        name = index.text()
        path_ = self.project_data[name]['path']
        path_ = Path(path_)
        self.hide()
        self.main_window = MainWindow(path_, True)
        self.main_window.show()

    def update_project_list(self):
        self.ui.project_list.clear()
        self.ui.project_list.addItems(self.project_data.keys())

        # 写入json文件
        file_path = self.WORKING_PATH / 'projects.json'
        file_path.write_text(json.dumps(self.project_data), encoding='utf-8')


class MainWindow(QMainWindow):
    def __init__(self, project_path, load=True):
        super().__init__()
        self.ui = Ui_main_window()
        self.ui.setupUi(self)
        # 设置全局变量
        SET_PROJECT_PATH(project_path)
        self.task_thread = None

        # 设置参考线
        self.v_line = None

        # 第一页使用
        self.atom: Optional[Atom] = Atom(1, 0)
        self.in36: Optional[In36] = In36()
        self.in36.atom = copy.deepcopy(self.atom)
        self.in2: Optional[In2] = In2()
        self.expdata_1: Optional[ExpData] = None

        self.cowan_lists = CowanList()
        self.cowan: Optional[Cowan] = None

        self.expdata_2: Optional[ExpData] = None
        self.simulated_grid: Optional[SimulateGrid] = None
        self.simulate: Optional[SimulateSpectral] = SimulateSpectral()
        self.simulate_page4: Optional[SimulateSpectral] = None
        self.space_time_resolution = SpaceTimeResolution()

        self.info = {
            'x_range': None,
        }

        # 初始化
        self.init()
        self.bind_slot()

        if load:
            self.load_project()
        # else:
        #     self.load_Ge()

        # self.test()
        # self.load_Ge()
        # self.cal_ave_wave()

    def init(self):
        # 设置窗口标题
        self.setWindowTitle(PROJECT_PATH().name)
        # 给元素选择器设置初始值
        self.ui.atomic_num.addItems(list(map(str, ATOM.keys())))
        self.ui.atomic_symbol.addItems(list(zip(*ATOM.values()))[0])
        self.ui.atomic_name.addItems(list(zip(*ATOM.values()))[1])
        # in36组态表格相关设置
        self.ui.in36_configuration_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)  # 设置行选择模式
        self.ui.in36_configuration_view.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents)  # 设置表格列宽自适应
        self.ui.in36_configuration_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.in36_configuration_view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)  # 设置表格不可编辑
        # 设置温度密度网格的相关信息
        self.ui.page2_grid_list.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)  # 设置表格不可编辑
        self.ui.page2_grid_list.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents)  # 设置表格列宽自适应
        self.ui.page2_grid_list.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)  # 设置单选
        # 设置时空分辨表格的相关信息
        self.ui.st_resolution_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)  # 设置表格不可编辑
        self.ui.st_resolution_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents)  # 设置表格列宽自适应
        self.ui.st_resolution_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)  # 设置行选择模式
        self.ui.st_resolution_table.setContextMenuPolicy(Qt.CustomContextMenu)  # 右键菜单
        # 设置右键菜单
        self.ui.run_history_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.selection_list.setContextMenuPolicy(Qt.CustomContextMenu)
        # 隐藏第四页树控件的标题
        self.ui.treeWidget.header().hide()

        # 设置初始页为第一页
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.navigation.setCurrentRow(0)

    def bind_slot(self):
        # 设置左侧列表与右侧页面切换之间的关联
        self.ui.navigation.currentRowChanged.connect(self.ui.stackedWidget.setCurrentIndex)

        # ------------------------------- 菜单栏 -------------------------------
        #  导出组态平均波长
        self.ui.export_configuration_average_wavelength.triggered.connect(
            functools.partial(Menu.export_con_ave_wave, self))
        # 保存项目
        self.ui.save_project.triggered.connect(self.save_project)
        # 显示参考线
        self.ui.show_guides.triggered.connect(functools.partial(Menu.show_guides, self))
        # 重置计算按钮
        self.ui.reset_cal.triggered.connect(lambda: self.ui.page2_cal_grid.setDisabled(False))
        # 退出项目
        self.ui.exit_project.triggered.connect(self.print_memory)
        # 导出数据
        self.ui.export_data.triggered.connect(functools.partial(Menu.export_data, self))
        # 设置x轴范围
        self.ui.set_xrange.triggered.connect(functools.partial(Menu.set_xrange, self))
        # 重置范围
        self.ui.reset_xrange.triggered.connect(functools.partial(Menu.reset_xrange, self))

        # ------------------------------- 第一页 -------------------------------
        # =====>> 下拉框
        # 原子序数改变
        self.ui.atomic_num.activated.connect(functools.partial(Page1.atom_changed, self))
        # 元素符号改变
        self.ui.atomic_symbol.activated.connect(functools.partial(Page1.atom_changed, self))
        # 元素名称改变
        self.ui.atomic_name.activated.connect(functools.partial(Page1.atom_changed, self))
        # 离化度
        self.ui.atomic_ion.activated.connect(functools.partial(Page1.atom_ion_changed, self))
        # =====>> 按钮
        # 加载实验数据
        self.ui.load_exp_data.clicked.connect(functools.partial(Menu.load_exp_data, self))
        # 添加组态
        self.ui.add_configuration.clicked.connect(functools.partial(Page1.add_configuration, self))
        # 加载in36文件
        self.ui.load_in36.clicked.connect(functools.partial(Page1.load_in36, self))
        # 加载in2文件
        self.ui.load_in2.clicked.connect(functools.partial(Page1.load_in2, self))
        # 预览in36
        self.ui.preview_in36.clicked.connect(functools.partial(Page1.preview_in36, self))
        # 预览in2
        self.ui.preview_in2.clicked.connect(functools.partial(Page1.preview_in2, self))
        # 组态下移
        self.ui.configuration_move_down.clicked.connect(functools.partial(Page1.configuration_move_down, self))
        # 组态上移
        self.ui.configuration_move_up.clicked.connect(functools.partial(Page1.configuration_move_up, self))
        # 运行Cowan
        self.ui.run_cowan.clicked.connect(functools.partial(Page1.run_cowan, self))
        # =====>> 单选框
        # 自动生成 in36 组态
        self.ui.auto_write_in36.clicked.connect(functools.partial(Page1.auto_write_in36, self))
        # 手动输入 in36 组态
        self.ui.manual_write_in36.clicked.connect(functools.partial(Page1.manual_write_in36, self))
        # 线状谱展宽成gauss
        self.ui.gauss.clicked.connect(
            lambda: self.ui.web_cal_widen.load(QUrl.fromLocalFile(self.cowan.cal_data.widen_all.plot_path_gauss)))
        # 线状谱展宽成crossP
        self.ui.crossP.clicked.connect(
            lambda: self.ui.web_cal_widen.load(QUrl.fromLocalFile(self.cowan.cal_data.widen_all.plot_path_cross_P)))
        # 线状谱展宽成crossNP
        self.ui.crossNP.clicked.connect(
            lambda: self.ui.web_cal_widen.load(QUrl.fromLocalFile(self.cowan.cal_data.widen_all.plot_path_cross_NP)))
        # =====>> 输入框
        # in2 的斯莱特系数改变
        self.ui.in2_11_e.valueChanged.connect(functools.partial(Page1.in2_11_e_value_changed, self))  # in2 11 e
        # 偏移
        self.ui.update_offect.clicked.connect(functools.partial(Page1.re_widen, self))  # 偏移
        # =====>> 右键菜单
        # in36 组态表格
        self.ui.in36_configuration_view.customContextMenuRequested.connect(
            functools.partial(Page1.in36_configuration_view_right_menu, self))
        # 运行历史
        self.ui.run_history_list.customContextMenuRequested.connect(
            functools.partial(Page1.run_history_list_right_menu, self))
        # 选择列表
        self.ui.selection_list.customContextMenuRequested.connect(
            functools.partial(Page1.selection_list_right_menu, self))
        # =====>> 双击操作
        # 加载库中的项目
        self.ui.run_history_list.itemDoubleClicked.connect(functools.partial(Page1.load_history, self))

        # ------------------------------- 第二页 -------------------------------
        # =====>> 按钮
        # 绘制模拟谱
        self.ui.page2_plot_spectrum.clicked.connect(functools.partial(Page2.plot_spectrum, self))
        # 加载实验数据
        self.ui.page2_load_exp_data.clicked.connect(functools.partial(Page2.load_exp_data, self))
        # 计算网格
        self.ui.page2_cal_grid.clicked.connect(functools.partial(Page2.cal_grid, self))
        # 记录
        self.ui.recoder.clicked.connect(functools.partial(Page2.st_resolution_recoder, self))
        # 绘制实验谱
        self.ui.plot_exp_2.clicked.connect(functools.partial(Page2.plot_exp, self))
        # 批量加载时空分辨光谱
        self.ui.load_space_time.clicked.connect(functools.partial(Page2.load_space_time, self))
        # 选择峰位置
        self.ui.choose_peaks.clicked.connect(functools.partial(Page2.choose_peaks, self))
        # 显示离子丰度
        self.ui.show_abu.clicked.connect(functools.partial(Page2.show_abu, self))
        # Cowan对象更新
        self.ui.page2_cowan_obj_update.clicked.connect(functools.partial(Page2.cowan_obj_update, self))
        # =====>> 复选框
        # 切换特征峰位置是否显示
        self.ui.show_peaks.toggled.connect(functools.partial(Page2.plot_spectrum, self))
        # =====>> 单击操作
        # 加载网格中的模拟谱线
        self.ui.page2_grid_list.itemSelectionChanged.connect(functools.partial(Page2.grid_list_clicked, self))  # 网格列表
        # =====>> 双击操作
        # 加载库中的项目
        self.ui.st_resolution_table.itemDoubleClicked.connect(functools.partial(Page2.st_resolution_clicked, self))
        # =====>> 列表
        # 选择列表该百年
        self.ui.page2_selection_list.itemChanged.connect(functools.partial(Page2.selection_list_changed, self))
        # =====>> 右键菜单
        self.ui.st_resolution_table.customContextMenuRequested.connect(
            functools.partial(Page2.st_resolution_right_menu, self))  # 时空分辨表格的右键菜单

        # ------------------------------- 第三页 -------------------------------
        # 按钮
        self.ui.td_by_t.clicked.connect(functools.partial(Page3.plot_by_times, self))
        self.ui.td_by_s.clicked.connect(functools.partial(Page3.plot_by_locations, self))
        self.ui.td_by_st.clicked.connect(functools.partial(Page3.plot_by_space_time, self))

        # ------------------------------- 第四页 -------------------------------
        # 按钮
        self.ui.page4_con_contribution.clicked.connect(functools.partial(Page4.plot_con_contribution, self))  # 组态贡献
        self.ui.page4_ion_contribution.clicked.connect(functools.partial(Page4.plot_ion_contribution, self))  # 组态贡献
        # 下拉框
        self.ui.comboBox.activated.connect(functools.partial(Page4.comboBox_changed, self))  # 选择列表
        # tree view
        self.ui.treeWidget.itemClicked.connect(functools.partial(Page4.tree_item_changed, self))  # 选择列表

    def test(self):
        pass
        SET_PROJECT_PATH(Path('F:/Cowan/Al'))
        delta = {3: 0.05, 4: -0.04, 5: 0.0, 6: 0.05}

        for i in range(3, 7):
            self.in36 = In36()
            self.in36.read_from_file(PROJECT_PATH() / f'in36_{i}')
            self.atom = copy.deepcopy(self.in36.atom)
            self.in2 = In2()
            self.expdata_1 = ExpData(PROJECT_PATH() / './exp_data.csv')
            self.cowan = Cowan(self.in36, self.in2, f'Al_{i}', self.expdata_1, 1)
            cowan_r = CowanThread(self.cowan)
            cowan_r.start()
            cowan_r.wait()
            cowan_r.update_origin()
            self.cowan.cal_data.widen_all.delta_lambda = delta[i]
            self.cowan.cal_data.widen_all.widen(25.6, False)
            self.cowan_lists.add_history(self.cowan)
        self.cowan_lists.chose_cowan = list(self.cowan_lists.cowan_run_history.keys())
        self.cowan_lists.add_or_not = [True for _ in range(len(self.cowan_lists.chose_cowan))]

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
        self.expdata_2 = ExpData(PROJECT_PATH() / 'exp_data.csv')
        # 更新界面
        self.ui.page2_exp_data_path_name.setText(self.expdata_2.filepath.name)
        # 更新谱峰个数
        # functools.partial(UpdatePage2.update_characteristic_peaks, self)()

        # 时空分辨表格
        functools.partial(UpdatePage2.update_space_time_table, self)()

        # --------------- 第三页
        functools.partial(UpdatePage3.update_space_time_combobox, self)()

        # --------------- 第四页
        functools.partial(UpdatePage4.update_space_time_combobox, self)()

    def load_Ge(self):
        folder_path = Path(r'E:\研究生工作\科研工作\2023_08_08_Ge等离子体光谱\计算数据')
        self.expdata_1 = ExpData(PROJECT_PATH() / './0.4mm_30ns.csv')
        for path in folder_path.iterdir():
            self.in36 = In36()
            self.in36.read_from_file(path / f'in36')
            self.atom = copy.deepcopy(self.in36.atom)
            self.in2 = In2()
            self.in2.read_from_file(path / f'in2')
            name = path.name.split('Ge')[-1].strip('+')
            self.cowan = Cowan(self.in36, self.in2, f'Ge_{name}', self.expdata_1, 1)
            self.cowan.cal_data = CalData(f'Ge_{name}', self.expdata_1)
            self.cowan.cal_data.widen_all.widen(25.6, False)
            self.cowan_lists.add_history(self.cowan)
            print(f'加载{self.cowan.name}')
        self.cowan_lists.chose_cowan = list(self.cowan_lists.cowan_run_history.keys())
        self.cowan_lists.add_or_not = [True for _ in range(len(self.cowan_lists.chose_cowan))]

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
        self.expdata_2 = ExpData(Path(r'F:\Cowan\Ge\0.4mm.csv'))
        # 更新界面
        self.ui.page2_exp_data_path_name.setText(self.expdata_2.filepath.name)
        # 时空分辨表格
        functools.partial(UpdatePage2.update_space_time_table, self)()
        # --------------- 第三页
        functools.partial(UpdatePage3.update_space_time_combobox, self)()
        # --------------- 第四页
        functools.partial(UpdatePage4.update_space_time_combobox, self)()

    def cal_ave_wave(self):
        SET_PROJECT_PATH(Path(r'F:/Cowan/Ni'))
        self.expdata_1 = ExpData(PROJECT_PATH() / './0.4mm_30ns.csv')
        data_frames = {}
        for path in PROJECT_PATH().joinpath('cal_result').iterdir():
            if 'Ni' not in path.name:
                continue
            self.in36 = In36()
            self.in36.read_from_file(path / f'in36')
            self.atom = copy.deepcopy(self.in36.atom)
            self.in2 = In2()
            self.in2.read_from_file(path / f'in2')
            name = path.name
            self.cowan = Cowan(self.in36, self.in2, name, self.expdata_1, 1)
            self.cowan.cal_data = CalData(name, self.expdata_1)
            self.cowan.cal_data.widen_all.widen(25.6, False)
            self.cowan_lists.add_history(self.cowan)
            ave_w = self.cowan.cal_data.get_average_wavelength()
            temp_1 = []
            temp_2 = []
            temp_3 = []
            temp_4 = []
            names = ['下态序号', '上态序号', '跃迁名称', '平均波长(nm)']
            for key, value in ave_w.items():
                a = int(key.split('_')[0])
                b = int(key.split('_')[1])
                c = self.cowan.in36.get_configuration_name(a, b)
                d = value
                temp_1.append(a)
                temp_2.append(b)
                temp_3.append(c)
                temp_4.append(d)
            data_frames[self.cowan.name] = (
                pd.DataFrame({names[0]: temp_1, names[1]: temp_2, names[2]: temp_3, names[3]: temp_4}))
            print(f'加载{self.cowan.name}')
        self.cowan_lists.chose_cowan = list(self.cowan_lists.cowan_run_history.keys())
        self.cowan_lists.add_or_not = [True for _ in range(len(self.cowan_lists.chose_cowan))]
        with pd.ExcelWriter('tb.xlsx', ) as writer:
            for key, value in data_frames.items():
                if key == 'Ni_12':
                    name = 'Ni_11_extra'
                else:
                    name = key
                value.to_excel(writer, sheet_name=name, index=False)

    def save_project(self):
        def task():
            obj_info = shelve.open(PROJECT_PATH().joinpath('.cowan/obj_info').as_posix())
            # 第一页
            self.task_thread.progress.emit(5, 'atom')
            obj_info['atom'] = self.atom
            self.task_thread.progress.emit(10, 'in36')
            obj_info['in36'] = self.in36
            self.task_thread.progress.emit(15, 'in2')
            obj_info['in2'] = self.in2
            self.task_thread.progress.emit(20, 'expdata_1')
            obj_info['expdata_1'] = self.expdata_1
            self.task_thread.progress.emit(30, 'cowan_lists')
            obj_info['cowan_lists'] = self.cowan_lists
            self.task_thread.progress.emit(35, 'cowan')
            obj_info['cowan'] = self.cowan
            self.task_thread.progress.emit(35, 'cowan')
            obj_info['info'] = self.info
            # 第二页
            self.task_thread.progress.emit(45, 'expdata_2')
            obj_info['expdata_2'] = self.expdata_2
            self.task_thread.progress.emit(50, 'simulate')
            obj_info['simulate'] = self.simulate
            self.task_thread.progress.emit(80, 'simulated_grid')
            obj_info['simulated_grid'] = self.simulated_grid
            self.task_thread.progress.emit(90, 'space_time_resolution')
            obj_info['space_time_resolution'] = self.space_time_resolution
            # 第四页
            obj_info['simulate_page4'] = self.simulate_page4
            self.task_thread.progress.emit(100, 'space_time_resolution')

            self.ui.statusbar.showMessage('保存成功！')

        self.task_thread = ProgressThread(dialog_title='正在保存项目，请稍后...', range_=(0, 100))
        self.task_thread.set_run(task)
        self.task_thread.progress_dialog.set_prompt_words('正在保存xxx变量...')
        self.task_thread.start()

    def load_project(self):
        obj_info = shelve.open(PROJECT_PATH().joinpath('.cowan/obj_info').as_posix())
        try:
            obj_info['atom']
        except KeyError:
            warnings.warn('初始化文件不存在！', UserWarning)
            return
        # 第一页
        self.atom = obj_info['atom']
        self.in36 = obj_info['in36']
        self.in2 = obj_info['in2']
        self.expdata_1 = obj_info['expdata_1']
        self.cowan = obj_info['cowan']
        self.cowan_lists = obj_info['cowan_lists']
        self.info = obj_info['info']
        # 第二页
        self.expdata_2 = obj_info['expdata_2']
        self.simulate = obj_info['simulate']
        self.simulated_grid = obj_info['simulated_grid']
        self.space_time_resolution = obj_info['space_time_resolution']
        # 第四页
        self.simulate_page4 = obj_info['simulate_page4']
        obj_info.close()

        # 更新界面
        # 第一页 =================================================
        functools.partial(UpdatePage1.update_page, self)()

        # 第二页 =================================================
        functools.partial(UpdatePage2.update_page, self)()

        # 第三页 =================================================
        functools.partial(UpdatePage3.update_space_time_combobox, self)()

        # 第四页 =================================================
        functools.partial(UpdatePage4.update_space_time_combobox, self)()

    @staticmethod
    def print_memory():
        print('{:>22} {:>15.2f} [GB]'.format('总大小：',
                                             asizeof.asizeof(window) / 1024 ** 3))

    def closeEvent(self, event):
        # dialog = self.save_project()
        # dialog.exec()
        sys.exit()
        # pass


if __name__ == '__main__':
    app = QApplication([])
    window = LoginWindow()  # 启动登陆页面
    # window = MainWindow(Path('F:/Cowan/Test'), False)  # 启动主界面
    # window = MainWindow(Path('F:/Cowan/Ge_new'), False)  # 启动主界面
    # window = MainWindow(Path('F:/Cowan/Ni'), False)  # 启动主界面
    window.show()
    app.exec()
