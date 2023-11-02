from PySide6.QtCore import QThread, Signal

from ..View import CustomProgressDialog


class ProgressThread(QThread):
    progress = Signal(int, str)

    def __init__(self, dialog_title='', range_: tuple = (0, 0)):
        """
        带进度条的线程
        """
        super().__init__()
        self.run = None
        self.progress_dialog = CustomProgressDialog(dialog_title=dialog_title, range_=range_)

        # 绑定信号
        self.started.connect(self.progress_dialog.show)
        self.finished.connect(self.progress_dialog.close)
        self.progress.connect(self.progress_dialog.update_progress)

    def set_run(self, run):
        """
        设置任务函数

        Args:
            run: 要运行的函数

        Returns:

        """
        self.run = run
