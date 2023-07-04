from PyQt5.QtCore import QObject, pyqtSignal

from Memory import *
from Register import Register


class ControlUnit(QObject):

    def __init__(self):
        super().__init__()
        self.control_memory = Memory(128, 20)
        self.car = Register(7, 'CAR')
        self.sbr = Register(7, 'SBR')

        self.ar = Register(11, 'AR')
        self.pc = Register(11, 'PC')
        self.dr = Register(16, 'DR')
        self.ac = Register(16, 'AC')

        self.clock = 0

        self.AC = ["ADD", "CLRAC", "INCAC", "DRTAC", "SUB", "OR", "AND", "XOR", "COM", "SHL", "SHR"]

        self.f1 = ['NOP', '000', 'ADD', '001', 'CLRAC', '010', 'INCAC', '011', 'DRTAC', '100', 'DRTAR', '101',
                   'PCTAR', '110', 'WRITE', '111']

        self.f2 = ['NOP', '000', 'SUB', '001', 'OR', '010', 'AND', '011', 'READ', '100', 'ACTDR', '101',
                   'INCDR', '110', 'PCTDR', '111']

        self.f3 = ['NOP', '000', 'XOR', '001', 'COM', '010', 'SHL', '011', 'SHR', '100', 'INCPC', '101',
                   'ARTPC', '110']

        self.cd = {'U': '00', 'I': '01', 'S': '10', 'Z': '11'}

        self.br = {'JMP': '00', 'CALL': '01', 'RET': '10', 'MAP': '11'}

        self.table = {}  # shows that where is each function

    def run(self, command, basic_memory):
        if command[:3] == '001':
            self.add()
        elif command[:3] == '010':
            self.clrac()
        elif command[:3] == '011':
            self.inc_ac()
        elif command[:3] == '100':
            self.dr_to_ac()
        elif command[:3] == '101':
            self.dr_to_ar()
        elif command[:3] == '110':
            self.pc_to_ar()
        elif command[:3] == '111':
            self.write(basic_memory)
        if command[3:6] == '001':
            self.sub()
        elif command[3:6] == '010':
            self.OR()
        elif command[3:6] == '011':
            self.AND()
        elif command[3:6] == '100':
            self.READ(basic_memory)
        elif command[3:6] == '101':
            self.ACTDR()
        elif command[3:6] == '110':
            self.INCDR()
        elif command[3:6] == '111':
            self.PCTDR()
        if command[6:9] == '001':
            self.XOR()
        elif command[6:9] == '010':
            self.COM()
        elif command[6:9] == '011':
            self.SHL()
        elif command[6:9] == '100':
            self.SHR()
        elif command[6:9] == '101':
            self.INCPC()
        elif command[6:9] == '110':
            self.ARTPC()

        if command[9:11] == '00':  # condition = U
            if command[11:13] == '00':  # JMP
                self.car.set(int(command[13:], 2))
            elif command[11:13] == '01':  # CALL
                self.sbr.set(self.car.value + 1)
                self.car.set(int(command[13:], 2))
            elif command[11:13] == '10':  # RET
                self.car.set(self.sbr.value)
            elif command[11:13] == '11':  # MAP
                self.car.clear()
                self.car.p_transform(1, 4, self.dr.binary[1:5])
        elif command[9:11] == '01':  # condition = I
            if self.dr.binary[0] == '1':
                if command[11:13] == '00':  # JMP
                    self.car.set(int(command[13:], 2))
                elif command[11:13] == '01':  # CALL
                    self.sbr.set(self.car.value + 1)
                    self.car.set(int(command[13:], 2))
                elif command[11:13] == '10':  # RET
                    self.car.set(self.sbr.value)
                elif command[11:13] == '11':  # MAP
                    self.car.clear()
                    self.car.p_transform(1, 4, self.dr.binary[1:5])
            else:
                self.car.set(self.car.value + 1)
        elif command[9:11] == '10':  # condition = S
            if self.ac.binary[0] == '1':
                if command[11:13] == '00':  # JMP
                    self.car.set(int(command[13:], 2))
                elif command[11:13] == '01':  # CALL
                    self.sbr.set(self.car.value + 1)
                    self.car.set(int(command[13:], 2))
                elif command[11:13] == '10':  # RET
                    self.car.set(self.sbr.value)
                elif command[11:13] == '11':  # MAP
                    self.car.clear()
                    self.car.p_transform(1, 4, self.dr.binary[1:5])
            else:
                self.car.set(self.car.value + 1)

        elif command[9:11] == '11':  # condition = Z
            if self.ac.value == 0:
                if command[11:13] == '00':  # JMP
                    self.car.set(int(command[13:], 2))
                elif command[11:13] == '01':  # CALL
                    self.sbr.set(self.car.value + 1)
                    self.car.set(int(command[13:], 2))
                elif command[11:13] == '10':  # RET
                    self.car.set(self.sbr.value)
                elif command[11:13] == '11':  # MAP
                    self.car.clear()
                    self.car.p_transform(1, 4, self.dr.binary[1:5])
            else:
                self.car.set(self.car.value + 1)

    def add(self):
        self.ac.add(self.dr.value)

    def clrac(self):
        self.ac.clear()

    def inc_ac(self):
        self.ac.add(1)

    def dr_to_ac(self):
        self.ac.set(self.dr.value)

    def dr_to_ar(self):
        self.ar.p_transform(0, 10, self.dr.binary[5:16])

    def pc_to_ar(self):
        self.ar.set(self.pc.value)

    def write(self, basic_memory):
        basic_memory.write(self.ar.value, self.dr.value)

    def sub(self):
        self.ac.add(-self.dr.value)

    def OR(self):
        res = ''
        for i in range(len(self.ac.binary)):
            if self.ac.binary[i] == '1' or self.dr.binary[i] == '1':
                res = res + '1'
            else:
                res = res + '0'
        self.ac.set(int(res, 2))

    def AND(self):
        res = ''
        for i in range(len(self.ac.binary)):
            if self.ac.binary[i] == '1' and self.dr.binary[i] == '1':
                res = res + '1'
            else:
                res = res + '0'
        self.ac.set(int(res, 2))

    def READ(self, basic_memory):
        self.dr.set(int(basic_memory.read(self.ar.value), 2))

    def ACTDR(self):
        self.dr.set(self.ac.value)

    def INCDR(self):
        self.dr.add(1)

    def PCTDR(self):
        self.dr.p_transform(0, 10, self.pc.value)

    def XOR(self):
        res = ''
        for i in range(len(self.ac.binary)):
            if self.ac.binary[i] != self.dr.binary[i]:
                res = res + '1'
            else:
                res = res + '0'
        self.ac.set(int(res, 2))

        pass

    def COM(self):
        res = self.ac.binary
        res = res.replace('0', '*')
        res = res.replace('1', '0')
        res = res.replace('*', '1')
        self.ac.set(int(res, 2))

    def SHL(self):
        pass

    def SHR(self):
        pass

    def INCPC(self):
        self.pc.add(1)

    def ARTPC(self):
        self.pc.set(self.ar.value)

    def compile(self, lines):  # compiles the control unit memory
        lc = 0
        flag = True
        self.check(lines)
        if flag:
            for line in lines:
                micros = line.split('\t')
                num = ''
                if micros[0][0:3] == 'ORG':
                    micros[0].replace(' ', '')
                    lc = int(micros[0][3:])
                    lc -= 1
                    print(lc)
                elif micros[0] == '':
                    flag = self.error(micros, lc)
                elif micros[0][-1] == ':':
                    self.table[micros[0][:-1]] = f'{lc}'
                    flag = self.error(micros, lc)
                if micros[0][0:3] != 'ORG':
                    num = self.translate(micros, lc)
                    self.control_memory.write(lc, int(num, 2))
                lc += 1
            if flag:
                # self.compile_signal.emit("Success")
                return True, lc
            else:
                # self.compile_signal.emit("Fail")
                return False, lc

    def check(self, lines):  # fills the table
        lc = 0
        for line in lines:
            if line[:3] == "ORG":
                line.replace(' ', '')
                lc = int(line[3:])
                lc = lc - 1
            elif ':' in line:
                a = line.split(':')
                self.table[a[0]] = lc

            lc += 1

    def translate(self, micros, lc):  # translate the code into binary values
        ops = micros[1].split(',')
        if len(ops) == 1:
            if ops[0] in self.f1:
                num = self.f1[self.f1.index(ops[0]) + 1]
                num = num + '000000'
                pass
            elif ops[0] in self.f2:
                num = self.f2[self.f2.index(ops[0]) + 1]
                num = '000' + num + '000'
            else:
                num = '000000' + self.f3[self.f3.index(ops[0]) + 1]

        elif len(ops) == 2:
            if ops[0] in self.f1 or ops[1] in self.f1:
                if ops[0] in self.f1:
                    num = self.f1[self.f1.index(ops[0]) + 1]
                    if ops[1] in self.f2:
                        num = num + self.f2[self.f2.index(ops[1]) + 1] + '000'
                    else:
                        num = num + '000' + self.f3[self.f3.index(ops[1]) + 1]
                else:
                    num = self.f1[self.f1.index(ops[1]) + 1]
                    if ops[0] in self.f2:
                        num = num + self.f2[self.f2.index(ops[0]) + 1] + '000'
                    else:
                        num = num + '000' + self.f3[self.f3.index(ops[0]) + 1]
            elif ops[0] in self.f2:
                num = '000' + self.f2[self.f2.index(ops[0]) + 1] + self.f3[self.f3.index(ops[1]) + 1]
            else:
                num = '000' + self.f2[self.f2.index(ops[1]) + 1] + self.f3[self.f3.index(ops[0]) + 1]
        else:
            if ops[0] in self.f1:
                num = self.f1[self.f1.index(ops[0]) + 1]
                if ops[1] in self.f2:
                    num = num + self.f2[self.f2.index(ops[1]) + 1] + self.f3[self.f3.index(ops[2]) + 1]
                else:
                    num = num + self.f2[self.f2.index(ops[2]) + 1] + self.f3[self.f3.index(ops[1]) + 1]
            elif ops[1] in self.f1:
                num = self.f1[self.f1.index(ops[1]) + 1]
                if ops[0] in self.f2:
                    num = num + self.f2[self.f2.index(ops[0]) + 1] + self.f3[self.f3.index(ops[1]) + 1]
                else:
                    num = num + self.f2[self.f2.index(ops[2]) + 1] + self.f3[self.f3.index(ops[0]) + 1]
            else:
                num = self.f1[self.f1.index(ops[2]) + 1]
                if ops[0] in self.f2:
                    num = num + self.f2[self.f2.index(ops[0]) + 1] + self.f3[self.f3.index(ops[1]) + 1]
                else:
                    num = num + self.f2[self.f2.index(ops[1]) + 1] + self.f3[self.f3.index(ops[0]) + 1]

        num = num + self.cd[micros[2]]
        num = num + self.br[micros[3]]
        if micros[3] == 'MAP':
            num = num + '0000000'
        elif micros[3] == "RET":
            num = num + '0000000'
        elif micros[4] == "NEXT":
            addr = format(lc + 1, '07b').replace(' ', '0')
            num = num + addr
        else:
            addr = format(self.table[micros[4]], '07b').replace(' ', '0')
            num = num + addr

        return num

    def error(self, micros, lc):  # checks that the RTL is right
        flag = True
        if micros[1][:3] != 'NOP':
            ops = micros[1].split(',')
            # self.control_memory.write(lc)
            if len(ops) == 2:
                if (ops[0] in self.f1 and ops[1] in self.f1) or (
                        ops[0] in self.f2 and ops[1] in self.f2) or (
                        ops[0] in self.f3 and ops[1] in self.f3):
                    print(f'Compile Error in Line:{lc}')
                    flag = False
                if ops[0] in self.AC and ops[2] in self.AC:
                    print(f'Compile Error in Line:{lc}')
                    flag = False

            elif len(ops) == 3:
                if ops[0] in self.f1:
                    if ops[1] in self.f1 or ops[2] in self.f1:
                        print(f'Compile Error in Line:{lc}')
                        flag = False
                if ops[0] in self.f2:
                    if ops[1] in self.f2 or ops[2] in self.f2:
                        print(f'Compile Error in Line:{lc}')
                        flag = False
                if ops[0] in self.f1:
                    if ops[1] in self.f3 or ops[2] in self.f3:
                        print(f'Compile Error in Line:{lc}')
                        flag = False
        return flag
