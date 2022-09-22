import sys
import re
from PySide6.QtWidgets import QApplication, QWidget, QLineEdit, QFormLayout
from lib.validators.qcommon_validator import QCommonValidator


class QProfileNameValidator(QCommonValidator):

    def __init__(self, parent=None):
        super(QProfileNameValidator, self).__init__(parent)

        self.regX_expression = re.compile('^[0-9]+$')

    def validate(self, text_input, pos):
        matches = self.regX_expression.findall(text_input)
        if matches and len(matches[0]) == len(text_input):
            if len(text_input) == 0:
                return self.return_state(self.STATE_INTERMEDIATE, text_input, pos)

            else:
                if self.edit.hasFocus():
                    return self.return_state(self.STATE_INTERMEDIATE, text_input, pos)

                else:
                    return self.return_state(self.STATE_INVALID, text_input, pos)

        else:
            if len(text_input) == 0:
                return self.return_state(self.STATE_INTERMEDIATE, text_input, pos)

            else:
                return self.return_state(self.STATE_ACCEPTABLE, text_input, pos)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = QWidget()

    lineEdit = QLineEdit()
    validator = QProfileNameValidator(lineEdit)
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
