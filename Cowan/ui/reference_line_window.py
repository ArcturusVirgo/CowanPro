# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'reference_line_window.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
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
from PySide6.QtWidgets import (QApplication, QFrame, QLabel, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_reference_line_window(object):
    def setupUi(self, reference_line_window):
        if not reference_line_window.objectName():
            reference_line_window.setObjectName(u"reference_line_window")
        reference_line_window.resize(100, 800)
        reference_line_window.setMaximumSize(QSize(16777215, 16777215))
        reference_line_window.setCursor(QCursor(Qt.ArrowCursor))
        reference_line_window.setMouseTracking(True)
        reference_line_window.setWindowOpacity(1.000000000000000)
        reference_line_window.setLayoutDirection(Qt.RightToLeft)
        reference_line_window.setAutoFillBackground(False)
        self.verticalLayout = QVBoxLayout(reference_line_window)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.line = QFrame(reference_line_window)
        self.line.setObjectName(u"line")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy)
        self.line.setStyleSheet(u"background-color:rgb(0, 0, 0);")
        self.line.setFrameShadow(QFrame.Plain)
        self.line.setLineWidth(1)
        self.line.setMidLineWidth(-1)
        self.line.setFrameShape(QFrame.VLine)

        self.verticalLayout.addWidget(self.line, 0, Qt.AlignHCenter)

        self.label = QLabel(reference_line_window)
        self.label.setObjectName(u"label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)
        self.label.setMinimumSize(QSize(20, 20))
        self.label.setMaximumSize(QSize(20, 20))
        self.label.setCursor(QCursor(Qt.SizeAllCursor))
        self.label.setStyleSheet(u"border-style: solid;\n"
"border-width: 2px;\n"
"border-color: black;\n"
"border: 2px solid red;\n"
"border-radius: 3px;\n"
"background-color:red;")
        self.label.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.label, 0, Qt.AlignHCenter|Qt.AlignVCenter)


        self.retranslateUi(reference_line_window)

        QMetaObject.connectSlotsByName(reference_line_window)
    # setupUi

    def retranslateUi(self, reference_line_window):
        reference_line_window.setWindowTitle(QCoreApplication.translate("reference_line_window", u"Form", None))
        self.label.setText("")
    # retranslateUi

