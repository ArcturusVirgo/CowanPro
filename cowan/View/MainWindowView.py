# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDoubleSpinBox,
    QFrame, QGridLayout, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QMainWindow, QMenu, QMenuBar,
    QPushButton, QRadioButton, QSizePolicy, QSpacerItem,
    QSpinBox, QStackedWidget, QStatusBar, QTabWidget,
    QTableWidget, QTableWidgetItem, QToolButton, QTreeWidget,
    QTreeWidgetItem, QVBoxLayout, QWidget)

class Ui_main_window(object):
    def setupUi(self, main_window):
        if not main_window.objectName():
            main_window.setObjectName(u"main_window")
        main_window.resize(1374, 883)
        main_window.setMinimumSize(QSize(0, 0))
        main_window.setMaximumSize(QSize(16777215, 16777215))
        main_window.setStyleSheet(u"")
        self.action = QAction(main_window)
        self.action.setObjectName(u"action")
        self.action.setPriority(QAction.NormalPriority)
        self.actionjiazai = QAction(main_window)
        self.actionjiazai.setObjectName(u"actionjiazai")
        self.action_2 = QAction(main_window)
        self.action_2.setObjectName(u"action_2")
        self.action_4 = QAction(main_window)
        self.action_4.setObjectName(u"action_4")
        self.choose_project_path = QAction(main_window)
        self.choose_project_path.setObjectName(u"choose_project_path")
        self.show_guides = QAction(main_window)
        self.show_guides.setObjectName(u"show_guides")
        self.action_3 = QAction(main_window)
        self.action_3.setObjectName(u"action_3")
        self.action_5 = QAction(main_window)
        self.action_5.setObjectName(u"action_5")
        self.save_project = QAction(main_window)
        self.save_project.setObjectName(u"save_project")
        self.exit_project = QAction(main_window)
        self.exit_project.setObjectName(u"exit_project")
        self.reset_cal = QAction(main_window)
        self.reset_cal.setObjectName(u"reset_cal")
        self.export_data = QAction(main_window)
        self.export_data.setObjectName(u"export_data")
        self.set_xrange = QAction(main_window)
        self.set_xrange.setObjectName(u"set_xrange")
        self.reset_xrange = QAction(main_window)
        self.reset_xrange.setObjectName(u"reset_xrange")
        self.export_configuration_average_wavelength = QAction(main_window)
        self.export_configuration_average_wavelength.setObjectName(u"export_configuration_average_wavelength")
        self.export_plot_data = QAction(main_window)
        self.export_plot_data.setObjectName(u"export_plot_data")
        self.centralwidget = QWidget(main_window)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setEnabled(True)
        self.centralwidget.setMinimumSize(QSize(0, 0))
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, -1, -1, -1)
        self.navigation = QListWidget(self.centralwidget)
        QListWidgetItem(self.navigation)
        QListWidgetItem(self.navigation)
        QListWidgetItem(self.navigation)
        QListWidgetItem(self.navigation)
        QListWidgetItem(self.navigation)
        self.navigation.setObjectName(u"navigation")
        self.navigation.setMinimumSize(QSize(50, 0))
        self.navigation.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout.addWidget(self.navigation)

        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.horizontalLayout_2 = QHBoxLayout(self.page)
        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(10, 10, 10, 10)
        self.tabWidget = QTabWidget(self.page)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setMinimumSize(QSize(210, 0))
        self.tabWidget.setMaximumSize(QSize(170, 16777215))
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_4 = QVBoxLayout(self.tab)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setHorizontalSpacing(10)
        self.gridLayout_2.setVerticalSpacing(5)
        self.in36_text_1 = QLabel(self.tab)
        self.in36_text_1.setObjectName(u"in36_text_1")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.in36_text_1.sizePolicy().hasHeightForWidth())
        self.in36_text_1.setSizePolicy(sizePolicy)
        self.in36_text_1.setMinimumSize(QSize(80, 0))
        self.in36_text_1.setMaximumSize(QSize(60, 16777215))
        self.in36_text_1.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.in36_text_1, 0, 0, 1, 1)

        self.in36_1 = QLineEdit(self.tab)
        self.in36_1.setObjectName(u"in36_1")
        self.in36_1.setMinimumSize(QSize(80, 0))
        self.in36_1.setMaximumSize(QSize(80, 16777215))
        self.in36_1.setSizeIncrement(QSize(0, 0))
        self.in36_1.setBaseSize(QSize(0, 0))
        self.in36_1.setCursorPosition(1)
        self.in36_1.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.in36_1.setClearButtonEnabled(False)

        self.gridLayout_2.addWidget(self.in36_1, 0, 1, 1, 1)

        self.in36_text_2 = QLabel(self.tab)
        self.in36_text_2.setObjectName(u"in36_text_2")
        sizePolicy.setHeightForWidth(self.in36_text_2.sizePolicy().hasHeightForWidth())
        self.in36_text_2.setSizePolicy(sizePolicy)
        self.in36_text_2.setMinimumSize(QSize(80, 0))
        self.in36_text_2.setMaximumSize(QSize(60, 16777215))
        self.in36_text_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.in36_text_2, 1, 0, 1, 1)

        self.in36_2 = QLineEdit(self.tab)
        self.in36_2.setObjectName(u"in36_2")
        self.in36_2.setMinimumSize(QSize(80, 0))
        self.in36_2.setMaximumSize(QSize(80, 16777215))
        self.in36_2.setSizeIncrement(QSize(0, 0))
        self.in36_2.setBaseSize(QSize(0, 0))
        self.in36_2.setCursorPosition(0)
        self.in36_2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.in36_2.setClearButtonEnabled(False)

        self.gridLayout_2.addWidget(self.in36_2, 1, 1, 1, 1)

        self.in36_text_3 = QLabel(self.tab)
        self.in36_text_3.setObjectName(u"in36_text_3")
        sizePolicy.setHeightForWidth(self.in36_text_3.sizePolicy().hasHeightForWidth())
        self.in36_text_3.setSizePolicy(sizePolicy)
        self.in36_text_3.setMinimumSize(QSize(80, 0))
        self.in36_text_3.setMaximumSize(QSize(60, 16777215))
        self.in36_text_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.in36_text_3, 2, 0, 1, 1)

        self.in36_3 = QLineEdit(self.tab)
        self.in36_3.setObjectName(u"in36_3")
        self.in36_3.setMinimumSize(QSize(80, 0))
        self.in36_3.setMaximumSize(QSize(80, 16777215))
        self.in36_3.setSizeIncrement(QSize(0, 0))
        self.in36_3.setBaseSize(QSize(0, 0))
        self.in36_3.setCursorPosition(0)
        self.in36_3.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.in36_3.setClearButtonEnabled(False)

        self.gridLayout_2.addWidget(self.in36_3, 2, 1, 1, 1)

        self.in36_text_4 = QLabel(self.tab)
        self.in36_text_4.setObjectName(u"in36_text_4")
        sizePolicy.setHeightForWidth(self.in36_text_4.sizePolicy().hasHeightForWidth())
        self.in36_text_4.setSizePolicy(sizePolicy)
        self.in36_text_4.setMinimumSize(QSize(80, 0))
        self.in36_text_4.setMaximumSize(QSize(60, 16777215))
        self.in36_text_4.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.in36_text_4, 3, 0, 1, 1)

        self.in36_4 = QLineEdit(self.tab)
        self.in36_4.setObjectName(u"in36_4")
        self.in36_4.setMinimumSize(QSize(80, 0))
        self.in36_4.setMaximumSize(QSize(80, 16777215))
        self.in36_4.setSizeIncrement(QSize(0, 0))
        self.in36_4.setBaseSize(QSize(0, 0))
        self.in36_4.setCursorPosition(0)
        self.in36_4.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.in36_4.setClearButtonEnabled(False)

        self.gridLayout_2.addWidget(self.in36_4, 3, 1, 1, 1)

        self.in36_text_5 = QLabel(self.tab)
        self.in36_text_5.setObjectName(u"in36_text_5")
        sizePolicy.setHeightForWidth(self.in36_text_5.sizePolicy().hasHeightForWidth())
        self.in36_text_5.setSizePolicy(sizePolicy)
        self.in36_text_5.setMinimumSize(QSize(80, 0))
        self.in36_text_5.setMaximumSize(QSize(60, 16777215))
        self.in36_text_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.in36_text_5, 4, 0, 1, 1)

        self.in36_5 = QLineEdit(self.tab)
        self.in36_5.setObjectName(u"in36_5")
        self.in36_5.setMinimumSize(QSize(80, 0))
        self.in36_5.setMaximumSize(QSize(80, 16777215))
        self.in36_5.setSizeIncrement(QSize(0, 0))
        self.in36_5.setBaseSize(QSize(0, 0))
        self.in36_5.setCursorPosition(0)
        self.in36_5.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.in36_5.setClearButtonEnabled(False)

        self.gridLayout_2.addWidget(self.in36_5, 4, 1, 1, 1)

        self.in36_text_6 = QLabel(self.tab)
        self.in36_text_6.setObjectName(u"in36_text_6")
        sizePolicy.setHeightForWidth(self.in36_text_6.sizePolicy().hasHeightForWidth())
        self.in36_text_6.setSizePolicy(sizePolicy)
        self.in36_text_6.setMinimumSize(QSize(80, 0))
        self.in36_text_6.setMaximumSize(QSize(60, 16777215))
        self.in36_text_6.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.in36_text_6, 5, 0, 1, 1)

        self.in36_6 = QLineEdit(self.tab)
        self.in36_6.setObjectName(u"in36_6")
        self.in36_6.setMinimumSize(QSize(80, 0))
        self.in36_6.setMaximumSize(QSize(80, 16777215))
        self.in36_6.setSizeIncrement(QSize(0, 0))
        self.in36_6.setBaseSize(QSize(0, 0))
        self.in36_6.setCursorPosition(0)
        self.in36_6.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.in36_6.setClearButtonEnabled(False)

        self.gridLayout_2.addWidget(self.in36_6, 5, 1, 1, 1)

        self.in36_text_7 = QLabel(self.tab)
        self.in36_text_7.setObjectName(u"in36_text_7")
        sizePolicy.setHeightForWidth(self.in36_text_7.sizePolicy().hasHeightForWidth())
        self.in36_text_7.setSizePolicy(sizePolicy)
        self.in36_text_7.setMinimumSize(QSize(80, 0))
        self.in36_text_7.setMaximumSize(QSize(60, 16777215))
        self.in36_text_7.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.in36_text_7, 6, 0, 1, 1)

        self.in36_7 = QLineEdit(self.tab)
        self.in36_7.setObjectName(u"in36_7")
        self.in36_7.setMinimumSize(QSize(80, 0))
        self.in36_7.setMaximumSize(QSize(80, 16777215))
        self.in36_7.setSizeIncrement(QSize(0, 0))
        self.in36_7.setBaseSize(QSize(0, 0))
        self.in36_7.setCursorPosition(0)
        self.in36_7.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.in36_7.setClearButtonEnabled(False)

        self.gridLayout_2.addWidget(self.in36_7, 6, 1, 1, 1)

        self.in36_text_8 = QLabel(self.tab)
        self.in36_text_8.setObjectName(u"in36_text_8")
        sizePolicy.setHeightForWidth(self.in36_text_8.sizePolicy().hasHeightForWidth())
        self.in36_text_8.setSizePolicy(sizePolicy)
        self.in36_text_8.setMinimumSize(QSize(80, 0))
        self.in36_text_8.setMaximumSize(QSize(60, 16777215))
        self.in36_text_8.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.in36_text_8, 7, 0, 1, 1)

        self.in36_8 = QLineEdit(self.tab)
        self.in36_8.setObjectName(u"in36_8")
        self.in36_8.setMinimumSize(QSize(80, 0))
        self.in36_8.setMaximumSize(QSize(80, 16777215))
        self.in36_8.setSizeIncrement(QSize(0, 0))
        self.in36_8.setBaseSize(QSize(0, 0))
        self.in36_8.setCursorPosition(0)
        self.in36_8.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.in36_8.setClearButtonEnabled(False)

        self.gridLayout_2.addWidget(self.in36_8, 7, 1, 1, 1)

        self.in36_text_9 = QLabel(self.tab)
        self.in36_text_9.setObjectName(u"in36_text_9")
        sizePolicy.setHeightForWidth(self.in36_text_9.sizePolicy().hasHeightForWidth())
        self.in36_text_9.setSizePolicy(sizePolicy)
        self.in36_text_9.setMinimumSize(QSize(80, 0))
        self.in36_text_9.setMaximumSize(QSize(60, 16777215))
        self.in36_text_9.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.in36_text_9, 8, 0, 1, 1)

        self.in36_9 = QLineEdit(self.tab)
        self.in36_9.setObjectName(u"in36_9")
        self.in36_9.setMinimumSize(QSize(80, 0))
        self.in36_9.setMaximumSize(QSize(80, 16777215))
        self.in36_9.setSizeIncrement(QSize(0, 0))
        self.in36_9.setBaseSize(QSize(0, 0))
        self.in36_9.setCursorPosition(0)
        self.in36_9.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.in36_9.setClearButtonEnabled(False)

        self.gridLayout_2.addWidget(self.in36_9, 8, 1, 1, 1)

        self.in36_text_10 = QLabel(self.tab)
        self.in36_text_10.setObjectName(u"in36_text_10")
        sizePolicy.setHeightForWidth(self.in36_text_10.sizePolicy().hasHeightForWidth())
        self.in36_text_10.setSizePolicy(sizePolicy)
        self.in36_text_10.setMinimumSize(QSize(80, 0))
        self.in36_text_10.setMaximumSize(QSize(60, 16777215))
        self.in36_text_10.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.in36_text_10, 9, 0, 1, 1)

        self.in36_10 = QLineEdit(self.tab)
        self.in36_10.setObjectName(u"in36_10")
        self.in36_10.setMinimumSize(QSize(80, 0))
        self.in36_10.setMaximumSize(QSize(80, 16777215))
        self.in36_10.setSizeIncrement(QSize(0, 0))
        self.in36_10.setBaseSize(QSize(0, 0))
        self.in36_10.setCursorPosition(0)
        self.in36_10.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.in36_10.setClearButtonEnabled(False)

        self.gridLayout_2.addWidget(self.in36_10, 9, 1, 1, 1)

        self.in36_text_11 = QLabel(self.tab)
        self.in36_text_11.setObjectName(u"in36_text_11")
        sizePolicy.setHeightForWidth(self.in36_text_11.sizePolicy().hasHeightForWidth())
        self.in36_text_11.setSizePolicy(sizePolicy)
        self.in36_text_11.setMinimumSize(QSize(80, 0))
        self.in36_text_11.setMaximumSize(QSize(60, 16777215))
        self.in36_text_11.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.in36_text_11, 10, 0, 1, 1)

        self.in36_11 = QLineEdit(self.tab)
        self.in36_11.setObjectName(u"in36_11")
        self.in36_11.setMinimumSize(QSize(80, 0))
        self.in36_11.setMaximumSize(QSize(80, 16777215))
        self.in36_11.setSizeIncrement(QSize(0, 0))
        self.in36_11.setBaseSize(QSize(0, 0))
        self.in36_11.setCursorPosition(0)
        self.in36_11.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.in36_11.setClearButtonEnabled(False)

        self.gridLayout_2.addWidget(self.in36_11, 10, 1, 1, 1)

        self.in36_text_12 = QLabel(self.tab)
        self.in36_text_12.setObjectName(u"in36_text_12")
        sizePolicy.setHeightForWidth(self.in36_text_12.sizePolicy().hasHeightForWidth())
        self.in36_text_12.setSizePolicy(sizePolicy)
        self.in36_text_12.setMinimumSize(QSize(80, 0))
        self.in36_text_12.setMaximumSize(QSize(60, 16777215))
        self.in36_text_12.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.in36_text_12, 11, 0, 1, 1)

        self.in36_12 = QLineEdit(self.tab)
        self.in36_12.setObjectName(u"in36_12")
        self.in36_12.setMinimumSize(QSize(80, 0))
        self.in36_12.setMaximumSize(QSize(80, 16777215))
        self.in36_12.setSizeIncrement(QSize(0, 0))
        self.in36_12.setBaseSize(QSize(0, 0))
        self.in36_12.setCursorPosition(0)
        self.in36_12.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.in36_12.setClearButtonEnabled(False)

        self.gridLayout_2.addWidget(self.in36_12, 11, 1, 1, 1)

        self.in36_text_13 = QLabel(self.tab)
        self.in36_text_13.setObjectName(u"in36_text_13")
        sizePolicy.setHeightForWidth(self.in36_text_13.sizePolicy().hasHeightForWidth())
        self.in36_text_13.setSizePolicy(sizePolicy)
        self.in36_text_13.setMinimumSize(QSize(80, 0))
        self.in36_text_13.setMaximumSize(QSize(60, 16777215))
        self.in36_text_13.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.in36_text_13, 12, 0, 1, 1)

        self.in36_13 = QLineEdit(self.tab)
        self.in36_13.setObjectName(u"in36_13")
        self.in36_13.setMinimumSize(QSize(80, 0))
        self.in36_13.setMaximumSize(QSize(80, 16777215))
        self.in36_13.setSizeIncrement(QSize(0, 0))
        self.in36_13.setBaseSize(QSize(0, 0))
        self.in36_13.setCursorPosition(0)
        self.in36_13.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.in36_13.setClearButtonEnabled(False)

        self.gridLayout_2.addWidget(self.in36_13, 12, 1, 1, 1)

        self.in36_text_14 = QLabel(self.tab)
        self.in36_text_14.setObjectName(u"in36_text_14")
        sizePolicy.setHeightForWidth(self.in36_text_14.sizePolicy().hasHeightForWidth())
        self.in36_text_14.setSizePolicy(sizePolicy)
        self.in36_text_14.setMinimumSize(QSize(80, 0))
        self.in36_text_14.setMaximumSize(QSize(60, 16777215))
        self.in36_text_14.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.in36_text_14, 13, 0, 1, 1)

        self.in36_14 = QLineEdit(self.tab)
        self.in36_14.setObjectName(u"in36_14")
        self.in36_14.setMinimumSize(QSize(80, 0))
        self.in36_14.setMaximumSize(QSize(80, 16777215))
        self.in36_14.setSizeIncrement(QSize(0, 0))
        self.in36_14.setBaseSize(QSize(0, 0))
        self.in36_14.setCursorPosition(0)
        self.in36_14.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.in36_14.setClearButtonEnabled(False)

        self.gridLayout_2.addWidget(self.in36_14, 13, 1, 1, 1)

        self.in36_text_15 = QLabel(self.tab)
        self.in36_text_15.setObjectName(u"in36_text_15")
        sizePolicy.setHeightForWidth(self.in36_text_15.sizePolicy().hasHeightForWidth())
        self.in36_text_15.setSizePolicy(sizePolicy)
        self.in36_text_15.setMinimumSize(QSize(80, 0))
        self.in36_text_15.setMaximumSize(QSize(60, 16777215))
        self.in36_text_15.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.in36_text_15, 14, 0, 1, 1)

        self.in36_15 = QLineEdit(self.tab)
        self.in36_15.setObjectName(u"in36_15")
        self.in36_15.setMinimumSize(QSize(80, 0))
        self.in36_15.setMaximumSize(QSize(80, 16777215))
        self.in36_15.setSizeIncrement(QSize(0, 0))
        self.in36_15.setBaseSize(QSize(0, 0))
        self.in36_15.setCursorPosition(0)
        self.in36_15.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.in36_15.setClearButtonEnabled(False)

        self.gridLayout_2.addWidget(self.in36_15, 14, 1, 1, 1)

        self.in36_text_16 = QLabel(self.tab)
        self.in36_text_16.setObjectName(u"in36_text_16")
        sizePolicy.setHeightForWidth(self.in36_text_16.sizePolicy().hasHeightForWidth())
        self.in36_text_16.setSizePolicy(sizePolicy)
        self.in36_text_16.setMinimumSize(QSize(80, 0))
        self.in36_text_16.setMaximumSize(QSize(60, 16777215))
        self.in36_text_16.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.in36_text_16, 15, 0, 1, 1)

        self.in36_16 = QLineEdit(self.tab)
        self.in36_16.setObjectName(u"in36_16")
        self.in36_16.setMinimumSize(QSize(80, 0))
        self.in36_16.setMaximumSize(QSize(80, 16777215))
        self.in36_16.setSizeIncrement(QSize(0, 0))
        self.in36_16.setBaseSize(QSize(0, 0))
        self.in36_16.setCursorPosition(0)
        self.in36_16.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.in36_16.setClearButtonEnabled(False)

        self.gridLayout_2.addWidget(self.in36_16, 15, 1, 1, 1)

        self.in36_text_17 = QLabel(self.tab)
        self.in36_text_17.setObjectName(u"in36_text_17")
        sizePolicy.setHeightForWidth(self.in36_text_17.sizePolicy().hasHeightForWidth())
        self.in36_text_17.setSizePolicy(sizePolicy)
        self.in36_text_17.setMinimumSize(QSize(80, 0))
        self.in36_text_17.setMaximumSize(QSize(60, 16777215))
        self.in36_text_17.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.in36_text_17, 16, 0, 1, 1)

        self.in36_17 = QLineEdit(self.tab)
        self.in36_17.setObjectName(u"in36_17")
        self.in36_17.setMinimumSize(QSize(80, 0))
        self.in36_17.setMaximumSize(QSize(80, 16777215))
        self.in36_17.setSizeIncrement(QSize(0, 0))
        self.in36_17.setBaseSize(QSize(0, 0))
        self.in36_17.setCursorPosition(0)
        self.in36_17.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.in36_17.setClearButtonEnabled(False)

        self.gridLayout_2.addWidget(self.in36_17, 16, 1, 1, 1)

        self.in36_text_18 = QLabel(self.tab)
        self.in36_text_18.setObjectName(u"in36_text_18")
        sizePolicy.setHeightForWidth(self.in36_text_18.sizePolicy().hasHeightForWidth())
        self.in36_text_18.setSizePolicy(sizePolicy)
        self.in36_text_18.setMinimumSize(QSize(80, 0))
        self.in36_text_18.setMaximumSize(QSize(60, 16777215))
        self.in36_text_18.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.in36_text_18, 17, 0, 1, 1)

        self.in36_18 = QLineEdit(self.tab)
        self.in36_18.setObjectName(u"in36_18")
        self.in36_18.setMinimumSize(QSize(80, 0))
        self.in36_18.setMaximumSize(QSize(80, 16777215))
        self.in36_18.setSizeIncrement(QSize(0, 0))
        self.in36_18.setBaseSize(QSize(0, 0))
        self.in36_18.setCursorPosition(0)
        self.in36_18.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.in36_18.setClearButtonEnabled(False)

        self.gridLayout_2.addWidget(self.in36_18, 17, 1, 1, 1)

        self.in36_text_19 = QLabel(self.tab)
        self.in36_text_19.setObjectName(u"in36_text_19")
        sizePolicy.setHeightForWidth(self.in36_text_19.sizePolicy().hasHeightForWidth())
        self.in36_text_19.setSizePolicy(sizePolicy)
        self.in36_text_19.setMinimumSize(QSize(80, 0))
        self.in36_text_19.setMaximumSize(QSize(60, 16777215))
        self.in36_text_19.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.in36_text_19, 18, 0, 1, 1)

        self.in36_19 = QLineEdit(self.tab)
        self.in36_19.setObjectName(u"in36_19")
        self.in36_19.setMinimumSize(QSize(80, 0))
        self.in36_19.setMaximumSize(QSize(80, 16777215))
        self.in36_19.setSizeIncrement(QSize(0, 0))
        self.in36_19.setBaseSize(QSize(0, 0))
        self.in36_19.setCursorPosition(0)
        self.in36_19.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.in36_19.setClearButtonEnabled(False)

        self.gridLayout_2.addWidget(self.in36_19, 18, 1, 1, 1)

        self.in36_text_20 = QLabel(self.tab)
        self.in36_text_20.setObjectName(u"in36_text_20")
        sizePolicy.setHeightForWidth(self.in36_text_20.sizePolicy().hasHeightForWidth())
        self.in36_text_20.setSizePolicy(sizePolicy)
        self.in36_text_20.setMinimumSize(QSize(80, 0))
        self.in36_text_20.setMaximumSize(QSize(60, 16777215))
        self.in36_text_20.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.in36_text_20, 19, 0, 1, 1)

        self.in36_20 = QLineEdit(self.tab)
        self.in36_20.setObjectName(u"in36_20")
        self.in36_20.setMinimumSize(QSize(80, 0))
        self.in36_20.setMaximumSize(QSize(80, 16777215))
        self.in36_20.setSizeIncrement(QSize(0, 0))
        self.in36_20.setBaseSize(QSize(0, 0))
        self.in36_20.setCursorPosition(0)
        self.in36_20.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.in36_20.setClearButtonEnabled(False)

        self.gridLayout_2.addWidget(self.in36_20, 19, 1, 1, 1)

        self.in36_text_21 = QLabel(self.tab)
        self.in36_text_21.setObjectName(u"in36_text_21")
        sizePolicy.setHeightForWidth(self.in36_text_21.sizePolicy().hasHeightForWidth())
        self.in36_text_21.setSizePolicy(sizePolicy)
        self.in36_text_21.setMinimumSize(QSize(80, 0))
        self.in36_text_21.setMaximumSize(QSize(60, 16777215))
        self.in36_text_21.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.in36_text_21, 20, 0, 1, 1)

        self.in36_21 = QLineEdit(self.tab)
        self.in36_21.setObjectName(u"in36_21")
        self.in36_21.setMinimumSize(QSize(80, 0))
        self.in36_21.setMaximumSize(QSize(80, 16777215))
        self.in36_21.setSizeIncrement(QSize(0, 0))
        self.in36_21.setBaseSize(QSize(0, 0))
        self.in36_21.setCursorPosition(0)
        self.in36_21.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.in36_21.setClearButtonEnabled(False)

        self.gridLayout_2.addWidget(self.in36_21, 20, 1, 1, 1)

        self.in36_text_22 = QLabel(self.tab)
        self.in36_text_22.setObjectName(u"in36_text_22")
        sizePolicy.setHeightForWidth(self.in36_text_22.sizePolicy().hasHeightForWidth())
        self.in36_text_22.setSizePolicy(sizePolicy)
        self.in36_text_22.setMinimumSize(QSize(80, 0))
        self.in36_text_22.setMaximumSize(QSize(60, 16777215))
        self.in36_text_22.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.in36_text_22.setWordWrap(False)
        self.in36_text_22.setTextInteractionFlags(Qt.LinksAccessibleByMouse)

        self.gridLayout_2.addWidget(self.in36_text_22, 21, 0, 1, 1, Qt.AlignRight)

        self.in36_22 = QLineEdit(self.tab)
        self.in36_22.setObjectName(u"in36_22")
        self.in36_22.setMinimumSize(QSize(80, 0))
        self.in36_22.setMaximumSize(QSize(80, 16777215))
        self.in36_22.setSizeIncrement(QSize(0, 0))
        self.in36_22.setBaseSize(QSize(0, 0))
        self.in36_22.setCursorPosition(0)
        self.in36_22.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.in36_22.setClearButtonEnabled(False)

        self.gridLayout_2.addWidget(self.in36_22, 21, 1, 1, 1)

        self.in36_text_23 = QLabel(self.tab)
        self.in36_text_23.setObjectName(u"in36_text_23")
        sizePolicy.setHeightForWidth(self.in36_text_23.sizePolicy().hasHeightForWidth())
        self.in36_text_23.setSizePolicy(sizePolicy)
        self.in36_text_23.setMinimumSize(QSize(80, 0))
        self.in36_text_23.setMaximumSize(QSize(60, 16777215))
        self.in36_text_23.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_2.addWidget(self.in36_text_23, 22, 0, 1, 1)

        self.in36_23 = QLineEdit(self.tab)
        self.in36_23.setObjectName(u"in36_23")
        self.in36_23.setMinimumSize(QSize(80, 0))
        self.in36_23.setMaximumSize(QSize(80, 16777215))
        self.in36_23.setSizeIncrement(QSize(0, 0))
        self.in36_23.setBaseSize(QSize(0, 0))
        self.in36_23.setCursorPosition(0)
        self.in36_23.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.in36_23.setClearButtonEnabled(False)

        self.gridLayout_2.addWidget(self.in36_23, 22, 1, 1, 1)


        self.verticalLayout_4.addLayout(self.gridLayout_2)

        self.line_7 = QFrame(self.tab)
        self.line_7.setObjectName(u"line_7")
        self.line_7.setFrameShape(QFrame.HLine)
        self.line_7.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_4.addWidget(self.line_7)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.load_in36 = QPushButton(self.tab)
        self.load_in36.setObjectName(u"load_in36")

        self.horizontalLayout_11.addWidget(self.load_in36)

        self.preview_in36 = QPushButton(self.tab)
        self.preview_in36.setObjectName(u"preview_in36")

        self.horizontalLayout_11.addWidget(self.preview_in36)


        self.verticalLayout_4.addLayout(self.horizontalLayout_11)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_2)

        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.verticalLayout_7 = QVBoxLayout(self.tab_2)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setHorizontalSpacing(10)
        self.gridLayout_3.setVerticalSpacing(5)
        self.in2_text_1 = QLabel(self.tab_2)
        self.in2_text_1.setObjectName(u"in2_text_1")
        self.in2_text_1.setMinimumSize(QSize(80, 0))
        self.in2_text_1.setMaximumSize(QSize(80, 16777215))
        self.in2_text_1.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.in2_text_1, 0, 0, 1, 1)

        self.in2_1 = QLineEdit(self.tab_2)
        self.in2_1.setObjectName(u"in2_1")
        self.in2_1.setMinimumSize(QSize(80, 0))
        self.in2_1.setMaximumSize(QSize(80, 30))
        self.in2_1.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.in2_1, 0, 1, 1, 1)

        self.in2_text_2 = QLabel(self.tab_2)
        self.in2_text_2.setObjectName(u"in2_text_2")
        self.in2_text_2.setMinimumSize(QSize(80, 0))
        self.in2_text_2.setMaximumSize(QSize(80, 16777215))
        self.in2_text_2.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.in2_text_2, 1, 0, 1, 1)

        self.in2_2 = QLineEdit(self.tab_2)
        self.in2_2.setObjectName(u"in2_2")
        self.in2_2.setMinimumSize(QSize(80, 0))
        self.in2_2.setMaximumSize(QSize(80, 30))
        self.in2_2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.in2_2, 1, 1, 1, 1)

        self.in2_text_3 = QLabel(self.tab_2)
        self.in2_text_3.setObjectName(u"in2_text_3")
        self.in2_text_3.setMinimumSize(QSize(80, 0))
        self.in2_text_3.setMaximumSize(QSize(80, 16777215))
        self.in2_text_3.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.in2_text_3, 2, 0, 1, 1)

        self.in2_3 = QLineEdit(self.tab_2)
        self.in2_3.setObjectName(u"in2_3")
        self.in2_3.setMinimumSize(QSize(80, 0))
        self.in2_3.setMaximumSize(QSize(80, 30))
        self.in2_3.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.in2_3, 2, 1, 1, 1)

        self.in2_text_4 = QLabel(self.tab_2)
        self.in2_text_4.setObjectName(u"in2_text_4")
        self.in2_text_4.setMinimumSize(QSize(80, 0))
        self.in2_text_4.setMaximumSize(QSize(80, 16777215))
        self.in2_text_4.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.in2_text_4, 3, 0, 1, 1)

        self.in2_4 = QLineEdit(self.tab_2)
        self.in2_4.setObjectName(u"in2_4")
        self.in2_4.setMinimumSize(QSize(80, 0))
        self.in2_4.setMaximumSize(QSize(80, 30))
        self.in2_4.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.in2_4, 3, 1, 1, 1)

        self.in2_text_5 = QLabel(self.tab_2)
        self.in2_text_5.setObjectName(u"in2_text_5")
        self.in2_text_5.setMinimumSize(QSize(80, 0))
        self.in2_text_5.setMaximumSize(QSize(80, 16777215))
        self.in2_text_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.in2_text_5, 4, 0, 1, 1)

        self.in2_5 = QLineEdit(self.tab_2)
        self.in2_5.setObjectName(u"in2_5")
        self.in2_5.setMinimumSize(QSize(80, 0))
        self.in2_5.setMaximumSize(QSize(80, 30))
        self.in2_5.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.in2_5, 4, 1, 1, 1)

        self.in2_text_6 = QLabel(self.tab_2)
        self.in2_text_6.setObjectName(u"in2_text_6")
        self.in2_text_6.setMinimumSize(QSize(80, 0))
        self.in2_text_6.setMaximumSize(QSize(80, 16777215))
        self.in2_text_6.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.in2_text_6, 5, 0, 1, 1)

        self.in2_6 = QLineEdit(self.tab_2)
        self.in2_6.setObjectName(u"in2_6")
        self.in2_6.setMinimumSize(QSize(80, 0))
        self.in2_6.setMaximumSize(QSize(80, 30))
        self.in2_6.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.in2_6, 5, 1, 1, 1)

        self.in2_text_7 = QLabel(self.tab_2)
        self.in2_text_7.setObjectName(u"in2_text_7")
        self.in2_text_7.setMinimumSize(QSize(80, 0))
        self.in2_text_7.setMaximumSize(QSize(80, 16777215))
        self.in2_text_7.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.in2_text_7, 6, 0, 1, 1)

        self.in2_7 = QLineEdit(self.tab_2)
        self.in2_7.setObjectName(u"in2_7")
        self.in2_7.setMinimumSize(QSize(80, 0))
        self.in2_7.setMaximumSize(QSize(80, 30))
        self.in2_7.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.in2_7, 6, 1, 1, 1)

        self.in2_text_8 = QLabel(self.tab_2)
        self.in2_text_8.setObjectName(u"in2_text_8")
        self.in2_text_8.setMinimumSize(QSize(80, 0))
        self.in2_text_8.setMaximumSize(QSize(80, 16777215))
        self.in2_text_8.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.in2_text_8, 7, 0, 1, 1)

        self.in2_8 = QLineEdit(self.tab_2)
        self.in2_8.setObjectName(u"in2_8")
        self.in2_8.setMinimumSize(QSize(80, 0))
        self.in2_8.setMaximumSize(QSize(80, 30))
        self.in2_8.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.in2_8, 7, 1, 1, 1)

        self.in2_text_9 = QLabel(self.tab_2)
        self.in2_text_9.setObjectName(u"in2_text_9")
        self.in2_text_9.setMinimumSize(QSize(80, 0))
        self.in2_text_9.setMaximumSize(QSize(80, 16777215))
        self.in2_text_9.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.in2_text_9, 8, 0, 1, 1)

        self.in2_9_a = QLineEdit(self.tab_2)
        self.in2_9_a.setObjectName(u"in2_9_a")
        self.in2_9_a.setMinimumSize(QSize(80, 0))
        self.in2_9_a.setMaximumSize(QSize(80, 30))
        self.in2_9_a.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.in2_9_a, 8, 1, 1, 1)

        self.in2_9_b = QLineEdit(self.tab_2)
        self.in2_9_b.setObjectName(u"in2_9_b")
        self.in2_9_b.setMinimumSize(QSize(80, 0))
        self.in2_9_b.setMaximumSize(QSize(80, 30))
        self.in2_9_b.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.in2_9_b, 9, 1, 1, 1)

        self.in2_9_c = QLineEdit(self.tab_2)
        self.in2_9_c.setObjectName(u"in2_9_c")
        self.in2_9_c.setMinimumSize(QSize(80, 0))
        self.in2_9_c.setMaximumSize(QSize(80, 30))
        self.in2_9_c.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.in2_9_c, 10, 1, 1, 1)

        self.in2_9_d = QLineEdit(self.tab_2)
        self.in2_9_d.setObjectName(u"in2_9_d")
        self.in2_9_d.setMinimumSize(QSize(80, 0))
        self.in2_9_d.setMaximumSize(QSize(80, 30))
        self.in2_9_d.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.in2_9_d, 11, 1, 1, 1)

        self.in2_text_10 = QLabel(self.tab_2)
        self.in2_text_10.setObjectName(u"in2_text_10")
        self.in2_text_10.setMinimumSize(QSize(80, 0))
        self.in2_text_10.setMaximumSize(QSize(80, 16777215))
        self.in2_text_10.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.in2_text_10, 12, 0, 1, 1)

        self.in2_10 = QLineEdit(self.tab_2)
        self.in2_10.setObjectName(u"in2_10")
        self.in2_10.setMinimumSize(QSize(80, 0))
        self.in2_10.setMaximumSize(QSize(80, 30))
        self.in2_10.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.in2_10, 12, 1, 1, 1)

        self.in2_text_12 = QLabel(self.tab_2)
        self.in2_text_12.setObjectName(u"in2_text_12")
        self.in2_text_12.setMinimumSize(QSize(80, 0))
        self.in2_text_12.setMaximumSize(QSize(80, 16777215))
        self.in2_text_12.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.in2_text_12, 13, 0, 1, 1)

        self.in2_12 = QLineEdit(self.tab_2)
        self.in2_12.setObjectName(u"in2_12")
        self.in2_12.setMinimumSize(QSize(80, 0))
        self.in2_12.setMaximumSize(QSize(80, 30))
        self.in2_12.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.in2_12, 13, 1, 1, 1)

        self.in2_text_13 = QLabel(self.tab_2)
        self.in2_text_13.setObjectName(u"in2_text_13")
        self.in2_text_13.setMinimumSize(QSize(80, 0))
        self.in2_text_13.setMaximumSize(QSize(80, 16777215))
        self.in2_text_13.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.in2_text_13, 14, 0, 1, 1)

        self.in2_13 = QLineEdit(self.tab_2)
        self.in2_13.setObjectName(u"in2_13")
        self.in2_13.setMinimumSize(QSize(80, 0))
        self.in2_13.setMaximumSize(QSize(80, 30))
        self.in2_13.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.in2_13, 14, 1, 1, 1)

        self.in2_text_14 = QLabel(self.tab_2)
        self.in2_text_14.setObjectName(u"in2_text_14")
        self.in2_text_14.setMinimumSize(QSize(80, 0))
        self.in2_text_14.setMaximumSize(QSize(80, 16777215))
        self.in2_text_14.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.in2_text_14, 15, 0, 1, 1)

        self.in2_14 = QLineEdit(self.tab_2)
        self.in2_14.setObjectName(u"in2_14")
        self.in2_14.setMinimumSize(QSize(80, 0))
        self.in2_14.setMaximumSize(QSize(80, 30))
        self.in2_14.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.in2_14, 15, 1, 1, 1)

        self.in2_text_15 = QLabel(self.tab_2)
        self.in2_text_15.setObjectName(u"in2_text_15")
        self.in2_text_15.setMinimumSize(QSize(80, 0))
        self.in2_text_15.setMaximumSize(QSize(80, 16777215))
        self.in2_text_15.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.in2_text_15, 16, 0, 1, 1)

        self.in2_15 = QLineEdit(self.tab_2)
        self.in2_15.setObjectName(u"in2_15")
        self.in2_15.setMinimumSize(QSize(80, 0))
        self.in2_15.setMaximumSize(QSize(80, 30))
        self.in2_15.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.in2_15, 16, 1, 1, 1)

        self.in2_text_16 = QLabel(self.tab_2)
        self.in2_text_16.setObjectName(u"in2_text_16")
        self.in2_text_16.setMinimumSize(QSize(80, 0))
        self.in2_text_16.setMaximumSize(QSize(80, 16777215))
        self.in2_text_16.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.in2_text_16, 17, 0, 1, 1)

        self.in2_16 = QLineEdit(self.tab_2)
        self.in2_16.setObjectName(u"in2_16")
        self.in2_16.setMinimumSize(QSize(80, 0))
        self.in2_16.setMaximumSize(QSize(80, 30))
        self.in2_16.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.in2_16, 17, 1, 1, 1)

        self.in2_text_17 = QLabel(self.tab_2)
        self.in2_text_17.setObjectName(u"in2_text_17")
        self.in2_text_17.setMinimumSize(QSize(80, 0))
        self.in2_text_17.setMaximumSize(QSize(80, 16777215))
        self.in2_text_17.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.in2_text_17, 18, 0, 1, 1)

        self.in2_17 = QLineEdit(self.tab_2)
        self.in2_17.setObjectName(u"in2_17")
        self.in2_17.setMinimumSize(QSize(80, 0))
        self.in2_17.setMaximumSize(QSize(80, 30))
        self.in2_17.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.in2_17, 18, 1, 1, 1)

        self.in2_text_18 = QLabel(self.tab_2)
        self.in2_text_18.setObjectName(u"in2_text_18")
        self.in2_text_18.setMinimumSize(QSize(80, 0))
        self.in2_text_18.setMaximumSize(QSize(80, 16777215))
        self.in2_text_18.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.in2_text_18, 19, 0, 1, 1)

        self.in2_18 = QLineEdit(self.tab_2)
        self.in2_18.setObjectName(u"in2_18")
        self.in2_18.setMinimumSize(QSize(80, 0))
        self.in2_18.setMaximumSize(QSize(80, 30))
        self.in2_18.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.in2_18, 19, 1, 1, 1)

        self.in2_text_19 = QLabel(self.tab_2)
        self.in2_text_19.setObjectName(u"in2_text_19")
        self.in2_text_19.setMinimumSize(QSize(80, 0))
        self.in2_text_19.setMaximumSize(QSize(80, 16777215))
        self.in2_text_19.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.in2_text_19, 20, 0, 1, 1)

        self.in2_19 = QLineEdit(self.tab_2)
        self.in2_19.setObjectName(u"in2_19")
        self.in2_19.setMinimumSize(QSize(80, 0))
        self.in2_19.setMaximumSize(QSize(80, 30))
        self.in2_19.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout_3.addWidget(self.in2_19, 20, 1, 1, 1)


        self.verticalLayout_7.addLayout(self.gridLayout_3)

        self.line_6 = QFrame(self.tab_2)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShape(QFrame.HLine)
        self.line_6.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_7.addWidget(self.line_6)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.load_in2 = QPushButton(self.tab_2)
        self.load_in2.setObjectName(u"load_in2")

        self.horizontalLayout_12.addWidget(self.load_in2)

        self.preview_in2 = QPushButton(self.tab_2)
        self.preview_in2.setObjectName(u"preview_in2")

        self.horizontalLayout_12.addWidget(self.preview_in2)


        self.verticalLayout_7.addLayout(self.horizontalLayout_12)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_3)

        self.tabWidget.addTab(self.tab_2, "")

        self.horizontalLayout_2.addWidget(self.tabWidget)

        self.widget = QWidget(self.page)
        self.widget.setObjectName(u"widget")
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QSize(500, 0))
        self.widget.setMaximumSize(QSize(500, 16777215))
        self.verticalLayout_3 = QVBoxLayout(self.widget)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.in36_configuration_view = QTableWidget(self.widget)
        if (self.in36_configuration_view.columnCount() < 3):
            self.in36_configuration_view.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.in36_configuration_view.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.in36_configuration_view.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.in36_configuration_view.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.in36_configuration_view.setObjectName(u"in36_configuration_view")

        self.verticalLayout_3.addWidget(self.in36_configuration_view)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_5)

        self.configuration_move_up = QPushButton(self.widget)
        self.configuration_move_up.setObjectName(u"configuration_move_up")

        self.horizontalLayout_10.addWidget(self.configuration_move_up)

        self.configuration_move_down = QPushButton(self.widget)
        self.configuration_move_down.setObjectName(u"configuration_move_down")

        self.horizontalLayout_10.addWidget(self.configuration_move_down)


        self.verticalLayout_3.addLayout(self.horizontalLayout_10)

        self.line = QFrame(self.widget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_3.addWidget(self.line)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label_4 = QLabel(self.widget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMaximumSize(QSize(50, 16777215))

        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)

        self.label_5 = QLabel(self.widget)
        self.label_5.setObjectName(u"label_5")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.label_5, 0, 1, 1, 1)

        self.label_6 = QLabel(self.widget)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 0, 2, 1, 1)

        self.label_7 = QLabel(self.widget)
        self.label_7.setObjectName(u"label_7")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.label_7, 0, 3, 1, 1)

        self.atomic_num = QComboBox(self.widget)
        self.atomic_num.setObjectName(u"atomic_num")
        sizePolicy3 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.atomic_num.sizePolicy().hasHeightForWidth())
        self.atomic_num.setSizePolicy(sizePolicy3)
        self.atomic_num.setMaximumSize(QSize(50, 16777215))

        self.gridLayout.addWidget(self.atomic_num, 1, 0, 1, 1)

        self.atomic_name = QComboBox(self.widget)
        self.atomic_name.setObjectName(u"atomic_name")
        sizePolicy4 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.atomic_name.sizePolicy().hasHeightForWidth())
        self.atomic_name.setSizePolicy(sizePolicy4)
        self.atomic_name.setMaximumSize(QSize(50, 16777215))

        self.gridLayout.addWidget(self.atomic_name, 1, 1, 1, 1)

        self.atomic_symbol = QComboBox(self.widget)
        self.atomic_symbol.setObjectName(u"atomic_symbol")
        self.atomic_symbol.setMaximumSize(QSize(50, 16777215))

        self.gridLayout.addWidget(self.atomic_symbol, 1, 2, 1, 1)

        self.atomic_ion = QComboBox(self.widget)
        self.atomic_ion.addItem("")
        self.atomic_ion.setObjectName(u"atomic_ion")
        sizePolicy5 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.atomic_ion.sizePolicy().hasHeightForWidth())
        self.atomic_ion.setSizePolicy(sizePolicy5)
        self.atomic_ion.setMinimumSize(QSize(50, 0))
        self.atomic_ion.setMaximumSize(QSize(50, 16777215))

        self.gridLayout.addWidget(self.atomic_ion, 1, 3, 1, 1)


        self.horizontalLayout_9.addLayout(self.gridLayout)

        self.horizontalSpacer_4 = QSpacerItem(32, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_4)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.label_11 = QLabel(self.widget)
        self.label_11.setObjectName(u"label_11")

        self.verticalLayout_6.addWidget(self.label_11)

        self.base_configuration = QLineEdit(self.widget)
        self.base_configuration.setObjectName(u"base_configuration")
        self.base_configuration.setDragEnabled(False)
        self.base_configuration.setReadOnly(True)

        self.verticalLayout_6.addWidget(self.base_configuration)


        self.horizontalLayout_9.addLayout(self.verticalLayout_6)


        self.verticalLayout_3.addLayout(self.horizontalLayout_9)

        self.line_2 = QFrame(self.widget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_3.addWidget(self.line_2)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_12 = QLabel(self.widget)
        self.label_12.setObjectName(u"label_12")

        self.horizontalLayout_4.addWidget(self.label_12)

        self.coupling_mode = QComboBox(self.widget)
        self.coupling_mode.addItem("")
        self.coupling_mode.addItem("")
        self.coupling_mode.setObjectName(u"coupling_mode")
        self.coupling_mode.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_4.addWidget(self.coupling_mode)

        self.horizontalSpacer_3 = QSpacerItem(15, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_3)

        self.label_14 = QLabel(self.widget)
        self.label_14.setObjectName(u"label_14")

        self.horizontalLayout_4.addWidget(self.label_14)

        self.in2_11_a = QSpinBox(self.widget)
        self.in2_11_a.setObjectName(u"in2_11_a")
        self.in2_11_a.setValue(90)

        self.horizontalLayout_4.addWidget(self.in2_11_a)

        self.in2_11_b = QSpinBox(self.widget)
        self.in2_11_b.setObjectName(u"in2_11_b")
        self.in2_11_b.setValue(99)

        self.horizontalLayout_4.addWidget(self.in2_11_b)

        self.in2_11_c = QSpinBox(self.widget)
        self.in2_11_c.setObjectName(u"in2_11_c")
        self.in2_11_c.setValue(90)

        self.horizontalLayout_4.addWidget(self.in2_11_c)

        self.in2_11_d = QSpinBox(self.widget)
        self.in2_11_d.setObjectName(u"in2_11_d")
        self.in2_11_d.setMaximum(99)
        self.in2_11_d.setValue(90)

        self.horizontalLayout_4.addWidget(self.in2_11_d)

        self.in2_11_e = QSpinBox(self.widget)
        self.in2_11_e.setObjectName(u"in2_11_e")
        self.in2_11_e.setValue(90)

        self.horizontalLayout_4.addWidget(self.in2_11_e)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        self.line_3 = QFrame(self.widget)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_3.addWidget(self.line_3)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_8 = QLabel(self.widget)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_5.addWidget(self.label_8)

        self.low_configuration = QComboBox(self.widget)
        self.low_configuration.setObjectName(u"low_configuration")
        self.low_configuration.setMinimumSize(QSize(50, 0))
        self.low_configuration.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_5.addWidget(self.low_configuration)

        self.high_configuration = QComboBox(self.widget)
        self.high_configuration.setObjectName(u"high_configuration")
        self.high_configuration.setMinimumSize(QSize(50, 0))
        self.high_configuration.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_5.addWidget(self.high_configuration)

        self.auto_write_in36 = QRadioButton(self.widget)
        self.auto_write_in36.setObjectName(u"auto_write_in36")
        self.auto_write_in36.setChecked(True)

        self.horizontalLayout_5.addWidget(self.auto_write_in36)

        self.manual_write_in36 = QRadioButton(self.widget)
        self.manual_write_in36.setObjectName(u"manual_write_in36")

        self.horizontalLayout_5.addWidget(self.manual_write_in36)

        self.configuration_edit = QLineEdit(self.widget)
        self.configuration_edit.setObjectName(u"configuration_edit")
        self.configuration_edit.setEnabled(False)
        self.configuration_edit.setClearButtonEnabled(True)

        self.horizontalLayout_5.addWidget(self.configuration_edit)

        self.add_configuration = QPushButton(self.widget)
        self.add_configuration.setObjectName(u"add_configuration")

        self.horizontalLayout_5.addWidget(self.add_configuration)


        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.line_5 = QFrame(self.widget)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.HLine)
        self.line_5.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_3.addWidget(self.line_5)

        self.horizontalLayout_26 = QHBoxLayout()
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.label_24 = QLabel(self.widget)
        self.label_24.setObjectName(u"label_24")

        self.horizontalLayout_26.addWidget(self.label_24)

        self.widen_temp = QDoubleSpinBox(self.widget)
        self.widen_temp.setObjectName(u"widen_temp")
        sizePolicy6 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.widen_temp.sizePolicy().hasHeightForWidth())
        self.widen_temp.setSizePolicy(sizePolicy6)
        self.widen_temp.setMinimumSize(QSize(70, 0))
        self.widen_temp.setSingleStep(0.100000000000000)
        self.widen_temp.setValue(25.600000000000001)

        self.horizontalLayout_26.addWidget(self.widen_temp)

        self.label_23 = QLabel(self.widget)
        self.label_23.setObjectName(u"label_23")

        self.horizontalLayout_26.addWidget(self.label_23)

        self.widen_fwhm = QDoubleSpinBox(self.widget)
        self.widen_fwhm.setObjectName(u"widen_fwhm")
        self.widen_fwhm.setMinimumSize(QSize(50, 0))
        self.widen_fwhm.setDecimals(3)
        self.widen_fwhm.setMaximum(10.000000000000000)
        self.widen_fwhm.setSingleStep(0.010000000000000)
        self.widen_fwhm.setValue(0.270000000000000)

        self.horizontalLayout_26.addWidget(self.widen_fwhm)

        self.label_10 = QLabel(self.widget)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_26.addWidget(self.label_10)

        self.offset = QDoubleSpinBox(self.widget)
        self.offset.setObjectName(u"offset")
        self.offset.setMinimumSize(QSize(63, 0))
        self.offset.setDecimals(3)
        self.offset.setMinimum(-50.000000000000000)
        self.offset.setMaximum(50.000000000000000)
        self.offset.setSingleStep(0.010000000000000)
        self.offset.setValue(0.000000000000000)

        self.horizontalLayout_26.addWidget(self.offset)

        self.horizontalSpacer_13 = QSpacerItem(30, 20, QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.horizontalLayout_26.addItem(self.horizontalSpacer_13)

        self.update_offect = QPushButton(self.widget)
        self.update_offect.setObjectName(u"update_offect")
        self.update_offect.setMinimumSize(QSize(75, 0))
        self.update_offect.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout_26.addWidget(self.update_offect)


        self.verticalLayout_3.addLayout(self.horizontalLayout_26)

        self.line_4 = QFrame(self.widget)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_3.addWidget(self.line_4)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.cowan_now_name = QLabel(self.widget)
        self.cowan_now_name.setObjectName(u"cowan_now_name")

        self.horizontalLayout_6.addWidget(self.cowan_now_name)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_7)

        self.run_cowan = QPushButton(self.widget)
        self.run_cowan.setObjectName(u"run_cowan")
        sizePolicy.setHeightForWidth(self.run_cowan.sizePolicy().hasHeightForWidth())
        self.run_cowan.setSizePolicy(sizePolicy)
        self.run_cowan.setMinimumSize(QSize(75, 0))
        self.run_cowan.setMaximumSize(QSize(75, 16777215))

        self.horizontalLayout_6.addWidget(self.run_cowan)


        self.verticalLayout_3.addLayout(self.horizontalLayout_6)

        self.line_10 = QFrame(self.widget)
        self.line_10.setObjectName(u"line_10")
        self.line_10.setFrameShape(QFrame.HLine)
        self.line_10.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_3.addWidget(self.line_10)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.groupBox_5 = QGroupBox(self.widget)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.gridLayout_4 = QGridLayout(self.groupBox_5)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.run_history_list = QListWidget(self.groupBox_5)
        self.run_history_list.setObjectName(u"run_history_list")
        self.run_history_list.setAlternatingRowColors(True)

        self.gridLayout_4.addWidget(self.run_history_list, 0, 0, 1, 1)


        self.horizontalLayout_7.addWidget(self.groupBox_5)

        self.groupBox_6 = QGroupBox(self.widget)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.gridLayout_5 = QGridLayout(self.groupBox_6)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.selection_list = QListWidget(self.groupBox_6)
        self.selection_list.setObjectName(u"selection_list")
        self.selection_list.setAlternatingRowColors(True)

        self.gridLayout_5.addWidget(self.selection_list, 0, 0, 1, 1)


        self.horizontalLayout_7.addWidget(self.groupBox_6)


        self.verticalLayout_3.addLayout(self.horizontalLayout_7)


        self.horizontalLayout_2.addWidget(self.widget)

        self.widget_2 = QWidget(self.page)
        self.widget_2.setObjectName(u"widget_2")
        self.verticalLayout_2 = QVBoxLayout(self.widget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_30 = QHBoxLayout()
        self.horizontalLayout_30.setObjectName(u"horizontalLayout_30")
        self.label = QLabel(self.widget_2)
        self.label.setObjectName(u"label")
        sizePolicy2.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy2)

        self.horizontalLayout_30.addWidget(self.label)

        self.horizontalSpacer_15 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_30.addItem(self.horizontalSpacer_15)

        self.redraw_exp_data = QPushButton(self.widget_2)
        self.redraw_exp_data.setObjectName(u"redraw_exp_data")

        self.horizontalLayout_30.addWidget(self.redraw_exp_data)

        self.load_exp_data = QPushButton(self.widget_2)
        self.load_exp_data.setObjectName(u"load_exp_data")

        self.horizontalLayout_30.addWidget(self.load_exp_data)


        self.verticalLayout_2.addLayout(self.horizontalLayout_30)

        self.exp_web = QWebEngineView(self.widget_2)
        self.exp_web.setObjectName(u"exp_web")
        sizePolicy7 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.exp_web.sizePolicy().hasHeightForWidth())
        self.exp_web.setSizePolicy(sizePolicy7)
        self.exp_web.setUrl(QUrl(u"about:blank"))

        self.verticalLayout_2.addWidget(self.exp_web)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_3 = QLabel(self.widget_2)
        self.label_3.setObjectName(u"label_3")
        sizePolicy2.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy2)

        self.horizontalLayout_3.addWidget(self.label_3)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)

        self.gauss = QRadioButton(self.widget_2)
        self.gauss.setObjectName(u"gauss")
        self.gauss.setEnabled(True)

        self.horizontalLayout_3.addWidget(self.gauss)

        self.crossP = QRadioButton(self.widget_2)
        self.crossP.setObjectName(u"crossP")
        self.crossP.setEnabled(True)
        sizePolicy8 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.crossP.sizePolicy().hasHeightForWidth())
        self.crossP.setSizePolicy(sizePolicy8)
        self.crossP.setAutoFillBackground(False)
        self.crossP.setChecked(True)

        self.horizontalLayout_3.addWidget(self.crossP)

        self.crossNP = QRadioButton(self.widget_2)
        self.crossNP.setObjectName(u"crossNP")
        self.crossNP.setEnabled(True)
        self.crossNP.setChecked(False)

        self.horizontalLayout_3.addWidget(self.crossNP)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.web_cal_widen = QWebEngineView(self.widget_2)
        self.web_cal_widen.setObjectName(u"web_cal_widen")
        sizePolicy7.setHeightForWidth(self.web_cal_widen.sizePolicy().hasHeightForWidth())
        self.web_cal_widen.setSizePolicy(sizePolicy7)
        self.web_cal_widen.setUrl(QUrl(u"about:blank"))

        self.verticalLayout_2.addWidget(self.web_cal_widen)

        self.label_2 = QLabel(self.widget_2)
        self.label_2.setObjectName(u"label_2")
        sizePolicy2.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy2)

        self.verticalLayout_2.addWidget(self.label_2)

        self.web_cal_line = QWebEngineView(self.widget_2)
        self.web_cal_line.setObjectName(u"web_cal_line")
        sizePolicy7.setHeightForWidth(self.web_cal_line.sizePolicy().hasHeightForWidth())
        self.web_cal_line.setSizePolicy(sizePolicy7)
        self.web_cal_line.setUrl(QUrl(u"about:blank"))

        self.verticalLayout_2.addWidget(self.web_cal_line)


        self.horizontalLayout_2.addWidget(self.widget_2)

        self.horizontalLayout_2.setStretch(2, 4)
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.verticalLayout_11 = QVBoxLayout(self.page_2)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.groupBox_3 = QGroupBox(self.page_2)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_10 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.page2_add_spectrum_web = QWebEngineView(self.groupBox_3)
        self.page2_add_spectrum_web.setObjectName(u"page2_add_spectrum_web")
        self.page2_add_spectrum_web.setMinimumSize(QSize(0, 300))
        self.page2_add_spectrum_web.setUrl(QUrl(u"about:blank"))

        self.verticalLayout_10.addWidget(self.page2_add_spectrum_web)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.show_peaks = QRadioButton(self.groupBox_3)
        self.show_peaks.setObjectName(u"show_peaks")

        self.horizontalLayout_8.addWidget(self.show_peaks)

        self.choose_peaks = QPushButton(self.groupBox_3)
        self.choose_peaks.setObjectName(u"choose_peaks")

        self.horizontalLayout_8.addWidget(self.choose_peaks)

        self.peaks_label = QLabel(self.groupBox_3)
        self.peaks_label.setObjectName(u"peaks_label")

        self.horizontalLayout_8.addWidget(self.peaks_label)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer)

        self.show_abu = QPushButton(self.groupBox_3)
        self.show_abu.setObjectName(u"show_abu")

        self.horizontalLayout_8.addWidget(self.show_abu)

        self.horizontalLayout_27 = QHBoxLayout()
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")

        self.horizontalLayout_8.addLayout(self.horizontalLayout_27)

        self.label_18 = QLabel(self.groupBox_3)
        self.label_18.setObjectName(u"label_18")

        self.horizontalLayout_8.addWidget(self.label_18)

        self.page2_temperature = QDoubleSpinBox(self.groupBox_3)
        self.page2_temperature.setObjectName(u"page2_temperature")
        self.page2_temperature.setDecimals(3)
        self.page2_temperature.setMaximum(10000.000000000000000)
        self.page2_temperature.setSingleStep(0.100000000000000)
        self.page2_temperature.setValue(25.600000000000001)

        self.horizontalLayout_8.addWidget(self.page2_temperature)

        self.label_19 = QLabel(self.groupBox_3)
        self.label_19.setObjectName(u"label_19")

        self.horizontalLayout_8.addWidget(self.label_19)

        self.page2_density_base = QDoubleSpinBox(self.groupBox_3)
        self.page2_density_base.setObjectName(u"page2_density_base")
        self.page2_density_base.setDecimals(3)
        self.page2_density_base.setSingleStep(0.100000000000000)
        self.page2_density_base.setValue(1.000000000000000)

        self.horizontalLayout_8.addWidget(self.page2_density_base)

        self.page2_density_index = QSpinBox(self.groupBox_3)
        self.page2_density_index.setObjectName(u"page2_density_index")
        self.page2_density_index.setMinimumSize(QSize(50, 0))
        self.page2_density_index.setMaximumSize(QSize(50, 16777215))
        self.page2_density_index.setValue(18)

        self.horizontalLayout_8.addWidget(self.page2_density_index)

        self.page2_plot_spectrum = QPushButton(self.groupBox_3)
        self.page2_plot_spectrum.setObjectName(u"page2_plot_spectrum")

        self.horizontalLayout_8.addWidget(self.page2_plot_spectrum)


        self.verticalLayout_10.addLayout(self.horizontalLayout_8)


        self.verticalLayout_11.addWidget(self.groupBox_3)

        self.horizontalLayout_23 = QHBoxLayout()
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.groupBox_4 = QGroupBox(self.page_2)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.horizontalLayout_22 = QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.page2_grid_list = QTableWidget(self.groupBox_4)
        self.page2_grid_list.setObjectName(u"page2_grid_list")

        self.horizontalLayout_22.addWidget(self.page2_grid_list)


        self.horizontalLayout_23.addWidget(self.groupBox_4)

        self.groupBox_2 = QGroupBox(self.page_2)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setMaximumSize(QSize(200, 16777215))
        self.verticalLayout_9 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.page2_selection_list = QListWidget(self.groupBox_2)
        self.page2_selection_list.setObjectName(u"page2_selection_list")
        self.page2_selection_list.setAlternatingRowColors(True)
        self.page2_selection_list.setProperty("isWrapping", False)
        self.page2_selection_list.setSpacing(0)
        self.page2_selection_list.setUniformItemSizes(False)
        self.page2_selection_list.setSortingEnabled(False)

        self.verticalLayout_9.addWidget(self.page2_selection_list)

        self.line_9 = QFrame(self.groupBox_2)
        self.line_9.setObjectName(u"line_9")
        self.line_9.setFrameShape(QFrame.HLine)
        self.line_9.setFrameShadow(QFrame.Sunken)

        self.verticalLayout_9.addWidget(self.line_9)

        self.horizontalLayout_21 = QHBoxLayout()
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.label_16 = QLabel(self.groupBox_2)
        self.label_16.setObjectName(u"label_16")

        self.horizontalLayout_21.addWidget(self.label_16)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_21.addItem(self.horizontalSpacer_9)

        self.temperature_num = QSpinBox(self.groupBox_2)
        self.temperature_num.setObjectName(u"temperature_num")
        self.temperature_num.setValue(10)

        self.horizontalLayout_21.addWidget(self.temperature_num)


        self.verticalLayout_9.addLayout(self.horizontalLayout_21)

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.temperature_min = QDoubleSpinBox(self.groupBox_2)
        self.temperature_min.setObjectName(u"temperature_min")
        self.temperature_min.setDecimals(3)
        self.temperature_min.setValue(20.000000000000000)

        self.horizontalLayout_18.addWidget(self.temperature_min)

        self.temperature_max = QDoubleSpinBox(self.groupBox_2)
        self.temperature_max.setObjectName(u"temperature_max")
        self.temperature_max.setDecimals(3)
        self.temperature_max.setValue(50.000000000000000)

        self.horizontalLayout_18.addWidget(self.temperature_max)


        self.verticalLayout_9.addLayout(self.horizontalLayout_18)

        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.label_17 = QLabel(self.groupBox_2)
        self.label_17.setObjectName(u"label_17")

        self.horizontalLayout_20.addWidget(self.label_17)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_20.addItem(self.horizontalSpacer_10)

        self.density_num = QSpinBox(self.groupBox_2)
        self.density_num.setObjectName(u"density_num")
        self.density_num.setValue(10)
        self.density_num.setDisplayIntegerBase(10)

        self.horizontalLayout_20.addWidget(self.density_num)


        self.verticalLayout_9.addLayout(self.horizontalLayout_20)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.density_min_base = QDoubleSpinBox(self.groupBox_2)
        self.density_min_base.setObjectName(u"density_min_base")
        self.density_min_base.setDecimals(3)
        self.density_min_base.setValue(1.000000000000000)

        self.horizontalLayout_16.addWidget(self.density_min_base)

        self.density_min_index = QSpinBox(self.groupBox_2)
        self.density_min_index.setObjectName(u"density_min_index")
        self.density_min_index.setMinimumSize(QSize(50, 0))
        self.density_min_index.setMaximumSize(QSize(50, 16777215))
        self.density_min_index.setValue(17)

        self.horizontalLayout_16.addWidget(self.density_min_index)


        self.verticalLayout_9.addLayout(self.horizontalLayout_16)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.density_max_base = QDoubleSpinBox(self.groupBox_2)
        self.density_max_base.setObjectName(u"density_max_base")
        self.density_max_base.setDecimals(3)
        self.density_max_base.setValue(1.000000000000000)

        self.horizontalLayout_17.addWidget(self.density_max_base)

        self.density_max_index = QSpinBox(self.groupBox_2)
        self.density_max_index.setObjectName(u"density_max_index")
        self.density_max_index.setMinimumSize(QSize(50, 0))
        self.density_max_index.setMaximumSize(QSize(50, 16777215))
        self.density_max_index.setValue(23)
        self.density_max_index.setDisplayIntegerBase(10)

        self.horizontalLayout_17.addWidget(self.density_max_index)


        self.verticalLayout_9.addLayout(self.horizontalLayout_17)

        self.page2_cal_grid = QPushButton(self.groupBox_2)
        self.page2_cal_grid.setObjectName(u"page2_cal_grid")

        self.verticalLayout_9.addWidget(self.page2_cal_grid)


        self.horizontalLayout_23.addWidget(self.groupBox_2)

        self.groupBox = QGroupBox(self.page_2)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setMinimumSize(QSize(300, 0))
        self.groupBox.setMaximumSize(QSize(450, 16777215))
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.label_15 = QLabel(self.groupBox)
        self.label_15.setObjectName(u"label_15")

        self.horizontalLayout_15.addWidget(self.label_15)

        self.page2_exp_data_path_name = QLineEdit(self.groupBox)
        self.page2_exp_data_path_name.setObjectName(u"page2_exp_data_path_name")
        self.page2_exp_data_path_name.setReadOnly(True)

        self.horizontalLayout_15.addWidget(self.page2_exp_data_path_name)

        self.page2_load_exp_data = QToolButton(self.groupBox)
        self.page2_load_exp_data.setObjectName(u"page2_load_exp_data")

        self.horizontalLayout_15.addWidget(self.page2_load_exp_data)

        self.plot_exp_2 = QPushButton(self.groupBox)
        self.plot_exp_2.setObjectName(u"plot_exp_2")

        self.horizontalLayout_15.addWidget(self.plot_exp_2)


        self.verticalLayout.addLayout(self.horizontalLayout_15)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.label_21 = QLabel(self.groupBox)
        self.label_21.setObjectName(u"label_21")

        self.horizontalLayout_19.addWidget(self.label_21)

        self.st_time = QLineEdit(self.groupBox)
        self.st_time.setObjectName(u"st_time")
        self.st_time.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout_19.addWidget(self.st_time)

        self.label_20 = QLabel(self.groupBox)
        self.label_20.setObjectName(u"label_20")

        self.horizontalLayout_19.addWidget(self.label_20)

        self.st_space_x = QLineEdit(self.groupBox)
        self.st_space_x.setObjectName(u"st_space_x")
        self.st_space_x.setEnabled(True)
        self.st_space_x.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout_19.addWidget(self.st_space_x)

        self.st_space_y = QLineEdit(self.groupBox)
        self.st_space_y.setObjectName(u"st_space_y")
        self.st_space_y.setEnabled(False)
        self.st_space_y.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout_19.addWidget(self.st_space_y)

        self.st_space_z = QLineEdit(self.groupBox)
        self.st_space_z.setObjectName(u"st_space_z")
        self.st_space_z.setEnabled(False)
        self.st_space_z.setMaximumSize(QSize(40, 16777215))

        self.horizontalLayout_19.addWidget(self.st_space_z)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_19.addItem(self.horizontalSpacer_8)

        self.recoder = QPushButton(self.groupBox)
        self.recoder.setObjectName(u"recoder")

        self.horizontalLayout_19.addWidget(self.recoder)

        self.line_8 = QFrame(self.groupBox)
        self.line_8.setObjectName(u"line_8")
        self.line_8.setFrameShape(QFrame.VLine)
        self.line_8.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_19.addWidget(self.line_8)

        self.load_space_time = QPushButton(self.groupBox)
        self.load_space_time.setObjectName(u"load_space_time")

        self.horizontalLayout_19.addWidget(self.load_space_time)


        self.verticalLayout.addLayout(self.horizontalLayout_19)

        self.horizontalLayout_29 = QHBoxLayout()
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.page2_cowan_obj_update = QPushButton(self.groupBox)
        self.page2_cowan_obj_update.setObjectName(u"page2_cowan_obj_update")

        self.horizontalLayout_29.addWidget(self.page2_cowan_obj_update)

        self.pushButton_2 = QPushButton(self.groupBox)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout_29.addWidget(self.pushButton_2)

        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_29.addItem(self.horizontalSpacer_14)

        self.update_similarity = QCheckBox(self.groupBox)
        self.update_similarity.setObjectName(u"update_similarity")
        self.update_similarity.setChecked(False)

        self.horizontalLayout_29.addWidget(self.update_similarity)


        self.verticalLayout.addLayout(self.horizontalLayout_29)

        self.st_resolution_table = QTableWidget(self.groupBox)
        if (self.st_resolution_table.columnCount() < 5):
            self.st_resolution_table.setColumnCount(5)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.st_resolution_table.setHorizontalHeaderItem(0, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.st_resolution_table.setHorizontalHeaderItem(1, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.st_resolution_table.setHorizontalHeaderItem(2, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.st_resolution_table.setHorizontalHeaderItem(3, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.st_resolution_table.setHorizontalHeaderItem(4, __qtablewidgetitem7)
        self.st_resolution_table.setObjectName(u"st_resolution_table")

        self.verticalLayout.addWidget(self.st_resolution_table)


        self.horizontalLayout_23.addWidget(self.groupBox)


        self.verticalLayout_11.addLayout(self.horizontalLayout_23)

        self.stackedWidget.addWidget(self.page_2)
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.gridLayout_6 = QGridLayout(self.page_4)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.groupBox_9 = QGroupBox(self.page_4)
        self.groupBox_9.setObjectName(u"groupBox_9")
        self.verticalLayout_12 = QVBoxLayout(self.groupBox_9)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.webEngineView_3 = QWebEngineView(self.groupBox_9)
        self.webEngineView_3.setObjectName(u"webEngineView_3")
        sizePolicy9 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(self.webEngineView_3.sizePolicy().hasHeightForWidth())
        self.webEngineView_3.setSizePolicy(sizePolicy9)
        self.webEngineView_3.setUrl(QUrl(u"about:blank"))

        self.verticalLayout_12.addWidget(self.webEngineView_3)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.label_13 = QLabel(self.groupBox_9)
        self.label_13.setObjectName(u"label_13")

        self.horizontalLayout_14.addWidget(self.label_13)

        self.location_select = QComboBox(self.groupBox_9)
        self.location_select.setObjectName(u"location_select")

        self.horizontalLayout_14.addWidget(self.location_select)

        self.horizontalSpacer_6 = QSpacerItem(168, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_6)

        self.td_by_t = QPushButton(self.groupBox_9)
        self.td_by_t.setObjectName(u"td_by_t")

        self.horizontalLayout_14.addWidget(self.td_by_t)


        self.verticalLayout_12.addLayout(self.horizontalLayout_14)


        self.gridLayout_6.addWidget(self.groupBox_9, 0, 0, 1, 1)

        self.groupBox_11 = QGroupBox(self.page_4)
        self.groupBox_11.setObjectName(u"groupBox_11")
        self.verticalLayout_14 = QVBoxLayout(self.groupBox_11)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.webEngineView_5 = QWebEngineView(self.groupBox_11)
        self.webEngineView_5.setObjectName(u"webEngineView_5")
        sizePolicy9.setHeightForWidth(self.webEngineView_5.sizePolicy().hasHeightForWidth())
        self.webEngineView_5.setSizePolicy(sizePolicy9)
        self.webEngineView_5.setUrl(QUrl(u"about:blank"))

        self.verticalLayout_14.addWidget(self.webEngineView_5)

        self.horizontalLayout_25 = QHBoxLayout()
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.variable_select = QComboBox(self.groupBox_11)
        self.variable_select.addItem("")
        self.variable_select.addItem("")
        self.variable_select.setObjectName(u"variable_select")

        self.horizontalLayout_25.addWidget(self.variable_select)

        self.horizontalSpacer_12 = QSpacerItem(168, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_25.addItem(self.horizontalSpacer_12)

        self.td_by_st = QPushButton(self.groupBox_11)
        self.td_by_st.setObjectName(u"td_by_st")

        self.horizontalLayout_25.addWidget(self.td_by_st)


        self.verticalLayout_14.addLayout(self.horizontalLayout_25)


        self.gridLayout_6.addWidget(self.groupBox_11, 0, 1, 2, 1)

        self.groupBox_10 = QGroupBox(self.page_4)
        self.groupBox_10.setObjectName(u"groupBox_10")
        self.verticalLayout_13 = QVBoxLayout(self.groupBox_10)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.webEngineView_4 = QWebEngineView(self.groupBox_10)
        self.webEngineView_4.setObjectName(u"webEngineView_4")
        sizePolicy9.setHeightForWidth(self.webEngineView_4.sizePolicy().hasHeightForWidth())
        self.webEngineView_4.setSizePolicy(sizePolicy9)
        self.webEngineView_4.setUrl(QUrl(u"about:blank"))

        self.verticalLayout_13.addWidget(self.webEngineView_4)

        self.horizontalLayout_24 = QHBoxLayout()
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.label_22 = QLabel(self.groupBox_10)
        self.label_22.setObjectName(u"label_22")

        self.horizontalLayout_24.addWidget(self.label_22)

        self.time_select = QComboBox(self.groupBox_10)
        self.time_select.setObjectName(u"time_select")

        self.horizontalLayout_24.addWidget(self.time_select)

        self.horizontalSpacer_11 = QSpacerItem(168, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_24.addItem(self.horizontalSpacer_11)

        self.td_by_s = QPushButton(self.groupBox_10)
        self.td_by_s.setObjectName(u"td_by_s")

        self.horizontalLayout_24.addWidget(self.td_by_s)


        self.verticalLayout_13.addLayout(self.horizontalLayout_24)


        self.gridLayout_6.addWidget(self.groupBox_10, 1, 0, 1, 1)

        self.stackedWidget.addWidget(self.page_4)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.horizontalLayout_13 = QHBoxLayout(self.page_3)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.groupBox_7 = QGroupBox(self.page_3)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.groupBox_7.setMaximumSize(QSize(300, 16777215))
        self.verticalLayout_8 = QVBoxLayout(self.groupBox_7)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.comboBox = QComboBox(self.groupBox_7)
        self.comboBox.setObjectName(u"comboBox")

        self.verticalLayout_8.addWidget(self.comboBox)

        self.treeWidget = QTreeWidget(self.groupBox_7)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.treeWidget.setHeaderItem(__qtreewidgetitem)
        self.treeWidget.setObjectName(u"treeWidget")
        self.treeWidget.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_8.addWidget(self.treeWidget)

        self.horizontalLayout_28 = QHBoxLayout()
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.page4_con_contribution = QPushButton(self.groupBox_7)
        self.page4_con_contribution.setObjectName(u"page4_con_contribution")

        self.horizontalLayout_28.addWidget(self.page4_con_contribution)

        self.page4_ion_contribution = QPushButton(self.groupBox_7)
        self.page4_ion_contribution.setObjectName(u"page4_ion_contribution")

        self.horizontalLayout_28.addWidget(self.page4_ion_contribution)


        self.verticalLayout_8.addLayout(self.horizontalLayout_28)


        self.horizontalLayout_13.addWidget(self.groupBox_7)

        self.groupBox_8 = QGroupBox(self.page_3)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.verticalLayout_5 = QVBoxLayout(self.groupBox_8)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.webEngineView = QWebEngineView(self.groupBox_8)
        self.webEngineView.setObjectName(u"webEngineView")
        self.webEngineView.setMaximumSize(QSize(16777215, 250))
        self.webEngineView.setUrl(QUrl(u"about:blank"))

        self.verticalLayout_5.addWidget(self.webEngineView)

        self.webEngineView_2 = QWebEngineView(self.groupBox_8)
        self.webEngineView_2.setObjectName(u"webEngineView_2")
        self.webEngineView_2.setUrl(QUrl(u"about:blank"))

        self.verticalLayout_5.addWidget(self.webEngineView_2)

        self.page4_consider_popular = QCheckBox(self.groupBox_8)
        self.page4_consider_popular.setObjectName(u"page4_consider_popular")

        self.verticalLayout_5.addWidget(self.page4_consider_popular)


        self.horizontalLayout_13.addWidget(self.groupBox_8)

        self.stackedWidget.addWidget(self.page_3)
        self.page_5 = QWidget()
        self.page_5.setObjectName(u"page_5")
        self.verticalLayout_15 = QVBoxLayout(self.page_5)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.statistical_table = QTableWidget(self.page_5)
        self.statistical_table.setObjectName(u"statistical_table")

        self.verticalLayout_15.addWidget(self.statistical_table)

        self.horizontalLayout_31 = QHBoxLayout()
        self.horizontalLayout_31.setObjectName(u"horizontalLayout_31")
        self.label_9 = QLabel(self.page_5)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_31.addWidget(self.label_9)

        self.page5_ion_select = QComboBox(self.page_5)
        self.page5_ion_select.setObjectName(u"page5_ion_select")

        self.horizontalLayout_31.addWidget(self.page5_ion_select)

        self.horizontalSpacer_16 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_31.addItem(self.horizontalSpacer_16)


        self.verticalLayout_15.addLayout(self.horizontalLayout_31)

        self.stackedWidget.addWidget(self.page_5)

        self.horizontalLayout.addWidget(self.stackedWidget)

        main_window.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(main_window)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1374, 22))
        self.menubar.setNativeMenuBar(True)
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        self.menu_2 = QMenu(self.menubar)
        self.menu_2.setObjectName(u"menu_2")
        self.menu_3 = QMenu(self.menubar)
        self.menu_3.setObjectName(u"menu_3")
        self.menu_4 = QMenu(self.menubar)
        self.menu_4.setObjectName(u"menu_4")
        self.menu_5 = QMenu(self.menubar)
        self.menu_5.setObjectName(u"menu_5")
        main_window.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(main_window)
        self.statusbar.setObjectName(u"statusbar")
        main_window.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menubar.addAction(self.menu_4.menuAction())
        self.menubar.addAction(self.menu_5.menuAction())
        self.menu.addAction(self.save_project)
        self.menu.addAction(self.exit_project)
        self.menu_2.addAction(self.set_xrange)
        self.menu_2.addAction(self.reset_xrange)
        self.menu_3.addAction(self.show_guides)
        self.menu_3.addAction(self.reset_cal)
        self.menu_4.addAction(self.export_data)
        self.menu_4.addAction(self.export_configuration_average_wavelength)
        self.menu_5.addAction(self.export_plot_data)

        self.retranslateUi(main_window)

        self.stackedWidget.setCurrentIndex(1)
        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(main_window)
    # setupUi

    def retranslateUi(self, main_window):
        main_window.setWindowTitle(QCoreApplication.translate("main_window", u"MainWindow", None))
        self.action.setText(QCoreApplication.translate("main_window", u"\u9000\u51fa", None))
        self.actionjiazai.setText(QCoreApplication.translate("main_window", u"jiazai ", None))
        self.action_2.setText(QCoreApplication.translate("main_window", u"\u52a0\u8f7d\u9879\u76ee", None))
        self.action_4.setText(QCoreApplication.translate("main_window", u"\u4fdd\u5b58\u4e3a", None))
        self.choose_project_path.setText(QCoreApplication.translate("main_window", u"\u8bf7\u9009\u62e9\u9879\u76ee\u8def\u5f84", None))
        self.show_guides.setText(QCoreApplication.translate("main_window", u"\u663e\u793a\u53c2\u8003\u7ebf", None))
        self.action_3.setText(QCoreApplication.translate("main_window", u"\u5c06\u8be5\u9879\u76ee\u4fdd\u5b58\u4e3a", None))
        self.action_5.setText(QCoreApplication.translate("main_window", u"\u52a0\u8f7d\u9879\u76ee", None))
        self.save_project.setText(QCoreApplication.translate("main_window", u"\u4fdd\u5b58\u9879\u76ee", None))
        self.exit_project.setText(QCoreApplication.translate("main_window", u"\u9000\u51fa", None))
        self.reset_cal.setText(QCoreApplication.translate("main_window", u"\u91cd\u7f6e\u8ba1\u7b97\u6309\u94ae", None))
        self.export_data.setText(QCoreApplication.translate("main_window", u"\u5bfc\u51fa\u6570\u636e", None))
        self.set_xrange.setText(QCoreApplication.translate("main_window", u"\u8bbe\u7f6e\u6ce2\u957f\u8303\u56f4", None))
        self.reset_xrange.setText(QCoreApplication.translate("main_window", u"\u91cd\u7f6e\u6ce2\u957f\u8303\u56f4", None))
        self.export_configuration_average_wavelength.setText(QCoreApplication.translate("main_window", u"\u5bfc\u51fa\u7ec4\u6001\u5e73\u5747\u6ce2\u957f", None))
        self.export_plot_data.setText(QCoreApplication.translate("main_window", u"\u5f00\u542f\u5bfc\u51fa", None))

        __sortingEnabled = self.navigation.isSortingEnabled()
        self.navigation.setSortingEnabled(False)
        ___qlistwidgetitem = self.navigation.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("main_window", u"\u5149\u8c31\u6307\u8ba4", None));
        ___qlistwidgetitem1 = self.navigation.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("main_window", u"\u5b9e\u9a8c\u8c31\u7ebf\u6a21\u62df", None));
        ___qlistwidgetitem2 = self.navigation.item(2)
        ___qlistwidgetitem2.setText(QCoreApplication.translate("main_window", u"\u6f14\u5316\u8fc7\u7a0b", None));
        ___qlistwidgetitem3 = self.navigation.item(3)
        ___qlistwidgetitem3.setText(QCoreApplication.translate("main_window", u"\u7ec4\u6001\u8d21\u732e", None));
        ___qlistwidgetitem4 = self.navigation.item(4)
        ___qlistwidgetitem4.setText(QCoreApplication.translate("main_window", u"\u6570\u636e\u7edf\u8ba1", None));
        self.navigation.setSortingEnabled(__sortingEnabled)

#if QT_CONFIG(tooltip)
        self.in36_text_1.setToolTip(QCoreApplication.translate("main_window", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(whatsthis)
        self.in36_text_1.setWhatsThis(QCoreApplication.translate("main_window", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(whatsthis)
        self.in36_text_1.setText(QCoreApplication.translate("main_window", u"ITPOW", None))
        self.in36_1.setText(QCoreApplication.translate("main_window", u"2", None))
        self.in36_1.setPlaceholderText(QCoreApplication.translate("main_window", u"I1", None))
        self.in36_text_2.setText(QCoreApplication.translate("main_window", u"IPTVU", None))
        self.in36_2.setPlaceholderText(QCoreApplication.translate("main_window", u"I1", None))
        self.in36_text_3.setText(QCoreApplication.translate("main_window", u"IPTEB", None))
        self.in36_3.setPlaceholderText(QCoreApplication.translate("main_window", u"I1", None))
#if QT_CONFIG(tooltip)
        self.in36_text_4.setToolTip(QCoreApplication.translate("main_window", u"<html><head/><body><p>&lt; 0\uff0c<span style=\" font-family:'\u5b8b\u4f53';\">\u4e0d\u6253\u5370\u6ce2\u51fd\u6570</span></p><p>&gt;0<span style=\" font-family:'\u5b8b\u4f53';\">\uff0c\u5728\u6bcf\u7b2c\u4e94\u4e2a\u7f51\u683c\u70b9\u6253\u5370\u524d\u4e24\u4e2a\u548c\u6700\u540e\u4e00\u4e2a</span> NORBPT <span style=\" font-family:'\u5b8b\u4f53';\">\u6ce2\u51fd\u6570</span></p><p>&gt;5<span style=\" font-family:'\u5b8b\u4f53';\">\uff0c\u5728\u6bcf\u4e2a\u7f51\u683c\u70b9\u6253\u5370\u8fde\u7eed\u6ce2\u51fd\u6570</span></p><p>=-9<span style=\" font-family:'\u5b8b\u4f53';\">\uff0c\u8f93\u51fa\u6240\u6709\u6ce2\u51fd\u6570</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.in36_text_4.setText(QCoreApplication.translate("main_window", u"NORBPT", None))
#if QT_CONFIG(tooltip)
        self.in36_4.setToolTip(QCoreApplication.translate("main_window", u"<html><head/><body><p><span style=\" font-size:12pt;\">|NORBPT &lt; 0| ==&gt; \u4e0d\u6253\u5370\u6ce2\u51fd\u6570</span></p><p><span style=\" font-size:12pt;\">|NORBPT &gt; 0| ==&gt; \u5728\u6bcf\u7b2c\u4e94\u4e2a\u7f51\u683c\u70b9\u6253\u5370\u524d\u4e24\u4e2a\u548c\u6700\u540e\u4e00\u4e2a -NORBPT- \u6ce2\u51fd\u6570</span></p><p><span style=\" font-size:12pt;\">|NORBPT &gt; 5| ==&gt; \u5728\u6bcf\u4e2a\u7f51\u683c\u70b9\u6253\u5370\u8fde\u7eed\u4ecb\u8d28\u6ce2\u51fd\u6570\uff0c\u5728tape2 \u6216 tape7\u4e0a\u5199\u5165\u6700\u540e\u7684 -NORBPT- \u4e2a\u6ce2\u51fd\u6570\uff08\u81f3\u5c11\u4e3a2\uff1b\u5982\u679c -NORBPT- = 9\uff0c\u5199\u5165\u6240\u6709\u6ce2\u51fd\u6570\uff09</span></p><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.in36_4.setText(QCoreApplication.translate("main_window", u"-9", None))
        self.in36_4.setPlaceholderText(QCoreApplication.translate("main_window", u"I2", None))
        self.in36_text_5.setText(QCoreApplication.translate("main_window", u"IZHXBW", None))
        self.in36_5.setText("")
        self.in36_5.setPlaceholderText(QCoreApplication.translate("main_window", u"I1", None))
        self.in36_text_6.setText(QCoreApplication.translate("main_window", u"IPHFWF", None))
        self.in36_6.setPlaceholderText(QCoreApplication.translate("main_window", u"I2", None))
        self.in36_text_7.setText(QCoreApplication.translate("main_window", u"IHF", None))
        self.in36_7.setText(QCoreApplication.translate("main_window", u"2", None))
        self.in36_7.setPlaceholderText(QCoreApplication.translate("main_window", u"I2", None))
        self.in36_text_8.setText(QCoreApplication.translate("main_window", u"IBB", None))
        self.in36_8.setPlaceholderText(QCoreApplication.translate("main_window", u"I3", None))
        self.in36_text_9.setText(QCoreApplication.translate("main_window", u"TOLSTB", None))
        self.in36_9.setText(QCoreApplication.translate("main_window", u"10", None))
        self.in36_9.setPlaceholderText(QCoreApplication.translate("main_window", u"F2.1", None))
        self.in36_text_10.setText(QCoreApplication.translate("main_window", u"TOLKM2", None))
        self.in36_10.setText(QCoreApplication.translate("main_window", u"1.0", None))
        self.in36_10.setPlaceholderText(QCoreApplication.translate("main_window", u"E5.1", None))
        self.in36_text_11.setText(QCoreApplication.translate("main_window", u"TOLEND", None))
        self.in36_11.setText(QCoreApplication.translate("main_window", u"5.e-08", None))
        self.in36_11.setPlaceholderText(QCoreApplication.translate("main_window", u"E10.1", None))
        self.in36_text_12.setText(QCoreApplication.translate("main_window", u"THRESH", None))
        self.in36_12.setText(QCoreApplication.translate("main_window", u"1.e-11", None))
        self.in36_12.setPlaceholderText(QCoreApplication.translate("main_window", u"E10.1", None))
        self.in36_text_13.setText(QCoreApplication.translate("main_window", u"KUTD", None))
#if QT_CONFIG(tooltip)
        self.in36_13.setToolTip(QCoreApplication.translate("main_window", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.in36_13.setText(QCoreApplication.translate("main_window", u"-2", None))
        self.in36_13.setPlaceholderText(QCoreApplication.translate("main_window", u"I2", None))
        self.in36_text_14.setText(QCoreApplication.translate("main_window", u"KUT1", None))
        self.in36_14.setPlaceholderText(QCoreApplication.translate("main_window", u"I2", None))
        self.in36_text_15.setText(QCoreApplication.translate("main_window", u"IVINTI", None))
        self.in36_15.setPlaceholderText(QCoreApplication.translate("main_window", u"I1", None))
        self.in36_text_16.setText(QCoreApplication.translate("main_window", u"IRELb", None))
        self.in36_16.setText(QCoreApplication.translate("main_window", u"1", None))
        self.in36_16.setPlaceholderText(QCoreApplication.translate("main_window", u"I1", None))
        self.in36_text_17.setText(QCoreApplication.translate("main_window", u"MAXIT", None))
        self.in36_17.setText(QCoreApplication.translate("main_window", u"90", None))
        self.in36_17.setPlaceholderText(QCoreApplication.translate("main_window", u"I2", None))
        self.in36_text_18.setText(QCoreApplication.translate("main_window", u"NPR", None))
        self.in36_18.setPlaceholderText(QCoreApplication.translate("main_window", u"I2", None))
        self.in36_text_19.setText(QCoreApplication.translate("main_window", u"EXF10", None))
        self.in36_19.setText(QCoreApplication.translate("main_window", u"1.0", None))
        self.in36_19.setPlaceholderText(QCoreApplication.translate("main_window", u"F5.5", None))
        self.in36_text_20.setText(QCoreApplication.translate("main_window", u"EXFM1", None))
        self.in36_20.setText(QCoreApplication.translate("main_window", u"0.65", None))
        self.in36_20.setPlaceholderText(QCoreApplication.translate("main_window", u"F5.5", None))
        self.in36_text_21.setText(QCoreApplication.translate("main_window", u"EMXc", None))
        self.in36_21.setText(QCoreApplication.translate("main_window", u"0.0", None))
        self.in36_21.setPlaceholderText(QCoreApplication.translate("main_window", u"F5.5", None))
        self.in36_text_22.setText(QCoreApplication.translate("main_window", u"CORRFd", None))
        self.in36_22.setText(QCoreApplication.translate("main_window", u"0.0", None))
        self.in36_22.setPlaceholderText(QCoreApplication.translate("main_window", u"F5.5", None))
        self.in36_text_23.setText(QCoreApplication.translate("main_window", u"IW6e", None))
        self.in36_23.setText("")
        self.in36_23.setPlaceholderText(QCoreApplication.translate("main_window", u"I5", None))
        self.load_in36.setText(QCoreApplication.translate("main_window", u"\u52a0\u8f7din36", None))
        self.preview_in36.setText(QCoreApplication.translate("main_window", u"in36\u6587\u4ef6\u9884\u89c8", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("main_window", u"in36\u7f16\u8f91", None))
        self.in2_text_1.setText(QCoreApplication.translate("main_window", u"\u5b50\u7a0b\u5e8f", None))
        self.in2_1.setText(QCoreApplication.translate("main_window", u"g5inp", None))
        self.in2_1.setPlaceholderText(QCoreApplication.translate("main_window", u"A3,2X", None))
        self.in2_text_2.setText(QCoreApplication.translate("main_window", u"NCK", None))
        self.in2_2.setPlaceholderText(QCoreApplication.translate("main_window", u"A2", None))
        self.in2_text_3.setText(QCoreApplication.translate("main_window", u"IOVF ACT", None))
        self.in2_3.setText(QCoreApplication.translate("main_window", u"0", None))
        self.in2_3.setPlaceholderText(QCoreApplication.translate("main_window", u"I1", None))
        self.in2_text_4.setText(QCoreApplication.translate("main_window", u"NOCET", None))
        self.in2_4.setText(QCoreApplication.translate("main_window", u"0", None))
        self.in2_4.setPlaceholderText(QCoreApplication.translate("main_window", u"I2", None))
        self.in2_text_5.setText(QCoreApplication.translate("main_window", u"NSCONF(3,1)", None))
        self.in2_5.setText(QCoreApplication.translate("main_window", u"0", None))
        self.in2_5.setPlaceholderText(QCoreApplication.translate("main_window", u"I1", None))
        self.in2_text_6.setText(QCoreApplication.translate("main_window", u"NSCONF(3,2)", None))
        self.in2_6.setText(QCoreApplication.translate("main_window", u"00", None))
        self.in2_6.setPlaceholderText(QCoreApplication.translate("main_window", u"I2", None))
        self.in2_text_7.setText(QCoreApplication.translate("main_window", u"EA V11 ", None))
        self.in2_7.setText(QCoreApplication.translate("main_window", u"0.000", None))
        self.in2_7.setPlaceholderText(QCoreApplication.translate("main_window", u"F7.4", None))
        self.in2_text_8.setText(QCoreApplication.translate("main_window", u"IABG ", None))
        self.in2_8.setPlaceholderText(QCoreApplication.translate("main_window", u"I1", None))
        self.in2_text_9.setText(QCoreApplication.translate("main_window", u"OPTION", None))
        self.in2_9_a.setText(QCoreApplication.translate("main_window", u"00000000", None))
        self.in2_9_a.setPlaceholderText(QCoreApplication.translate("main_window", u"A8", None))
        self.in2_9_b.setText(QCoreApplication.translate("main_window", u"0000000", None))
        self.in2_9_b.setPlaceholderText(QCoreApplication.translate("main_window", u"A8", None))
        self.in2_9_c.setText(QCoreApplication.translate("main_window", u"00000", None))
        self.in2_9_c.setPlaceholderText(QCoreApplication.translate("main_window", u"A8", None))
        self.in2_9_d.setText(QCoreApplication.translate("main_window", u"000", None))
        self.in2_9_d.setPlaceholderText(QCoreApplication.translate("main_window", u"A4", None))
        self.in2_text_10.setText(QCoreApplication.translate("main_window", u"IQUAD", None))
        self.in2_10.setText(QCoreApplication.translate("main_window", u"0", None))
        self.in2_10.setPlaceholderText(QCoreApplication.translate("main_window", u"I1", None))
        self.in2_text_12.setText(QCoreApplication.translate("main_window", u"DMIN ", None))
        self.in2_12.setText(QCoreApplication.translate("main_window", u".0000", None))
        self.in2_12.setPlaceholderText(QCoreApplication.translate("main_window", u"A5", None))
        self.in2_text_13.setText(QCoreApplication.translate("main_window", u"IPRINT", None))
        self.in2_13.setText("")
        self.in2_13.setPlaceholderText(QCoreApplication.translate("main_window", u"A5", None))
        self.in2_text_14.setText(QCoreApplication.translate("main_window", u"IENGYD", None))
        self.in2_14.setText(QCoreApplication.translate("main_window", u"0", None))
        self.in2_14.setPlaceholderText(QCoreApplication.translate("main_window", u"A1", None))
        self.in2_text_15.setText(QCoreApplication.translate("main_window", u"ISPECC", None))
        self.in2_15.setText(QCoreApplication.translate("main_window", u"7", None))
        self.in2_15.setPlaceholderText(QCoreApplication.translate("main_window", u"A1", None))
        self.in2_text_16.setText(QCoreApplication.translate("main_window", u"ICON", None))
        self.in2_16.setText(QCoreApplication.translate("main_window", u"2", None))
        self.in2_16.setPlaceholderText(QCoreApplication.translate("main_window", u"I1", None))
        self.in2_text_17.setText(QCoreApplication.translate("main_window", u"ISLI", None))
        self.in2_17.setText(QCoreApplication.translate("main_window", u"2", None))
        self.in2_17.setPlaceholderText(QCoreApplication.translate("main_window", u"I1", None))
        self.in2_text_18.setText(QCoreApplication.translate("main_window", u"IDIP", None))
        self.in2_18.setText(QCoreApplication.translate("main_window", u"9", None))
        self.in2_18.setPlaceholderText(QCoreApplication.translate("main_window", u"I1", None))
        self.in2_text_19.setText(QCoreApplication.translate("main_window", u"ALF", None))
        self.in2_19.setPlaceholderText(QCoreApplication.translate("main_window", u"F5.0", None))
        self.load_in2.setText(QCoreApplication.translate("main_window", u"\u52a0\u8f7din2", None))
        self.preview_in2.setText(QCoreApplication.translate("main_window", u"in2\u6587\u4ef6\u9884\u89c8", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("main_window", u"in2\u7f16\u8f91", None))
        ___qtablewidgetitem = self.in36_configuration_view.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("main_window", u"\u5b87\u79f0", None));
        ___qtablewidgetitem1 = self.in36_configuration_view.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("main_window", u"\u539f\u5b50\u72b6\u6001", None));
        ___qtablewidgetitem2 = self.in36_configuration_view.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("main_window", u"\u7ec4\u6001", None));
        self.configuration_move_up.setText(QCoreApplication.translate("main_window", u"\u4e0a\u79fb", None))
        self.configuration_move_down.setText(QCoreApplication.translate("main_window", u"\u4e0b\u79fb", None))
        self.label_4.setText(QCoreApplication.translate("main_window", u"\u5e8f\u6570", None))
        self.label_5.setText(QCoreApplication.translate("main_window", u"\u540d\u79f0", None))
        self.label_6.setText(QCoreApplication.translate("main_window", u"\u7b26\u53f7", None))
        self.label_7.setText(QCoreApplication.translate("main_window", u"\u79bb\u5316\u5ea6", None))
        self.atomic_ion.setItemText(0, QCoreApplication.translate("main_window", u"0", None))

        self.label_11.setText(QCoreApplication.translate("main_window", u"\u57fa\u7ec4\u6001", None))
        self.base_configuration.setText(QCoreApplication.translate("main_window", u"1s01", None))
        self.label_12.setText(QCoreApplication.translate("main_window", u"\u8026\u5408\u65b9\u5f0f", None))
        self.coupling_mode.setItemText(0, QCoreApplication.translate("main_window", u"L-S", None))
        self.coupling_mode.setItemText(1, QCoreApplication.translate("main_window", u"j-j", None))

        self.label_14.setText(QCoreApplication.translate("main_window", u"\u65af\u83b1\u7279\u7cfb\u6570", None))
        self.label_8.setText(QCoreApplication.translate("main_window", u"\u652f\u58f3\u5c42", None))
        self.auto_write_in36.setText(QCoreApplication.translate("main_window", u"\u81ea\u52a8", None))
        self.manual_write_in36.setText(QCoreApplication.translate("main_window", u"\u624b\u52a8", None))
#if QT_CONFIG(tooltip)
        self.configuration_edit.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.configuration_edit.setStatusTip("")
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.configuration_edit.setWhatsThis(QCoreApplication.translate("main_window", u"<html><head/><body><p><br/></p></body></html>", None))
#endif // QT_CONFIG(whatsthis)
#if QT_CONFIG(accessibility)
        self.configuration_edit.setAccessibleDescription("")
#endif // QT_CONFIG(accessibility)
        self.configuration_edit.setInputMask("")
        self.configuration_edit.setText("")
        self.configuration_edit.setPlaceholderText(QCoreApplication.translate("main_window", u"\u7535\u5b50\u7ec4\u6001", None))
        self.add_configuration.setText(QCoreApplication.translate("main_window", u"\u6dfb\u52a0", None))
        self.label_24.setText(QCoreApplication.translate("main_window", u"\u5c55\u5bbd\u6e29\u5ea6", None))
        self.widen_temp.setSuffix(QCoreApplication.translate("main_window", u"eV", None))
        self.label_23.setText(QCoreApplication.translate("main_window", u"FWHM", None))
        self.widen_fwhm.setSuffix(QCoreApplication.translate("main_window", u"eV", None))
        self.label_10.setText(QCoreApplication.translate("main_window", u"\u504f\u79fb", None))
        self.offset.setSuffix(QCoreApplication.translate("main_window", u"nm", None))
        self.update_offect.setText(QCoreApplication.translate("main_window", u"\u91cd\u65b0\u5c55\u5bbd", None))
        self.cowan_now_name.setText(QCoreApplication.translate("main_window", u"\u5f53\u524d\u5c55\u793a\uff1a", None))
        self.run_cowan.setText(QCoreApplication.translate("main_window", u"\u8ba1\u7b97", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("main_window", u"\u8ba1\u7b97\u5386\u53f2", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("main_window", u"\u5e93", None))
        self.label.setText(QCoreApplication.translate("main_window", u"\u5b9e\u9a8c\u8c31", None))
        self.redraw_exp_data.setText(QCoreApplication.translate("main_window", u"\u91cd\u65b0\u7ed8\u5236", None))
        self.load_exp_data.setText(QCoreApplication.translate("main_window", u"\u52a0\u8f7d\u5b9e\u9a8c\u5149\u8c31", None))
        self.label_3.setText(QCoreApplication.translate("main_window", u"\u8f6e\u5ed3", None))
        self.gauss.setText(QCoreApplication.translate("main_window", u"gauss", None))
        self.crossP.setText(QCoreApplication.translate("main_window", u"cross-P", None))
        self.crossNP.setText(QCoreApplication.translate("main_window", u"cross-NP", None))
        self.label_2.setText(QCoreApplication.translate("main_window", u"\u8ba1\u7b97\u8c31", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("main_window", u"\u6a21\u62df\u8c31\u7ebf", None))
        self.show_peaks.setText("")
        self.choose_peaks.setText(QCoreApplication.translate("main_window", u"\u7279\u5f81\u5cf0\u6311\u9009", None))
        self.peaks_label.setText(QCoreApplication.translate("main_window", u"\u672a\u6307\u5b9a", None))
        self.show_abu.setText(QCoreApplication.translate("main_window", u"\u67e5\u770b\u5404\u79bb\u5b50\u7684\u4e30\u5ea6", None))
        self.label_18.setText(QCoreApplication.translate("main_window", u"\u6e29\u5ea6", None))
        self.page2_temperature.setPrefix("")
        self.page2_temperature.setSuffix("")
        self.label_19.setText(QCoreApplication.translate("main_window", u"\u5bc6\u5ea6", None))
        self.page2_plot_spectrum.setText(QCoreApplication.translate("main_window", u"\u6a21\u62df", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("main_window", u"\u7f51\u683c\u8ba1\u7b97", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("main_window", u"\u53c2\u6570\u8f93\u5165\u533a", None))
        self.label_16.setText(QCoreApplication.translate("main_window", u"\u6e29\u5ea6\u8303\u56f4", None))
        self.temperature_num.setSuffix(QCoreApplication.translate("main_window", u"\u4e2a", None))
        self.label_17.setText(QCoreApplication.translate("main_window", u"\u5bc6\u5ea6\u8303\u56f4", None))
        self.density_num.setSuffix(QCoreApplication.translate("main_window", u"\u4e2a", None))
        self.page2_cal_grid.setText(QCoreApplication.translate("main_window", u"\u5f00\u59cb\u8ba1\u7b97", None))
        self.groupBox.setTitle(QCoreApplication.translate("main_window", u"\u65f6\u7a7a\u5206\u8fa8", None))
        self.label_15.setText(QCoreApplication.translate("main_window", u"\u5b9e\u9a8c\u6570\u636e", None))
        self.page2_load_exp_data.setText(QCoreApplication.translate("main_window", u"...", None))
        self.plot_exp_2.setText(QCoreApplication.translate("main_window", u"\u7ed8\u5236", None))
        self.label_21.setText(QCoreApplication.translate("main_window", u"\u65f6\u95f4", None))
        self.st_time.setText(QCoreApplication.translate("main_window", u"1", None))
        self.label_20.setText(QCoreApplication.translate("main_window", u"\u4f4d\u7f6e", None))
        self.st_space_x.setText(QCoreApplication.translate("main_window", u"1", None))
        self.st_space_y.setText(QCoreApplication.translate("main_window", u"0", None))
        self.st_space_z.setText(QCoreApplication.translate("main_window", u"0", None))
        self.recoder.setText(QCoreApplication.translate("main_window", u"\u8bb0\u5f55", None))
        self.load_space_time.setText(QCoreApplication.translate("main_window", u"\u6279\u91cf\u52a0\u8f7d", None))
        self.page2_cowan_obj_update.setText(QCoreApplication.translate("main_window", u"\u66f4\u65b0cowan\u5bf9\u8c61", None))
        self.pushButton_2.setText(QCoreApplication.translate("main_window", u"\u6d4b\u8bd5\u6309\u94ae", None))
        self.update_similarity.setText(QCoreApplication.translate("main_window", u"\u66f4\u65b0\u7f51\u683c\u76f8\u4f3c\u5ea6", None))
        ___qtablewidgetitem3 = self.st_resolution_table.horizontalHeaderItem(0)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("main_window", u"\u65f6\u95f4", None));
        ___qtablewidgetitem4 = self.st_resolution_table.horizontalHeaderItem(1)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("main_window", u"\u4f4d\u7f6e", None));
        ___qtablewidgetitem5 = self.st_resolution_table.horizontalHeaderItem(2)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("main_window", u"\u6e29\u5ea6", None));
        ___qtablewidgetitem6 = self.st_resolution_table.horizontalHeaderItem(3)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("main_window", u"\u5bc6\u5ea6", None));
        ___qtablewidgetitem7 = self.st_resolution_table.horizontalHeaderItem(4)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("main_window", u"\u5b9e\u9a8c\u8c31\u6587\u4ef6\u540d", None));
        self.groupBox_9.setTitle(QCoreApplication.translate("main_window", u"\u968f\u65f6\u95f4\u7684\u53d8\u5316", None))
        self.label_13.setText(QCoreApplication.translate("main_window", u"\u4f4d\u7f6e\u9009\u62e9", None))
        self.td_by_t.setText(QCoreApplication.translate("main_window", u"\u7ed8\u5236", None))
        self.groupBox_11.setTitle(QCoreApplication.translate("main_window", u"\u4e8c\u4f4d\u70ed\u529b\u56fe", None))
        self.variable_select.setItemText(0, QCoreApplication.translate("main_window", u"\u6e29\u5ea6", None))
        self.variable_select.setItemText(1, QCoreApplication.translate("main_window", u"\u5bc6\u5ea6", None))

        self.td_by_st.setText(QCoreApplication.translate("main_window", u"\u7ed8\u5236", None))
        self.groupBox_10.setTitle(QCoreApplication.translate("main_window", u"\u968f\u4f4d\u7f6e\u7684\u53d8\u5316", None))
        self.label_22.setText(QCoreApplication.translate("main_window", u"\u65f6\u95f4\u9009\u62e9", None))
        self.td_by_s.setText(QCoreApplication.translate("main_window", u"\u7ed8\u5236", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("main_window", u"GroupBox", None))
        self.page4_con_contribution.setText(QCoreApplication.translate("main_window", u"\u67e5\u770b\u5404\u7ec4\u6001\u7684\u8d21\u732e", None))
        self.page4_ion_contribution.setText(QCoreApplication.translate("main_window", u"\u67e5\u770b\u5404\u79bb\u5b50\u7684\u8d21\u732e", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("main_window", u"GroupBox", None))
        self.page4_consider_popular.setText(QCoreApplication.translate("main_window", u"\u8003\u8651\u5e03\u5c45", None))
        self.label_9.setText(QCoreApplication.translate("main_window", u"\u8bf7\u9009\u62e9\u79bb\u5316\u5ea6", None))
        self.menu.setTitle(QCoreApplication.translate("main_window", u"\u6587\u4ef6", None))
        self.menu_2.setTitle(QCoreApplication.translate("main_window", u"\u8ba1\u7b97", None))
        self.menu_3.setTitle(QCoreApplication.translate("main_window", u"\u5de5\u5177", None))
        self.menu_4.setTitle(QCoreApplication.translate("main_window", u"\u5bfc\u51fa", None))
        self.menu_5.setTitle(QCoreApplication.translate("main_window", u"\u8bbe\u7f6e", None))
    # retranslateUi

