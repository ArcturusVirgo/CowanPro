# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'login_window.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QListWidget, QListWidgetItem, QPushButton, QSizePolicy,
    QSpacerItem, QStackedWidget, QToolButton, QVBoxLayout,
    QWidget)

class Ui_login_window(object):
    def setupUi(self, login_window):
        if not login_window.objectName():
            login_window.setObjectName(u"login_window")
        login_window.resize(299, 400)
        self.verticalLayout = QVBoxLayout(login_window)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(login_window)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(0, 70))

        self.verticalLayout.addWidget(self.label)

        self.stackedWidget = QStackedWidget(login_window)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.verticalLayout_2 = QVBoxLayout(self.page)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_2 = QLabel(self.page)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout.addWidget(self.label_2)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.project_list = QListWidget(self.page)
        self.project_list.setObjectName(u"project_list")

        self.verticalLayout_2.addWidget(self.project_list)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.new_project = QPushButton(self.page)
        self.new_project.setObjectName(u"new_project")

        self.horizontalLayout_2.addWidget(self.new_project)

        self.delete_project = QPushButton(self.page)
        self.delete_project.setObjectName(u"delete_project")

        self.horizontalLayout_2.addWidget(self.delete_project)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.stackedWidget.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.verticalLayout_3 = QVBoxLayout(self.page_2)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.label_3 = QLabel(self.page_2)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_3.addWidget(self.label_3)

        self.project_name = QLineEdit(self.page_2)
        self.project_name.setObjectName(u"project_name")
        self.project_name.setEnabled(True)

        self.verticalLayout_3.addWidget(self.project_name)

        self.label_4 = QLabel(self.page_2)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_3.addWidget(self.label_4)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.project_path = QLineEdit(self.page_2)
        self.project_path.setObjectName(u"project_path")
        self.project_path.setEnabled(False)

        self.horizontalLayout_3.addWidget(self.project_path)

        self.select_path = QToolButton(self.page_2)
        self.select_path.setObjectName(u"select_path")

        self.horizontalLayout_3.addWidget(self.select_path)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.verticalSpacer = QSpacerItem(20, 153, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.back = QPushButton(self.page_2)
        self.back.setObjectName(u"back")

        self.horizontalLayout_4.addWidget(self.back)

        self.create_project = QPushButton(self.page_2)
        self.create_project.setObjectName(u"create_project")

        self.horizontalLayout_4.addWidget(self.create_project)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        self.stackedWidget.addWidget(self.page_2)

        self.verticalLayout.addWidget(self.stackedWidget)


        self.retranslateUi(login_window)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(login_window)
    # setupUi

    def retranslateUi(self, login_window):
        login_window.setWindowTitle(QCoreApplication.translate("login_window", u"Form", None))
        self.label.setText(QCoreApplication.translate("login_window", u"Cowan\u53ef\u89c6\u5316\u754c\u9762\u7a0b\u5e8f", None))
        self.label_2.setText(QCoreApplication.translate("login_window", u"\u9879\u76ee\u5217\u8868", None))
        self.new_project.setText(QCoreApplication.translate("login_window", u"\u65b0\u5efa\u9879\u76ee", None))
        self.delete_project.setText(QCoreApplication.translate("login_window", u"\u5220\u9664\u9879\u76ee", None))
        self.label_3.setText(QCoreApplication.translate("login_window", u"\u9879\u76ee\u540d\u79f0", None))
        self.label_4.setText(QCoreApplication.translate("login_window", u"\u9879\u76ee\u8def\u5f84", None))
        self.select_path.setText(QCoreApplication.translate("login_window", u"...", None))
        self.back.setText(QCoreApplication.translate("login_window", u"\u8fd4\u56de\u4e0a\u4e00\u9875", None))
        self.create_project.setText(QCoreApplication.translate("login_window", u"\u521b\u5efa\u9879\u76ee", None))
    # retranslateUi

