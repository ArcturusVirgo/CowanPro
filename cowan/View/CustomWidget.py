from PySide6.QtWidgets import QWidget, QProgressBar, QLabel, QVBoxLayout, QMessageBox, QFileDialog
from PySide6.QtCore import Qt


class CustomProgressDialog(QWidget):
    """
    自定义进度条对话框
    """

    def __init__(self, dialog_title, range_=(0, 0)):
        super().__init__()
        self.setWindowModality(Qt.WindowModal)
        self.resize(500, 75)
        self.set_window_title(dialog_title)
        self.setWindowFlags(Qt.WindowMinimizeButtonHint)
        # 设置父窗口不能点击的模态
        self.setWindowModality(Qt.ApplicationModal)

        self.label = QLabel(dialog_title)
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(*range_)
        if range_[0] == range_[1] == 0:
            self.progress_bar.setTextVisible(False)
        else:
            self.progress_bar.setValue(0)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)

        self.prompt_words = 'xxx'

    def set_value(self, value):
        self.progress_bar.setValue(value)

    def set_label_text(self, text):
        self.label.setText(text)

    def update_progress(self, val, text):
        self.set_value(val)
        self.set_label_text(self.prompt_words.replace('xxx', text))

    def set_window_title(self, title):
        self.setWindowTitle(title)

    def set_prompt_words(self, words):
        self.prompt_words = words
