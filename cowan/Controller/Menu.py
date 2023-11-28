import copy
from pathlib import Path

import pandas as pd
from PySide6.QtWidgets import QFileDialog, QDialog, QPushButton, \
    QHBoxLayout, QDoubleSpinBox, QLabel, QVBoxLayout

from main import VerticalLine, MainWindow
from ..Model import PROJECT_PATH, Cowan
from ..Tools import ProgressThread


class Menu(MainWindow):
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

    def set_xrange(self):
        """
        设置波长范围

        """

        def update_xrange():
            def task():
                self.task_thread.progress.emit(0, 'ready to set range ...')
                x_range = [min_input.value(), max_input.value(), step_input.value()]
                num = int((x_range[1] - x_range[0]) / x_range[2])

                # 设置 info --------------------------------
                self.info['x_range'] = x_range
                # 设置第一页的实验谱线 --------------------------------
                self.task_thread.progress.emit(10, 'self.expdata_1 set range ...')
                if self.expdata_1 is not None:
                    self.expdata_1.set_xrange(x_range)
                # 设置 页面上的 Cowan  --------------------------------
                self.task_thread.progress.emit(20, 'self.cowan set range ...')
                if self.cowan is not None:
                    self.cowan.set_xrange(x_range, num)
                # 设置各个 Cowan  --------------------------------
                self.task_thread.progress.emit(30, 'self.cowan_lists set range ...')
                if self.cowan_lists is not None:
                    self.cowan_lists.set_xrange(x_range, num)
                # 设置第二页的实验谱线  --------------------------------
                self.task_thread.progress.emit(40, 'self.expdata_2 set range ...')
                if self.expdata_2 is not None:
                    self.expdata_2.set_xrange(x_range)
                # 设置叠加谱线 --------------------------------
                self.task_thread.progress.emit(50, 'self.simulate set range ...')
                if self.simulate is not None:
                    self.simulate.set_xrange(x_range, num, self.cowan_lists)
                # 设置实验叠加谱线 --------------------------------
                self.task_thread.progress.emit(100, 'self.space_time_resolution set range ...')
                if self.space_time_resolution is not None:
                    self.space_time_resolution.set_xrange(x_range, num, self.cowan_lists)
                # 完成 --------------------------------
                self.ui.statusbar.showMessage('设置范围成功！')

            dialog.close()
            self.task_thread = ProgressThread(dialog_title='正在设置范围...', range_=(0, 100))
            self.task_thread.set_run(task)
            self.task_thread.start()

        dialog = QDialog()
        label = QLabel('请输入范围以及最小步长：')
        # 最大最小值以及步长
        min_input = QDoubleSpinBox()  # 定义
        max_input = QDoubleSpinBox()
        step_input = QDoubleSpinBox()
        spin_box_list = [min_input, max_input, step_input]
        if self.info['x_range'] is not None:
            min_input.setValue(self.info['x_range'][0])  # 设置初始值
            max_input.setValue(self.info['x_range'][1])
            step_input.setValue(self.info['x_range'][2])
        else:
            min_input.setValue(self.expdata_1.x_range[0])  # 设置初始值
            max_input.setValue(self.expdata_1.x_range[1])
            step_input.setValue(0.01)
        layout_input = QHBoxLayout()
        for spin_box in spin_box_list:
            spin_box.setSuffix('nm')  # 设置单位
            spin_box.setDecimals(3)  # 设置精度
            spin_box.setSingleStep(0.010)  # 设置步长
            layout_input.addWidget(spin_box)
        ok_btn = QPushButton('确认')
        cancel_btn = QPushButton('取消')
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
            self.task_thread.progress.emit(0, 'ready to reset range ...')
            self.info['x_range'] = None
            widen_temperature = self.ui.widen_temp.value()

            # 设置第一页的实验谱线
            self.task_thread.progress.emit(10, 'self.expdata_1 reset range ...')
            if self.expdata_1 is not None:
                self.expdata_1.reset_xrange()
            # 设置 页面上的 Cowan
            self.task_thread.progress.emit(20, 'self.cowan reset range ...')
            if self.cowan is not None:
                self.cowan.reset_xrange()
            # 设置各个 Cowan
            self.task_thread.progress.emit(30, 'self.cowan_lists reset range ...')
            if self.cowan_lists is not None:
                self.cowan_lists.reset_xrange()
            # 设置第二页的实验谱线
            self.task_thread.progress.emit(40, 'self.expdata_2 reset range ...')
            if self.expdata_2 is not None:
                self.expdata_2.reset_xrange()
            # 设置叠加谱线
            self.task_thread.progress.emit(50, 'self.simulate reset range ...')
            if self.simulate is not None:
                self.simulate.reset_xrange(self.cowan_lists)
            # 设置实验叠加谱线
            self.task_thread.progress.emit(100, 'self.space_time_resolution reset range ...')
            if self.space_time_resolution is not None:
                self.space_time_resolution.reset_xrange(self.cowan_lists)

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
        names = ['下态序号', '上态序号', '跃迁名称', 'averaged transition energy (nm)', 'width']
        for cowan, _ in self.cowan_lists:
            cowan: Cowan
            ave_w = cowan.cal_data.get_average_wavelength()
            temp_1 = []
            temp_2 = []
            temp_3 = []
            temp_4 = []
            temp_5 = []
            for key, value in ave_w.items():
                temp_1.append(int(key.split('_')[0]))
                temp_2.append(int(key.split('_')[1]))
                temp_3.append(
                    cowan.in36.get_configuration_name(
                        int(key.split('_')[0]),
                        int(key.split('_')[1])
                    )
                )
                temp_4.append(value[0])
                temp_5.append(value[1])
            # 创建数据
            export_data = pd.DataFrame({
                names[0]: temp_1,
                names[1]: temp_2,
                names[2]: temp_3,
                names[3]: temp_4,
                names[4]: temp_5,
            })
            # 对数据进行排序
            export_data.sort_values(by=['下态序号', '上态序号'], inplace=True)
            # 将数据放在DataFrame中
            data_frames[cowan.name] = export_data

            # 存储
            with pd.ExcelWriter(path.joinpath('averaged transition energy.xlsx'), ) as writer:
                for key, value in data_frames.items():
                    value.to_excel(writer, sheet_name=key, index=False)

        self.ui.statusbar.showMessage('导出成功！')
