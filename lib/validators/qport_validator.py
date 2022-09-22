import sys
import re
from PySide6.QtWidgets import QLineEdit, QApplication, QWidget, QFormLayout
from lib.validators.qcommon_validator import QCommonValidator


class QPortValidator(QCommonValidator):

    DEFAULT_BOTTOM = 1
    DEFAULT_TOP = 65535

    def __init__(self, parent=None, bottom=None, top=None):
        super(QPortValidator, self).__init__(parent)

        self.bottom = bottom
        if self.bottom is None:
            self.bottom = self.DEFAULT_BOTTOM

        self.top = top
        if self.top is None:
            self.top = self.DEFAULT_TOP

        if self.bottom == 0:
            self.regX_expression = re.compile('(0|[1-9][0-9]*)')

        else:
            self.regX_expression = re.compile('([1-9][0-9]*)')

    def get_bottom(self):
        return self.bottom

    def get_top(self):
        return self.top

    def validate(self, text_input, pos):
        matches = self.regX_expression.findall(text_input)
        if matches and len(matches[0]) == len(text_input):
            if len(text_input) == 0:
                return self.return_state(self.STATE_INTERMEDIATE, text_input, pos)

            else:
                num = int(text_input)
                if self.bottom <= num <= self.top:
                    return self.return_state(self.STATE_ACCEPTABLE, text_input, pos)

                else:
                    if self.edit.hasFocus():
                        return self.return_state(self.STATE_INTERMEDIATE, text_input, pos)

                    else:
                        return self.return_state(self.STATE_INVALID, text_input, pos)
        else:
            if len(text_input) == 0:
                return self.return_state(self.STATE_INTERMEDIATE, text_input, pos)
            else:
                return self.return_state(self.STATE_INVALID, text_input, pos)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = QWidget()

    lineEdit = QLineEdit()
    validator = QPortValidator(lineEdit)
    lineEdit.setValidator(validator)

    lineEdit1 = QLineEdit()

    flo = QFormLayout()
    flo.addRow("integer validator", lineEdit)
    flo.addRow("Double validator", lineEdit1)
    mainWindow.setLayout(flo)

    mainWindow.show()

    app.exec_()
    app.deleteLater()
    sys.exit()
