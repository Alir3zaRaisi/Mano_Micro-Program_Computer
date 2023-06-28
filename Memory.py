from Register import Register


class Memory:
    def __init__(self, length, bit):
        self.registers = []
        for i in range(length):
            self.registers.append(Register(bit, f'{i}'))

    def read(self, index):
        return self.registers[index].binary

    def write(self, index, value):
        self.registers[index].set(value)


Basic_Memory = Memory(2048, 16)
