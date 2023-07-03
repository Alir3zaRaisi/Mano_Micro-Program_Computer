from Register import Register


class Memory:
    def __init__(self, length, bit):
        self.registers = []
        for i in range(length):
            self.registers.append(Register(bit, f'{i}'))
        self.table = {}

    def read(self, index):
        return self.registers[index].binary

    def write(self, index, value):
        self.registers[index].set(value)

    def lookup(self, lines):
        lc = 0
        num = ["HEX", "DEC", "BIN"]
        for line in lines:
            if line[:3] == "ORG":
                line.replace(' ', '')
                lc = int(line[3:])
                lc = lc - 1
            elif ':' in line:
                operand = line.split(':')
                if operand[1][1:4] == "HEX":
                    value = int(operand[1][5:], 16)
                elif operand[1][1:4] == "BIN":
                    value = int(operand[1][5:], 2)
                else:
                    value = int(operand[1][5:], 10)
                self.table[operand[0]] = [lc, value]
                self.write(lc, value)
            elif line[:3] in num:
                if line[:3] == "HEX":
                    value = int(line[4:], 16)
                elif line[:3] == "DEC":
                    value = int(line[4:])
                else:
                    value = int(line[4:], 2)
                self.write(lc, value)
            lc += 1


Basic_Memory = Memory(2048, 16)
