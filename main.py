import copy
import functools
import json
import shelve
import shutil
import sys
import warnings
import traceback
from pathlib import Path
from typing import Optional

from pympler import asizeof
from packaging.version import Version
from PySide6.QtCore import Qt, QUrl
from PySide6.QtWidgets import QAbstractItemView, QWidget, QMessageBox, QFileDialog, QMainWindow, QHeaderView, \
    QApplication

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
        """
        打开文件并读取项目列表，加载再界面上

        Returns:

        """
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
        # self.ui.project_path.textChanged.connect(self.slot_project_path_changed)
        self.ui.project_name.textChanged.connect(self.slot_project_name_changed)
        self.ui.project_list.itemDoubleClicked.connect(self.slot_project_path_item_double_clicked)

    def slot_create_project(self):
        """
        创建项目

        Returns:

        """
        # 创建项目
        name = self.ui.project_name.text()
        path_ = self.ui.project_path.text()
        # 判断项目名称和路径是否为空
        if name == '' or path_ == '':
            QMessageBox.critical(self, '错误', '项目名称或路径不能为空！')
            return
        # 判断项目名称和路径是否已存在
        if name in self.project_data.keys():
            QMessageBox.critical(self, '错误', '项目名称已存在！')
            return
        # 判断项目路径是否已存在
        if Path(path_).exists():
            QMessageBox.critical(self, '错误', '项目路径已存在，请删除后再进行创建！')
            return

        # 获取项目名称和路径
        path_ = path_.replace('/', '\\')
        self.project_data[name] = {'path': path_}
        self.update_project_list()

        # 将init_file文件夹直接复制为项目文件夹
        path_ = Path(path_)
        old_path = self.WORKING_PATH / 'init_file'
        shutil.copytree(old_path, path_)

        self.hide()
        self.main_window = MainWindow(path_)
        self.main_window.show()

    def slot_delete_project(self):
        """
        删除项目

        Returns:

        """
        key = self.ui.project_list.currentIndex().data()  # 要删除的项目名称
        path_ = Path(self.project_data[key]['path'])  # 要删除的项目路径
        if path_.exists():  # 如果存在就删除
            shutil.rmtree(path_)
        else:
            warnings.warn('项目文件夹不存在！')
        self.project_data.pop(key)
        self.update_project_list()

    def slot_back(self):
        """
        返回首页

        Returns:

        """
        self.ui.stackedWidget.setCurrentIndex(0)

    def slot_new_project(self):
        """
        进入项目创建页面

        Returns:

        """
        self.ui.stackedWidget.setCurrentIndex(1)

    def slot_select_path(self):
        """
        选择项目路径

        Returns:

        """
        self.temp_path = QFileDialog.getExistingDirectory(self, '选择项目路径', './') + '/'
        self.ui.project_path.setText(self.temp_path)

    def slot_project_name_changed(self):
        self.ui.project_path.setText(self.temp_path + self.ui.project_name.text())

    # def slot_project_path_changed(self):
    #     name = self.ui.project_path.text().split('/')[-1]
    #     if name == '':
    #         name = self.ui.project_path.text().split('/')[-2]
    #     self.ui.project_name.setText(name)

    def slot_project_path_item_double_clicked(self, index):
        """
        双击项目列表中的项目，打开项目

        Args:
            index: 双击的序号

        Returns:

        """
        name = index.text()
        path_ = self.project_data[name]['path']
        path_ = Path(path_)  # 项目路径
        # 如果项目文件不存在，就删除项目
        if not path_.exists():
            reply = QMessageBox.question(self, 'Warning', '项目路径不存在，是否删除该项目？',
                                         QMessageBox.StandardButton.Yes,
                                         QMessageBox.StandardButton.No
                                         )
            if reply == QMessageBox.StandardButton.Yes:
                self.project_data.pop(name)
                self.update_project_list()
            return

        self.hide()
        # 打开项目
        try:
            self.main_window = MainWindow(path_, True)
        except Exception as e:
            QMessageBox.critical(self, '错误', f'{e}')
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
            traceback.print_exc()
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        # 如果窗口对象没有创建成功
        if self.main_window is None:
            self.show()
            QMessageBox.critical(self, '错误', f'项目打开失败，请联系管理员解决！')
            return
        else:
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
        # 导出窗口
        self.export_data_window = None

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
        self.cowan_page5: Optional[Cowan] = None

        self.info = {
            'x_range': None,  # example: [2, 8, 0.01] [<最小波长>, <最大波长>, <最小步长>]
            'version': '1.0.3',  # example: '1.0.0'
        }

        print('当前软件版本：{}'.format(self.info['version']))

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
        # 导出画图数据
        self.ui.export_plot_data.triggered.connect(functools.partial(Menu.switch_export_data, self))
        # 展示导出窗口
        self.ui.export_data_window.triggered.connect(functools.partial(ExportData.show_export_data_window, self))

        # ------------------------------- 第一页 -------------------------------
        # =====>> 下拉框
        # 原子序数改变
        self.ui.atomic_num.activated.connect(functools.partial(LineIdentification.atom_changed, self))
        # 元素符号改变
        self.ui.atomic_symbol.activated.connect(functools.partial(LineIdentification.atom_changed, self))
        # 元素名称改变
        self.ui.atomic_name.activated.connect(functools.partial(LineIdentification.atom_changed, self))
        # 离化度
        self.ui.atomic_ion.activated.connect(functools.partial(LineIdentification.atom_ion_changed, self))
        # =====>> 按钮
        # 加载实验数据
        self.ui.load_exp_data.clicked.connect(functools.partial(LineIdentification.load_exp_data, self))
        # 重新绘制实验谱线
        self.ui.redraw_exp_data.clicked.connect(functools.partial(LineIdentification.redraw_exp_data, self))
        # 添加组态
        self.ui.add_configuration.clicked.connect(functools.partial(LineIdentification.add_configuration, self))
        # 加载in36文件
        self.ui.load_in36.clicked.connect(functools.partial(LineIdentification.load_in36, self))
        # 加载in2文件
        self.ui.load_in2.clicked.connect(functools.partial(LineIdentification.load_in2, self))
        # 预览in36
        self.ui.preview_in36.clicked.connect(functools.partial(LineIdentification.preview_in36, self))
        # 预览in2
        self.ui.preview_in2.clicked.connect(functools.partial(LineIdentification.preview_in2, self))
        # 组态下移
        self.ui.configuration_move_down.clicked.connect(
            functools.partial(LineIdentification.configuration_move_down, self))
        # 组态上移
        self.ui.configuration_move_up.clicked.connect(functools.partial(LineIdentification.configuration_move_up, self))
        # 运行Cowan
        self.ui.run_cowan.clicked.connect(functools.partial(LineIdentification.run_cowan, self))
        # =====>> 单选框
        # 自动生成 in36 组态
        self.ui.auto_write_in36.clicked.connect(functools.partial(LineIdentification.auto_write_in36, self))
        # 手动输入 in36 组态
        self.ui.manual_write_in36.clicked.connect(functools.partial(LineIdentification.manual_write_in36, self))
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
        self.ui.in2_11_e.valueChanged.connect(
            functools.partial(LineIdentification.in2_11_e_value_changed, self))  # in2 11 e
        # 偏移
        self.ui.update_offect.clicked.connect(functools.partial(LineIdentification.re_widen, self))  # 偏移
        # =====>> 右键菜单
        # in36 组态表格
        self.ui.in36_configuration_view.customContextMenuRequested.connect(
            functools.partial(LineIdentification.in36_configuration_view_right_menu, self))
        # 运行历史
        self.ui.run_history_list.customContextMenuRequested.connect(
            functools.partial(LineIdentification.run_history_list_right_menu, self))
        # 选择列表
        self.ui.selection_list.customContextMenuRequested.connect(
            functools.partial(LineIdentification.selection_list_right_menu, self))
        # =====>> 双击操作
        # 加载库中的项目
        self.ui.run_history_list.itemDoubleClicked.connect(functools.partial(LineIdentification.load_history, self))

        # ------------------------------- 第二页 -------------------------------
        # =====>> 按钮
        # 绘制模拟谱
        self.ui.page2_plot_spectrum.clicked.connect(functools.partial(SpectralSimulation.plot_spectrum, self))
        # 加载实验数据
        self.ui.page2_load_exp_data.clicked.connect(functools.partial(SpectralSimulation.load_exp_data, self))
        # 计算网格
        self.ui.page2_cal_grid.clicked.connect(functools.partial(SpectralSimulation.cal_grid, self))
        # 记录
        self.ui.recoder.clicked.connect(functools.partial(SpectralSimulation.st_resolution_recoder, self))
        # 绘制实验谱
        self.ui.plot_exp_2.clicked.connect(functools.partial(SpectralSimulation.plot_exp, self))
        # 批量加载时空分辨光谱
        self.ui.load_space_time.clicked.connect(functools.partial(SpectralSimulation.load_space_time, self))
        # 选择峰位置
        self.ui.choose_peaks.clicked.connect(functools.partial(SpectralSimulation.choose_peaks, self))
        # 显示离子丰度
        self.ui.show_abu.clicked.connect(functools.partial(SpectralSimulation.show_abu, self))
        # Cowan对象更新
        self.ui.page2_cowan_obj_update.clicked.connect(functools.partial(SpectralSimulation.cowan_obj_update, self))
        # =====>> 复选框
        # 切换特征峰位置是否显示
        self.ui.show_peaks.toggled.connect(functools.partial(SpectralSimulation.plot_spectrum, self))
        # =====>> 单击操作
        # 加载网格中的模拟谱线
        self.ui.page2_grid_list.itemSelectionChanged.connect(
            functools.partial(SpectralSimulation.grid_list_clicked, self))  # 网格列表
        # =====>> 双击操作
        # 加载库中的项目
        self.ui.st_resolution_table.itemDoubleClicked.connect(
            functools.partial(SpectralSimulation.st_resolution_clicked, self))
        # =====>> 列表
        # 选择列表该百年
        self.ui.page2_selection_list.itemChanged.connect(
            functools.partial(SpectralSimulation.selection_list_changed, self))
        # =====>> 右键菜单
        self.ui.st_resolution_table.customContextMenuRequested.connect(
            functools.partial(SpectralSimulation.st_resolution_right_menu, self))  # 时空分辨表格的右键菜单

        # ------------------------------- 第三页 -------------------------------
        # 按钮
        self.ui.td_by_t.clicked.connect(functools.partial(EvolutionaryProcess.plot_by_times, self))
        self.ui.td_by_s.clicked.connect(functools.partial(EvolutionaryProcess.plot_by_locations, self))
        self.ui.td_by_st.clicked.connect(functools.partial(EvolutionaryProcess.plot_by_space_time, self))

        # ------------------------------- 第四页 -------------------------------
        # 按钮
        self.ui.page4_con_contribution.clicked.connect(
            functools.partial(ConfigurationContribution.plot_con_contribution, self))  # 组态贡献
        self.ui.page4_ion_contribution.clicked.connect(
            functools.partial(ConfigurationContribution.plot_ion_contribution, self))  # 组态贡献
        # 下拉框
        self.ui.comboBox.activated.connect(functools.partial(ConfigurationContribution.comboBox_changed, self))  # 选择列表
        # tree view
        self.ui.treeWidget.itemClicked.connect(
            functools.partial(ConfigurationContribution.tree_item_changed, self))  # 选择列表

        # ------------------------------- 第五页 -------------------------------
        # 下拉框
        self.ui.page5_ion_select.activated.connect(functools.partial(DataStatistics.ion_selected, self))  # 选择列表
        # 导出数据
        self.ui.export_static_table.clicked.connect(functools.partial(ExportData.export_statistics_table, self))

    def save_project(self):
        def task():
            obj_info = shelve.open(PROJECT_PATH().joinpath('.cowan/obj_info').as_posix(), flag='n')
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
            self.task_thread.progress.emit(95, 'simulate_page4')
            obj_info['simulate_page4'] = self.simulate_page4

            # 第五页
            self.task_thread.progress.emit(95, 'cowan_page5')
            obj_info['cowan_page5'] = self.cowan_page5

            # 总共
            obj_info['info'] = self.info
            # -----------------------------------------------------------
            self.task_thread.progress.emit(100, 'All saved!')
            self.ui.statusbar.showMessage('保存成功！')

        self.task_thread = ProgressThread(dialog_title='正在保存项目，请稍后...', range_=(0, 100))
        self.task_thread.set_run(task)
        self.task_thread.progress_dialog.set_prompt_words('正在保存xxx变量...')
        self.task_thread.start()

    def load_project(self):
        def load_info():
            info = obj_info['info']
            self.info['x_range'] = info['x_range']
            self.info['version'] = info['version']

        # 函数定义结束 ------------------------------------------------------

        if not PROJECT_PATH().joinpath('.cowan/obj_info.dat').exists():
            return
        # 读取初始化文件
        obj_info = shelve.open(PROJECT_PATH().joinpath('.cowan/obj_info').as_posix())
        self.update_version(obj_info)
        # ---------------------------------------------------------
        # 总共
        self.info = obj_info['info']
        # 第一页
        self.atom = obj_info['atom']
        self.in36 = obj_info['in36']
        self.in2 = obj_info['in2']
        self.expdata_1 = obj_info['expdata_1']
        self.cowan = obj_info['cowan']
        self.cowan_lists = obj_info['cowan_lists']
        # 第二页
        self.expdata_2 = obj_info['expdata_2']
        self.simulate = obj_info['simulate']
        self.simulated_grid = obj_info['simulated_grid']
        self.space_time_resolution = obj_info['space_time_resolution']
        # 第四页
        self.simulate_page4 = obj_info['simulate_page4']
        # 第五页
        self.cowan_page5 = obj_info['cowan_page5']

        # ---------------------------------------------------------
        obj_list = [
            (self.atom, 'atom'), (self.in36, 'in36'), (self.in2, 'in2'), (self.expdata_1, 'expdata_1'),
            (self.cowan, 'cowan'), (self.cowan_lists, 'cowan_lists'), (self.expdata_2, 'expdata_2'),
            (self.simulate, 'simulate'), (self.simulated_grid, 'simulated_grid'),
            (self.space_time_resolution, 'space_time_resolution'), (self.simulate_page4, 'simulate_page4')
        ]
        load_info()
        for obj, name in obj_list:
            if obj is not None:
                obj.load_class(obj_info[name])
        # ---------------------------------------------------------
        obj_info.close()

        # 更新界面
        # 第一页 =================================================
        functools.partial(UpdateLineIdentification.update_page, self)()

        # 第二页 =================================================
        functools.partial(UpdateSpectralSimulation.update_page, self)()

        # 第三页 =================================================
        functools.partial(UpdateEvolutionaryProcess.update_space_time_combobox, self)()

        # 第四页 =================================================
        functools.partial(UpdateConfigurationContribution.update_space_time_combobox, self)()

    @staticmethod
    def print_memory():
        print('{:>22} {:>15.2f} [GB]'.format('总大小：',
                                             asizeof.asizeof(window) / 1024 ** 3))

    @staticmethod
    def update_version(obj_info):
        if 'version' not in obj_info['info'].keys():
            print('数据版本：无版本')
        else:
            print('数据版本：{}'.format(obj_info['info']['version']))

        # 无版本号 > 1.0.0 ---------------------------------------------------
        if 'version' not in obj_info['info'].keys():
            print('正在进行版本升级 [无版本号 > 1.0.0]')
            project_info = obj_info['info']
            # 1. 添加版本号
            project_info['version'] = '1.0.0'
            print('版本号更新完成')
            # 2. 更新了自定义波长的记录方式
            if project_info['x_range'] is not None:
                if len(project_info['x_range']) == 2:
                    project_info['x_range'].append(0.01)
            print('更新了自定义波长的记录方式')

            # 更新 >>>>>>>>>>>>>>>>>>
            obj_info.update({'info': project_info})
            print('版本升级完成！')

        # 1.0.0 > 1.0.1 ---------------------------------------------------
        if Version(obj_info['info']['version']) < Version('1.0.1'):
            print('正在进行版本升级 [1.0.0 > 1.0.1]')
            project_info = obj_info['info']
            # 1. 添加版本号
            project_info['version'] = '1.0.1'
            print('版本号更新完成')
            # 2. 更新了数据统计功能，主窗口类添加 cowan_page5 属性
            if 'cowan_page5' not in obj_info.keys():
                obj_info['cowan_page5'] = None
            print('更新了数据统计功能')

            # 更新 >>>>>>>>>>>>>>>>>>
            obj_info.update({'info': project_info})
            print('版本升级完成！')
        # 1.0.1 > 1.0.2 ---------------------------------------------------
        if Version(obj_info['info']['version']) < Version('1.0.2'):
            print('正在进行版本升级 [1.0.1 > 1.0.2]')
            project_info = obj_info['info']
            # 1. 添加版本号
            project_info['version'] = '1.0.2'
            print('版本号更新完成')
            # 2. 添加了第一页和第二页画图时数据的导出功能
            if not PROJECT_PATH().joinpath('plot_data').exists():
                old_path = Path.cwd().joinpath('init_file/plot_data')
                path_ = PROJECT_PATH().joinpath('plot_data')
                shutil.copytree(old_path, path_)
            print('添加了第一页和第二页画图时数据的导出功能')

            # 更新 >>>>>>>>>>>>>>>>>>
            obj_info.update({'info': project_info})
            print('版本升级完成！')
        # 1.0.2 > 1.0.3 ---------------------------------------------------
        if Version(obj_info['info']['version']) < Version('1.0.3'):
            print('正在进行版本升级 [1.0.2 > 1.0.3]')
            project_info = obj_info['info']
            # 1. 添加版本号
            project_info['version'] = '1.0.3'
            print('版本号更新完成')
            # 2. 给widenpart添加了grouped_data属性
            print('给widenpart添加了grouped_data属性')
            # 更新 >>>>>>>>>>>>>>>>>>
            obj_info.update({'info': project_info})
            print('版本升级完成！')

    def closeEvent(self, event):
        # dialog = self.save_project()
        # dialog.exec()
        sys.exit()
        # pass


if __name__ == '__main__':
    app = QApplication([])
    window = LoginWindow()  # 启动登陆页面
    window.show()
    app.exec()
