from PyQt5 import QtWidgets

from ControlUnit import ControlUnit
from GUI import MyEmitter, AppMainWindow
from Memory import Memory

if __name__ == "__main__":
    import sys

    my_emitter = MyEmitter()

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = AppMainWindow(ControlUnit(), Memory(2048, 16), my_emitter)
    ui.setWindowTitle("Mano Micro-Program Computer")
    ui.show()
    sys.exit(app.exec_())
