# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DataShowWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QStackedWidget,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_DataShow(object):
    def setupUi(self, DataShow):
        if not DataShow.objectName():
            DataShow.setObjectName(u"DataShow")
        DataShow.resize(851, 598)
        self.horizontalLayout = QHBoxLayout(DataShow)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.widget = QWidget(DataShow)
        self.widget.setObjectName(u"widget")
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.cowan_change = QPushButton(self.widget)
        self.cowan_change.setObjectName(u"cowan_change")
        self.cowan_change.setMinimumSize(QSize(100, 70))

        self.verticalLayout.addWidget(self.cowan_change)

        self.all_cowan_change = QPushButton(self.widget)
        self.all_cowan_change.setObjectName(u"all_cowan_change")
        self.all_cowan_change.setMinimumSize(QSize(100, 70))

        self.verticalLayout.addWidget(self.all_cowan_change)

        self.st_change = QPushButton(self.widget)
        self.st_change.setObjectName(u"st_change")
        self.st_change.setMinimumSize(QSize(100, 70))

        self.verticalLayout.addWidget(self.st_change)

        self.all_st_change = QPushButton(self.widget)
        self.all_st_change.setObjectName(u"all_st_change")
        self.all_st_change.setMinimumSize(QSize(100, 70))

        self.verticalLayout.addWidget(self.all_st_change)

        self.verticalSpacer = QSpacerItem(20, 224, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout.addWidget(self.widget)

        self.stackedWidget = QStackedWidget(DataShow)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.cowan = QWidget()
        self.cowan.setObjectName(u"cowan")
        self.verticalLayout_5 = QVBoxLayout(self.cowan)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(self.cowan)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label)

        self.choose_ion = QComboBox(self.cowan)
        self.choose_ion.setObjectName(u"choose_ion")

        self.horizontalLayout_2.addWidget(self.choose_ion)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout_5.addLayout(self.horizontalLayout_2)

        self.ion_info = QLabel(self.cowan)
        self.ion_info.setObjectName(u"ion_info")

        self.verticalLayout_5.addWidget(self.ion_info)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.groupBox_2 = QGroupBox(self.cowan)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_4 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.init_res_overall = QCheckBox(self.groupBox_2)
        self.init_res_overall.setObjectName(u"init_res_overall")
        self.init_res_overall.setChecked(True)

        self.verticalLayout_4.addWidget(self.init_res_overall)

        self.line = QFrame(self.groupBox_2)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.line)

        self.line_over_all = QCheckBox(self.groupBox_2)
        self.line_over_all.setObjectName(u"line_over_all")
        self.line_over_all.setChecked(True)

        self.verticalLayout_4.addWidget(self.line_over_all)

        self.gauss_overall = QCheckBox(self.groupBox_2)
        self.gauss_overall.setObjectName(u"gauss_overall")
        self.gauss_overall.setChecked(True)

        self.verticalLayout_4.addWidget(self.gauss_overall)

        self.cross_np_overall = QCheckBox(self.groupBox_2)
        self.cross_np_overall.setObjectName(u"cross_np_overall")
        self.cross_np_overall.setChecked(True)

        self.verticalLayout_4.addWidget(self.cross_np_overall)

        self.cross_p_overall = QCheckBox(self.groupBox_2)
        self.cross_p_overall.setObjectName(u"cross_p_overall")
        self.cross_p_overall.setChecked(True)

        self.verticalLayout_4.addWidget(self.cross_p_overall)

        self.verticalSpacer_2 = QSpacerItem(20, 166, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_2)

        self.export_1_overall = QPushButton(self.groupBox_2)
        self.export_1_overall.setObjectName(u"export_1_overall")

        self.verticalLayout_4.addWidget(self.export_1_overall)


        self.horizontalLayout_4.addWidget(self.groupBox_2)

        self.groupBox_3 = QGroupBox(self.cowan)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_3 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.init_res_con = QCheckBox(self.groupBox_3)
        self.init_res_con.setObjectName(u"init_res_con")
        self.init_res_con.setChecked(True)

        self.verticalLayout_3.addWidget(self.init_res_con)

        self.line_2 = QFrame(self.groupBox_3)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_3.addWidget(self.line_2)

        self.line_con = QCheckBox(self.groupBox_3)
        self.line_con.setObjectName(u"line_con")
        self.line_con.setChecked(True)

        self.verticalLayout_3.addWidget(self.line_con)

        self.gauss_con = QCheckBox(self.groupBox_3)
        self.gauss_con.setObjectName(u"gauss_con")
        self.gauss_con.setChecked(True)

        self.verticalLayout_3.addWidget(self.gauss_con)

        self.cross_np_con = QCheckBox(self.groupBox_3)
        self.cross_np_con.setObjectName(u"cross_np_con")
        self.cross_np_con.setChecked(True)

        self.verticalLayout_3.addWidget(self.cross_np_con)

        self.cross_p_con = QCheckBox(self.groupBox_3)
        self.cross_p_con.setObjectName(u"cross_p_con")
        self.cross_p_con.setChecked(True)

        self.verticalLayout_3.addWidget(self.cross_p_con)

        self.verticalSpacer_3 = QSpacerItem(20, 166, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_3)

        self.export_1_con = QPushButton(self.groupBox_3)
        self.export_1_con.setObjectName(u"export_1_con")

        self.verticalLayout_3.addWidget(self.export_1_con)


        self.horizontalLayout_4.addWidget(self.groupBox_3)


        self.verticalLayout_5.addLayout(self.horizontalLayout_4)

        self.stackedWidget.addWidget(self.cowan)
        self.all_cowan = QWidget()
        self.all_cowan.setObjectName(u"all_cowan")
        self.verticalLayout_2 = QVBoxLayout(self.all_cowan)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.all_cowan_info_table = QTableWidget(self.all_cowan)
        if (self.all_cowan_info_table.columnCount() < 4):
            self.all_cowan_info_table.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.all_cowan_info_table.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.all_cowan_info_table.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.all_cowan_info_table.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.all_cowan_info_table.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        self.all_cowan_info_table.setObjectName(u"all_cowan_info_table")

        self.verticalLayout_2.addWidget(self.all_cowan_info_table)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.export_2 = QPushButton(self.all_cowan)
        self.export_2.setObjectName(u"export_2")

        self.horizontalLayout_3.addWidget(self.export_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.stackedWidget.addWidget(self.all_cowan)
        self.st_resolution = QWidget()
        self.st_resolution.setObjectName(u"st_resolution")
        self.verticalLayout_8 = QVBoxLayout(self.st_resolution)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_2 = QLabel(self.st_resolution)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_5.addWidget(self.label_2)

        self.choose_st = QComboBox(self.st_resolution)
        self.choose_st.setObjectName(u"choose_st")

        self.horizontalLayout_5.addWidget(self.choose_st)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_4)


        self.verticalLayout_8.addLayout(self.horizontalLayout_5)

        self.st_info = QLabel(self.st_resolution)
        self.st_info.setObjectName(u"st_info")

        self.verticalLayout_8.addWidget(self.st_info)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.groupBox_4 = QGroupBox(self.st_resolution)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.verticalLayout_6 = QVBoxLayout(self.groupBox_4)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.exp_data = QCheckBox(self.groupBox_4)
        self.exp_data.setObjectName(u"exp_data")
        self.exp_data.setChecked(True)

        self.verticalLayout_6.addWidget(self.exp_data)

        self.sim_data = QCheckBox(self.groupBox_4)
        self.sim_data.setObjectName(u"sim_data")
        self.sim_data.setChecked(True)

        self.verticalLayout_6.addWidget(self.sim_data)

        self.ion_abu = QCheckBox(self.groupBox_4)
        self.ion_abu.setObjectName(u"ion_abu")
        self.ion_abu.setChecked(True)

        self.verticalLayout_6.addWidget(self.ion_abu)

        self.verticalSpacer_4 = QSpacerItem(20, 227, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_4)

        self.export_3_overall = QPushButton(self.groupBox_4)
        self.export_3_overall.setObjectName(u"export_3_overall")

        self.verticalLayout_6.addWidget(self.export_3_overall)


        self.horizontalLayout_6.addWidget(self.groupBox_4)

        self.groupBox_5 = QGroupBox(self.st_resolution)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.verticalLayout_7 = QVBoxLayout(self.groupBox_5)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.ion_widen = QCheckBox(self.groupBox_5)
        self.ion_widen.setObjectName(u"ion_widen")
        self.ion_widen.setChecked(True)

        self.verticalLayout_7.addWidget(self.ion_widen)

        self.ion_widen_abu = QCheckBox(self.groupBox_5)
        self.ion_widen_abu.setObjectName(u"ion_widen_abu")
        self.ion_widen_abu.setChecked(True)

        self.verticalLayout_7.addWidget(self.ion_widen_abu)

        self.verticalSpacer_5 = QSpacerItem(20, 227, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_5)

        self.export_3_con = QPushButton(self.groupBox_5)
        self.export_3_con.setObjectName(u"export_3_con")

        self.verticalLayout_7.addWidget(self.export_3_con)


        self.horizontalLayout_6.addWidget(self.groupBox_5)


        self.verticalLayout_8.addLayout(self.horizontalLayout_6)

        self.stackedWidget.addWidget(self.st_resolution)
        self.all_st_resolution = QWidget()
        self.all_st_resolution.setObjectName(u"all_st_resolution")
        self.verticalLayout_9 = QVBoxLayout(self.all_st_resolution)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.st_info_table = QTableWidget(self.all_st_resolution)
        if (self.st_info_table.columnCount() < 4):
            self.st_info_table.setColumnCount(4)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.st_info_table.setHorizontalHeaderItem(0, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.st_info_table.setHorizontalHeaderItem(1, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.st_info_table.setHorizontalHeaderItem(2, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.st_info_table.setHorizontalHeaderItem(3, __qtablewidgetitem7)
        self.st_info_table.setObjectName(u"st_info_table")

        self.verticalLayout_9.addWidget(self.st_info_table)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_3)

        self.export_4 = QPushButton(self.all_st_resolution)
        self.export_4.setObjectName(u"export_4")

        self.horizontalLayout_7.addWidget(self.export_4)


        self.verticalLayout_9.addLayout(self.horizontalLayout_7)

        self.stackedWidget.addWidget(self.all_st_resolution)

        self.horizontalLayout.addWidget(self.stackedWidget)


        self.retranslateUi(DataShow)

        self.stackedWidget.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(DataShow)
    # setupUi

    def retranslateUi(self, DataShow):
        DataShow.setWindowTitle(QCoreApplication.translate("DataShow", u"Form", None))
        self.cowan_change.setText(QCoreApplication.translate("DataShow", u"\u5404\u4e2aCowan\u5bf9\u8c61", None))
        self.all_cowan_change.setText(QCoreApplication.translate("DataShow", u"\u6574\u4f53Cowan\u5bf9\u8c61", None))
        self.st_change.setText(QCoreApplication.translate("DataShow", u"\u65f6\u7a7a\u5206\u8fa8\u5bf9\u8c61", None))
        self.all_st_change.setText(QCoreApplication.translate("DataShow", u"\u6574\u4f53\u65f6\u7a7a\u5206\u8fa8\u5bf9\u8c61", None))
        self.label.setText(QCoreApplication.translate("DataShow", u"\u79bb\u5316\u5ea6\u9009\u62e9", None))
        self.ion_info.setText(QCoreApplication.translate("DataShow", u"\u534a\u9ad8\uff1a\u6e29\u5ea6\uff1a\u504f\u79fb\uff1a", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("DataShow", u"\u603b\u4f53\u5c55\u5bbd", None))
        self.init_res_overall.setText(QCoreApplication.translate("DataShow", u"\u539f\u59cb\u8ba1\u7b97\u7ed3\u679c", None))
        self.line_over_all.setText(QCoreApplication.translate("DataShow", u"\u8dc3\u8fc1\u7ebf", None))
        self.gauss_overall.setText(QCoreApplication.translate("DataShow", u"gauss", None))
        self.cross_np_overall.setText(QCoreApplication.translate("DataShow", u"cross_np", None))
        self.cross_p_overall.setText(QCoreApplication.translate("DataShow", u"cross_p", None))
        self.export_1_overall.setText(QCoreApplication.translate("DataShow", u"\u5bfc\u51fa\u6570\u636e", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("DataShow", u"\u6309\u7ec4\u6001\u5206\u7ec4", None))
        self.init_res_con.setText(QCoreApplication.translate("DataShow", u"\u539f\u59cb\u8ba1\u7b97\u7ed3\u679c", None))
        self.line_con.setText(QCoreApplication.translate("DataShow", u"\u8dc3\u8fc1\u7ebf", None))
        self.gauss_con.setText(QCoreApplication.translate("DataShow", u"gauss", None))
        self.cross_np_con.setText(QCoreApplication.translate("DataShow", u"cross_np", None))
        self.cross_p_con.setText(QCoreApplication.translate("DataShow", u"cross_p", None))
        self.export_1_con.setText(QCoreApplication.translate("DataShow", u"\u5bfc\u51fa\u6570\u636e", None))
        ___qtablewidgetitem = self.all_cowan_info_table.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("DataShow", u"\u79bb\u5316\u5ea6", None));
        ___qtablewidgetitem1 = self.all_cowan_info_table.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("DataShow", u"\u5c55\u5bbd\u6e29\u5ea6", None));
        ___qtablewidgetitem2 = self.all_cowan_info_table.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("DataShow", u"\u534a\u9ad8\u5168\u5bbd", None));
        ___qtablewidgetitem3 = self.all_cowan_info_table.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("DataShow", u"\u504f\u79fb", None));
        self.export_2.setText(QCoreApplication.translate("DataShow", u"\u5bfc\u51fa\u6570\u636e", None))
        self.label_2.setText(QCoreApplication.translate("DataShow", u"\u65f6\u7a7a\u5206\u8fa8\u9009\u62e9", None))
        self.st_info.setText(QCoreApplication.translate("DataShow", u"\u6e29\u5ea6\uff1a\u5bc6\u5ea6", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("DataShow", u"\u6574\u4f53", None))
        self.exp_data.setText(QCoreApplication.translate("DataShow", u"\u5b9e\u9a8c\u8c31\u7ebf", None))
        self.sim_data.setText(QCoreApplication.translate("DataShow", u"\u6a21\u62df\u8c31\u7ebf", None))
        self.ion_abu.setText(QCoreApplication.translate("DataShow", u"\u79bb\u5b50\u4e30\u5ea6", None))
        self.export_3_overall.setText(QCoreApplication.translate("DataShow", u"\u5bfc\u51fa\u6570\u636e", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("DataShow", u"\u6309\u7ec4\u6001", None))
        self.ion_widen.setText(QCoreApplication.translate("DataShow", u"\u5404\u79bb\u5b50\u5c55\u5bbd", None))
        self.ion_widen_abu.setText(QCoreApplication.translate("DataShow", u"\u5404\u79bb\u5b50\u5c55\u5bbd*\u79bb\u5b50\u4e30\u5ea6", None))
        self.export_3_con.setText(QCoreApplication.translate("DataShow", u"\u5bfc\u51fa\u6570\u636e", None))
        ___qtablewidgetitem4 = self.st_info_table.horizontalHeaderItem(0)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("DataShow", u"\u65f6\u95f4", None));
        ___qtablewidgetitem5 = self.st_info_table.horizontalHeaderItem(1)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("DataShow", u"\u4f4d\u7f6e", None));
        ___qtablewidgetitem6 = self.st_info_table.horizontalHeaderItem(2)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("DataShow", u"\u6e29\u5ea6", None));
        ___qtablewidgetitem7 = self.st_info_table.horizontalHeaderItem(3)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("DataShow", u"\u5bc6\u5ea6", None));
        self.export_4.setText(QCoreApplication.translate("DataShow", u"\u5bfc\u51fa\u6570\u636e ", None))
    # retranslateUi

