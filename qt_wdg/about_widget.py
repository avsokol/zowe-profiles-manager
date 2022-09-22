from PySide6.QtWidgets import QDialog
from qt_ui.about import UiDialog


class About(QDialog, UiDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setup_ui(self)
        self.show()
