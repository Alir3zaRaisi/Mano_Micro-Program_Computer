from PyQt5 import QtWidgets
from PyQt5.QtCore import QAbstractTableModel, Qt

from ControlUnit import ControlUnit
from Memory import Basic_Memory
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
    def __init__(self, control_unit, basic_memory):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.basicMemoryTable.horizontalHeader().setDefaultSectionSize(200)
        self.ui.conterol_unit_tabl.horizontalHeader().setDefaultSectionSize(200)
        self.c = control_unit
        self.basic_memory = basic_memory
        self.ui.compile.clicked.connect(self.get_control_unit)
        self.ui.BasicMemoryCompile.clicked.connect(self.get_memory)
        self.ui.Run.clicked.connect(self.set_pc)
        self.ui.update_memory.clicked.connect(self.update)

    def update(self):
        data = []
        for reg in self.basic_memory.registers:
            data.append(['{:016b}'.format(reg.value)])
        model = TableModel(data)

        self.ui.basicMemoryTable.setModel(model)

    def set_pc(self):
        data = self.ui.pc.text()
        self.c.pc.set(int(data))
        reg = self.basic_memory.registers[int(data)]
        self.c.car.p_transform(1, 4, reg.binary[1:5])
        self.c.dr.set(reg.value)
        # self.c.ar.set(int(data))
        self.c.ar.set(int(self.c.dr.binary[6:], 2))
        self.c.INCPC()
        while self.c.dr.value != 32767:
            self.ui.show_CAR.setText(self.c.car.binary)
            self.ui.show_AC.setText(self.c.ac.binary)
            self.ui.show_AR.setText(self.c.ar.binary)
            self.ui.show_DR.setText(self.c.dr.binary)
            self.ui.show_SBR.setText(self.c.sbr.binary)
            self.ui.pc.setText(self.c.pc.binary)
            # time.sleep(1)
            self.c.run(command=self.c.control_memory.registers[int(self.c.car.binary, 2)].binary)

    def get_control_unit(self):
        text = self.ui.control_unit_input.toPlainText()
        # self.ui.control_unit_input.appendPlainText("ALIREZA RAISI")
        lines = text.split('\n')
        res = self.c.compile(lines)
        if res[0]:
            data = []
            for reg in self.c.control_memory.registers:
                data.append(['{:020b}'.format(reg.value)])
            model = TableModel(data)
            self.ui.conterol_unit_tabl.setModel(model)
        else:
            data = [f'Compile Error in line:{res[1]}']
            model = TableModel(data)
            self.ui.conterol_unit_tabl.setModel(model)
        print(text)

    def get_memory(self):
        lc = 0
        text = self.ui.Basic_Memory.toPlainText()
        flag = True
        lines = text.split('\n')
        self.basic_memory.lookup(lines)
        for line in lines:
            if not flag:
                break
            if line[:3] == "ORG":
                line.replace(' ', '')
                lc = int(line[3:])
                lc = lc - 1
            elif line[:3] == "HLT":
                self.basic_memory.write(lc, 32767)  # HLT => 0 1111 1111111111
                break
            elif line[:3] == "DEC":
                value = line.replace(" ", '')
                Basic_Memory.write(lc, int(value[4:]))
            elif line[:3] == "HEX":
                value = line.replace(" ", '')
                Basic_Memory.write(lc, int(value[4:], 16))
            else:
                command = line.split('\t')
                if command[0] == 'I' or command[0] == 'i':
                    num = '1'
                    if self.c.table.get(command[1], 'Not Found') != 'Not Found':
                        addr = self.c.table[command[1]]
                        addr = format(int(addr), '04b').replace(' ', '0')
                        if self.basic_memory.table.get(command[2], 'Not Found') != 'Not Found':
                            num = num + addr + format(self.basic_memory.table[command[2]][0], '11b').replace(' ', '0')
                        elif command[2][:3] == "HEX":
                            num = num + addr + format(int(command[2][4:], 16), '11b').replace(' ', '0')
                            # self.basic_memory.write(lc, int(num, 2))
                        elif command[2][:3] == "BIN":
                            num = num + addr + format(int(command[2][4:], 2), '11b').replace(' ', '0')
                            # self.basic_memory.write(lc, int(num, 2))
                        elif command[2][:3] == "DEC":
                            num = num + addr + format(int(command[2][4:]), '11b').replace(' ', '0')
                    else:
                        flag = False
                else:
                    num = '0'
                    if self.c.table.get(command[0], 'Not Found') != 'Not Found':
                        addr = self.c.table[command[0]]
                        addr = format(int(addr), '04b').replace(' ', '0')
                        if self.basic_memory.table.get(command[1], 'Not Found') != 'Not Found':
                            num = num + addr + format(self.basic_memory.table[command[1]][0], '11b').replace(' ', '0')
                        elif command[1][:3] == "HEX":
                            num = num + addr + format(int(command[1][3:], 16), '11b').replace(' ', '0')
                            # self.basic_memory.write(lc, int(command[3], 16))
                        elif command[1][:3] == "BIN":
                            num = num + addr + format(int(command[1][3:], 2), '11b').replace(' ', '0')
                            # self.basic_memory.write(lc, int(command[3], 2))
                        elif command[1][:3] == "DEC":
                            num = num + addr + format(int(command[1][3:]), '11b').replace(' ', '0')
                        # self.basic_memory.write(lc, int(num, 2))
                    else:
                        flag = False
                self.basic_memory.write(lc, int(num, 2))
            lc += 1
        data = []
        print(flag)
        if flag:
            for reg in self.basic_memory.registers:
                data.append(['{:016b}'.format(reg.value)])
        else:
            data = [f'Compile Error in line:{lc}']
        model = TableModel(data)
        self.ui.basicMemoryTable.setModel(model)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = AppMainWindow(ControlUnit(), Basic_Memory)
    ui.show()
    sys.exit(app.exec_())
