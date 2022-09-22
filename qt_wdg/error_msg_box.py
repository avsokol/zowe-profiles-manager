from PySide6.QtWidgets import QMessageBox


class ErrMsgBox(object):

    def __init__(self, msg_text, detailed_error):
        self.text = msg_text
        self.detailed_text = detailed_error

    def show_error_msg_box(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(self.text)
        msg.setWindowTitle("Error")
        msg.setDetailedText(self.detailed_text)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
