from PySide6.QtCore import QThread, Signal
from .ui.custom_widget import *


class ProgressThread(QThread):
    """
    带进度条的线程
    """
    progress = Signal(int, str)

    def __init__(self, dialog_title='', range_: tuple = (0, 0)):
        super().__init__()
        self.run = None
        self.progress_dialog = CustomProgressDialog(dialog_title=dialog_title, range_=range_)

        # 绑定信号
        self.started.connect(self.progress_dialog.show)
        self.finished.connect(self.progress_dialog.close)
        self.progress.connect(self.progress_dialog.update_progress)

    def set_run(self, run):
        self.run = run


