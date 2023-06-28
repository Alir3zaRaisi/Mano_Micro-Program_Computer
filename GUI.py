from PyQt5 import QtWidgets
from PyQt5.QtCore import QAbstractTableModel, Qt

from ControlUnit import ControlUnit
from front import Ui_MainWindow


class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self.data = data

    def rowCount(self, parent=None) -> int:
        return len(self.data)

    def columnCount(self, parent=None):
        return 1

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return str(self.data[index.row()][index.column()])

        return None


class AppMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.c = ControlUnit()
        self.ui.compile.clicked.connect(self.get_control_unit)
        self.ui.conterol_unit_tabl.horizontalHeader().resize(0, 1000)

    def get_control_unit(self):
        text = self.ui.control_unit_input.toPlainText()
        # self.ui.control_unit_input.appendPlainText("ALIREZARAISI")
        lines = text.split('\n')
        if self.c.compile(lines):
            data = []
            for reg in self.c.control_memory.registers:
                data.append([bin(reg.value)[2:]])
            model = TableModel(data)
            self.ui.conterol_unit_tabl.setModel(model)
        else:
            pass
        print(text)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = AppMainWindow()
    ui.show()
    sys.exit(app.exec_())
