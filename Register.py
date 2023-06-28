class Register:
    def __init__(self, length, name='', value=0):
        self.length = length
        self.name = name
        self.value = value
        self.binary = ''
        self.to_binary()
        # self.arr = list(map(lambda x: int(x), self.binary))

    def clear(self):
        self.value = 0
        self.to_binary()

    def set(self, n_value):
        self.value = n_value
        self.to_binary()

    def to_binary(self):
        binary = bin(self.value)
        if (self.value >= 0):
            binary = binary[2:]
            if (len(binary) < self.length):
                binary = (self.length - len(binary)) * '0' + binary
        else:
            binary = binary[3:]
            res = ''
            for i in range(len(binary)):
                if binary[i] == '0':
                    res += '1'
                else:
                    res += '0'
            if len(res) != self.length:
                res = '1' + res
            binary = res
            if len(binary) < self.length:
                binary = (self.length - len(binary)) * '1' + binary
        self.binary = binary

    def add(self, value_1):
        self.value = self.value + value_1
        self.to_binary()

    def p_transform(self, start, end, value):
        arr = list(map(lambda x: int(x), self.binary))
        j = 0
        for i in range(start, end + 1):
            arr[i] = int(value[j])
            j += 1
        self.binary = ''
        for i in arr:
            self.binary += str(i)
        self.value = int(self.binary, 2)  # needs to handle negative values


ar = Register(11, 'AR')
pc = Register(11, 'PC')
dr = Register(16, 'DR')
ac = Register(16, 'AC')
