from Control_Unit import Control_Unit
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal
from front import Ui_MainWindow


class AppMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    compile_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.c = Control_Unit()
        self.c.compile_signal.connect(self.compiled)

    def get_control_unit(self):
        text = self.control_unit_input.toPlainText()
        lines = text.split('\n')
        self.c.compile(lines)
        print(text)

    def compiled(self, data):
        QMessageBox.information(self, data, "This is an information message.")


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = AppMainWindow()
    MainWindow.show()

    sys.exit(app.exec_())
