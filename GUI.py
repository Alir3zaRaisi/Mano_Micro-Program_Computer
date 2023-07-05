import time

from PyQt5 import QtWidgets
from PyQt5.QtCore import QAbstractTableModel, Qt, pyqtSignal, QObject, QCoreApplication, QTimer, QVariant
from PyQt5.QtGui import QTextCursor, QColor

from front import Ui_MainWindow


class MyEmitter(QObject):
    control_unit_compile = pyqtSignal(tuple)
    basic_memory_compile = pyqtSignal(tuple)
    update_registers = pyqtSignal(bool)


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

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(section)
            elif orientation == Qt.Vertical:
                return str(section)
        return QVariant()


class AppMainWindow(QtWidgets.QMainWindow):
    def __init__(self, control_unit, basic_memory, emitter):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.basicMemoryTable.horizontalHeader().setDefaultSectionSize(200)
        self.ui.conterol_unit_tabl.horizontalHeader().setDefaultSectionSize(200)
        self.c = control_unit
        self.emitter = emitter
        self.emitter.control_unit_compile.connect(self._show_pop_up_compile)
        self.emitter.update_registers.connect(self.show_registers)
        self.basic_memory = basic_memory
        self.ui.pc.setText('0')
        self.ui.clock_rate.setText('500')
        self.ui.compile.clicked.connect(self.get_control_unit)
        self.ui.BasicMemoryCompile.clicked.connect(self.get_memory)
        self.ui.Run.clicked.connect(self.set_pc)
        self.last_high_lighted = 0

    def _show_pop_up_compile(self, res):
        msg_box = QtWidgets.QMessageBox()

        msg_box_size = msg_box.sizeHint()
        x = (1212 - msg_box_size.width() - 80) // 2
        y = (952 - msg_box_size.height() - 20) // 2

        msg_box.move(x, y)

        msg_box.setWindowTitle("Compile")
        if res:
            msg_box.setText("Basic Memory Compiled Successfully")
        else:
            msg_box.setText(f"Compile Error in line{res[1]}")
        msg_box.exec_()

    def update(self):
        data = []
        for reg in self.basic_memory.registers:
            data.append(['{:016b}'.format(reg.value)])
        model = TableModel(data)

        self.ui.basicMemoryTable.setModel(model)

    def set_pc(self):
        data = self.ui.pc.text()
        self.c.pc.set(int(data))
        clock = self.ui.clock_rate.text()
        self.c.car.p_transform(1, 4, self.basic_memory.registers[int(data)].binary[1:5])
        self.c.dr.set(self.basic_memory.registers[int(data)].value)
        self.c.ar.set(int(self.c.dr.binary[6:], 2))
        self.c.INCPC()
        self.show_registers()
        QCoreApplication.processEvents()
        while self.c.dr.value != 32767:
            self.c.run(command=self.c.control_memory.registers[int(self.c.car.binary, 2)].binary,
                       basic_memory=self.basic_memory)
            self.emitter.update_registers.emit(True)
            QTimer.singleShot(int(clock), self.show_registers)
            time.sleep(int(clock) / 1000)
            QCoreApplication.processEvents()
        self.update()

    def show_registers(self):
        self.ui.show_CAR.setText(self.c.car.binary)
        self.ui.show_AC.setText(self.c.ac.binary)
        self.ui.show_AR.setText(self.c.ar.binary)
        self.ui.show_DR.setText(self.c.dr.binary)
        self.ui.show_SBR.setText(self.c.sbr.binary)
        self.ui.pc.setText(self.c.pc.binary)

        self.highlight(self.ui.control_unit_input, self.last_high_lighted, QColor(Qt.white))
        self.highlight(self.ui.control_unit_input, self.c.line[self.c.car.value], QColor(Qt.yellow))
        if self.c.dr.value != 32767:
            self.highlight(self.ui.Basic_Memory, self.basic_memory.memory_line[self.c.pc.value] - 2, QColor(Qt.white))
            self.highlight(self.ui.Basic_Memory, self.basic_memory.memory_line[self.c.pc.value] - 1, QColor(Qt.red))
        else:
            self.highlight(self.ui.Basic_Memory, self.basic_memory.memory_line[self.c.pc.value - 1] - 1,
                           QColor(Qt.white))
            self.highlight(self.ui.Basic_Memory, self.basic_memory.memory_line[self.c.pc.value - 1], QColor(Qt.red))

    def highlight(self, text_edit, line, color):

        if text_edit == self.ui.control_unit_input:
            self.last_high_lighted = line
        # Get the cursor of the text edit
        cursor = text_edit.textCursor()

        # Move the cursor to the start of the line we want to highlight
        cursor.movePosition(QTextCursor.Start)

        # Move the cursor to the desired line
        for _ in range(line):
            cursor.movePosition(QTextCursor.Down)

        # Get the current block format
        format = cursor.blockFormat()

        # Set the background color for the line
        format.setBackground(color)

        # Apply the modified block format
        cursor.setBlockFormat(format)

        # Set the new cursor and focus to the text edit
        text_edit.setTextCursor(cursor)
        text_edit.setFocus()

    def get_control_unit(self):
        text = self.ui.control_unit_input.toPlainText()
        lines = text.split('\n')
        res = self.c.compile(lines)
        if res[0]:
            self.emitter.control_unit_compile.emit(res)
            data = []
            for reg in self.c.control_memory.registers:
                data.append(['{:020b}'.format(reg.value)])
            model = TableModel(data)
            self.ui.conterol_unit_tabl.setModel(model)
        else:
            data = [f'Compile Error in line:{res[1]}']
            model = TableModel(data)
            self.ui.conterol_unit_tabl.setModel(model)

    def get_memory(self):
        text = self.ui.Basic_Memory.toPlainText()
        lines = text.split('\n')
        self.basic_memory.lookup(lines)

        res = self.basic_memory.compile(lines, 0, self.c.table)

        data = []
        if res[0]:
            for reg in self.basic_memory.registers:
                data.append(['{:016b}'.format(reg.value)])
        else:
            data = [f'Compile Error in line:{res[1]}']
        model = TableModel(data)
        self.ui.basicMemoryTable.setModel(model)

