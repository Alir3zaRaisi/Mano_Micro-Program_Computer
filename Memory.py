from Register import Register


class Memory:
    def __init__(self, length, bit):  # Creates A memory with registers of given length and bits for words length
        self.registers = []
        for i in range(length):
            self.registers.append(Register(bit, f'{i}'))
        self.table = {}
        self.memory_line = {}

    def read(self, index):  # returns the value of the indexed register
        return self.registers[index].binary

    def write(self, index, value):  # writes the value into the given register
        self.registers[index].set(value)

    def lookup(self, lines):  # fills the lookup table of the register with variables name and places
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

    def compile(self, lines, lc, table):
        flag = True
        for line in lines:
            if not flag:
                break
            if line[:3] == "ORG":
                line.replace(' ', '')
                lc = int(line[3:])
                lc = lc - 1
            elif line[:3] == "HLT":
                self.write(lc, 32767)  # HLT => 0 1111 1111111111
                self.memory_line[lc] = lines.index(line)
                break
            elif line[:3] == "DEC":
                value = line.replace(" ", '')
                self.write(lc, int(value[4:]))
            elif line[:3] == "HEX":
                value = line.replace(" ", '')
                self.write(lc, int(value[4:], 16))
            else:
                command = line.split('\t')
                if command[0] == 'I' or command[0] == 'i':
                    num = '1'
                    if table.get(command[1], 'Not Found') != 'Not Found':
                        addr = table[command[1]]
                        addr = format(int(int(addr) / 4), '04b').replace(' ', '0')
                        if self.table.get(command[2], 'Not Found') != 'Not Found':
                            num = num + addr + format(self.table[command[2]][0], '11b').replace(' ', '0')
                        elif command[2][:3] == "HEX":
                            num = num + addr + format(int(command[2][4:], 16), '11b').replace(' ', '0')
                            # self.basic_memory.write(lc, int(num, 2))
                        elif command[2][:3] == "BIN":
                            num = num + addr + format(int(command[2][4:], 2), '11b').replace(' ', '0')
                            # self.basic_memory.write(lc, int(num, 2))
                        elif command[2][:3] == "DEC":
                            num = num + addr + format(int(command[2][4:]), '11b').replace(' ', '0')
                    else:
                        return flag, lc
                else:
                    num = '0'
                    if table.get(command[0], 'Not Found') != 'Not Found':
                        addr = table[command[0]]
                        addr = format(int(int(addr) / 4), '04b').replace(' ', '0')
                        if self.table.get(command[1], 'Not Found') != 'Not Found':
                            num = num + addr + format(self.table[command[1]][0], '11b').replace(' ', '0')
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
                        return flag, lc
                self.write(lc, int(num, 2))
                self.memory_line[lc] = lines.index(line)

            lc += 1
        return True, lc
