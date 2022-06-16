import sys
from PySide2.QtGui import Qt
from PySide2.QtWidgets import QMessageBox


class NoZoweDlg(object):

    def __init__(self, detailed_error):
        self.detailed_text = detailed_error

    def show_error_msg_box(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)

        msg.setTextFormat(Qt.RichText)
        msg.setText("<p>Couldn't find zowe executable.</p>"
                    "Either you have no ZOWE CLI installed or<br>it's not in your PATH environment variable."
                    "<p>Please refer to:<br><a href='https://docs.zowe.org/stable/user-guide/cli-installcli.html'>"
                    "https://docs.zowe.org/stable/user-guide/cli-installcli.html</a></p>")

        msg.setWindowTitle("Error")
        msg.setDetailedText(self.detailed_text)
        msg.setStandardButtons(QMessageBox.Ok)
        sys.exit(msg.exec_())
