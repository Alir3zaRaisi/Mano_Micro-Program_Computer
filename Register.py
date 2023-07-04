class Register:
    def __init__(self, length, name='', value=0):
        self.length = length
        self.name = name
        self.value = value
        self.binary = ''
        self.to_binary()

    def clear(self):
        self.value = 0
        self.to_binary()

    def set(self, n_value):
        self.value = n_value
        self.to_binary()

    def to_binary(self):
        binary = format(self.value, f'0{self.length}b').replace(' ', '0')
        if self.value < 0:
            binary = binary[1:]
            binary = binary.replace('1', '*')
            binary = binary.replace('0', '1')
            binary = binary.replace('*', '0')
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
