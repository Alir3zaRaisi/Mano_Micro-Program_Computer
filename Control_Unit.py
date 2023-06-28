from Memory import *
from Register import *
from PyQt5.QtCore import pyqtSignal, QObject


class Control_Unit(QObject):
    compile_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.control_memory = Memory(128, 20)
        self.car = Register(7, 'CAR')
        self.sbr = Register(7, 'SBR')

        self.compile_signal = pyqtSignal(str)

        self.clock = 0

        self.AC = ["ADD", "CLRAC", "INCAC", "DRTAC", "SUB", "OR", "AND", "XOR", "COM", "SHL", "SHR"]

        self.f1 = ['NOP', '000', 'ADD', '001', 'CLRAC', '010', 'INCAC', '011', 'DRTAC', '100', 'DRTAR', '101',
                   'PCTAR', '110', 'WRITE', '111']

        self.f2 = ['NOP', '000', 'SUB', '001', 'OR', '010', 'AND', '011', 'READ', '100', 'ACTDR', '101',
                   'INCDR', '110', 'PCTDR', '111']

        self.f3 = ['NOP', '000', 'XOR', '001', 'COM', '010', 'SHL', '011', 'SHR', '100', 'INCPC', '101',
                   'ARTPC', '110']

        self.cd = {'U': '00', 'I': '01', 'S': '10', 'Z': '11'}

        self.br = {'JMP': '00', 'CALL': '01', 'RET': '01', 'MAP': '11'}

        self.table = {}

    def ADD(self):
        ac.add(dr.value)

    def CLRAC(self):
        ac.clear()

    def INCAC(self):
        ac.add(1)

    def DRTAC(self):
        ac.set(dr.value)

    def DRTAR(self):
        ar.p_transform(0, 10, dr.binary[5:16])

    def PCTAR(self):
        ar.set(pc.value)

    def WRITE(self):
        Basic_Memory.write(ar.value, dr.value)

    def SUB(self):
        ac.add(-(dr.value))

    def OR(self):
        pass

    def AND(self):
        pass

    def READ(self):
        dr.set(Basic_Memory.read(ar.value))

    def ACTDR(self):
        dr.set(ar.value)

    def INCDR(self):
        dr.add(1)

    def PCTDR(self):
        dr.p_transform(0, 10, pc.value)

    def XOR(self):
        pass

    def COM(self):
        pass

    def SHL(self):
        pass

    def SHR(self):
        pass

    def INCPC(self):
        pc.add(1)

    def ARTPC(self):
        pc.set(ar.value)

    def check(self):
        pass

    def compile(self, lines):
        lc = 0
        flag = True
        if flag:
            for line in lines:
                micros = line.split('\t')
                if micros[0][0:3] == 'ORG':
                    micros[0].replace(' ', '')
                    lc = int(micros[0][3:])
                    lc -= 1
                    print(lc)
                elif micros[0] == '':
                    if micros[1][:3] != 'NOP' and flag:
                        ops = micros[1].split(',')
                        if len(ops) == 1:
                            flag = False
                        elif len(ops) == 2:
                            if (ops[0] in self.f1 and ops[1] in self.f1) or (
                                    ops[0] in self.f2 and ops[1] in self.f2) or (
                                    ops[0] in self.f3 and ops[1] in self.f3):
                                print(f'Complie Eror in Line:{lc}')
                                flag = False
                            if (ops[0] in self.AC and ops[2] in self.AC):
                                print(f'Complie Eror in Line:{lc}')
                                flag = False
                        elif len(ops) == 3:
                            if ops[0] in self.f1:
                                if ops[1] in self.f1 or ops[2] in self.f1:
                                    print(f'Complie Eror in Line:{lc}')
                                    flag = False
                            if ops[0] in self.f2:
                                if ops[1] in self.f2 or ops[2] in self.f2:
                                    print(f'Complie Eror in Line:{lc}')
                                    flag = False
                            if ops[0] in self.f1:
                                if ops[1] in self.f3 or ops[2] in self.f3:
                                    print(f'Complie Eror in Line:{lc}')
                                    flag = False
                elif micros[0][-1] == ':':
                    self.table['FETCH'] = "ali"
                    flag = True
                    if micros[1][:3] != 'NOP' and flag:
                        ops = micros[1].split(',')
                        if len(ops) == 1:
                            flag = False
                        elif len(ops) == 2:
                            if (ops[0] in self.f1 and ops[1] in self.f1) or (
                            self.ops[0 in f2 and ops[1] in self.f2]) or (
                                    ops[0] in self.f3 and ops[1] in self.f3):
                                print(f'Complie Eror in Line:{lc}')
                                flag = False
                            if (ops[0] in self.Ac and ops[2] in self.AC):
                                print(f'Complie Eror in Line:{lc}')
                                flag = False
                        elif len(ops) == 3:
                            if ops[0] in self.f1:
                                if ops[1] in self.f1 or ops[2] in self.f1:
                                    print(f'Complie Eror in Line:{lc}')
                                    flag = False
                            if ops[0] in self.f2:
                                if ops[1] in self.f2 or ops[2] in self.f2:
                                    print(f'Complie Eror in Line:{lc}')
                                    flag = False
                            if ops[0] in self.f1:
                                if ops[1] in self.f3 or ops[2] in self.f3:
                                    print(f'Complie Eror in Line:{lc}')
                                    flag = False
                lc += 1
            if flag:
                self.compile_signal.emit("Success")
            else:
                self.compile_signal.emit("Fail")
# control = Control_Unit
# print(ar.value)
# dr.set(56)
#
# control.DRTAR(control)
# print(ar.value)
