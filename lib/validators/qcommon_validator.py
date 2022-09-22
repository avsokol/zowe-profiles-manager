from PySide6.QtGui import QValidator


class QCommonValidator(QValidator):

    STATE_ACCEPTABLE = "acceptable"
    STATE_INTERMEDIATE = "intermediate"
    STATE_INVALID = "invalid"

    COLOR_OK = "#00cc00"
    COLOR_WARN = "#fff79a"
    COLOR_ERR = "#f6989d"

    def __init__(self, parent=None):
        super(QCommonValidator, self).__init__(parent)

        self.edit = parent
        self.states = {
            self.STATE_INVALID: QValidator.Invalid,
            self.STATE_INTERMEDIATE: QValidator.Intermediate,
            self.STATE_ACCEPTABLE: QValidator.Acceptable,
        }

    def return_state(self, state, text, pos):
        if state == self.STATE_ACCEPTABLE:
            color = None
            # color = self.COLOR_OK

        elif state == self.STATE_INTERMEDIATE:
            color = self.COLOR_WARN

        else:
            color = self.COLOR_ERR

        if color is None:
            self.parent().setStyleSheet("QLineEdit {}")

        else:
            self.parent().setStyleSheet("QLineEdit {{ background-color: {0} }}".format(color))

        return self.states[state]
