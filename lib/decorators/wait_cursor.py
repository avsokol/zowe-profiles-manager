from PySide6.QtGui import QCursor, Qt
from PySide6.QtWidgets import QApplication


class WaitCursor(object):

    def __init__(self):
        pass

    def __call__(self, target_func):
        def func_wrapper(*args, **kwargs):
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

            QApplication.processEvents()
            QApplication.processEvents()

            target_func(*args, **kwargs)

            QApplication.restoreOverrideCursor()
            QApplication.processEvents()
            QApplication.processEvents()

        return func_wrapper
