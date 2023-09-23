from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton


class NonStopProgressDialog(QtWidgets.QProgressDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowModality(Qt.WindowModal)
        self.setCancelButton(None)
        self.autoClose()
        self.resize(500, 75)

    # def reject(self):
    #     pass
    #
    # def closeEvent(self, event):
    #     if event.spontaneous():
    #         event.ignore()


