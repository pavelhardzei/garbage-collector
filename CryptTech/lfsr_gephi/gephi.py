class Gephi:
    def __init__(self, lfsr_first, lfsr_second, lfsr_third, init_first, init_second, init_third):
        self.__polynomial_lfsr_first = self.__reverse_bits(lfsr_first)
        self.__polynomial_lfsr_second = self.__reverse_bits(lfsr_second)
        self.__polynomial_lfsr_third = self.__reverse_bits(lfsr_third)
        self.__init_first = init_first
        self.__init_second = init_second
        self.__init_third = init_third

    @staticmethod
    def __reverse_bits(num):
        result = 0
        while num:
            result = (result << 1) | (num & 1)
            num >>= 1
        return result

    def __generate_first_lfsr_galois(self):
        if self.__init_first & 0b1:
            self.__init_first = ((self.__init_first ^ self.__polynomial_lfsr_first) >> 1)\
                                | 0b10000000000000000000000
            return 0b1
        self.__init_first >>= 1
        return 0b0

    def __generate_second_lfsr_galois(self):
        if self.__init_second & 0b1:
            self.__init_second = ((self.__init_second ^ self.__polynomial_lfsr_second) >> 1)\
                                | 0b10000000000000000000000000000
            return 0b1
        self.__init_second >>= 1
        return 0b0

    def __generate_third_lfsr_galois(self):
        if self.__init_third & 0b1:
            self.__init_third = ((self.__init_third ^ self.__polynomial_lfsr_third) >> 1)\
                                | 0b1000000000000000000000000000000
            return 0b1
        self.__init_third >>= 1
        return 0b0

    def generate_next_gephi(self):
        bit1 = self.__generate_first_lfsr_galois()
        bit2 = self.__generate_second_lfsr_galois()
        bit3 = self.__generate_third_lfsr_galois()
        return (bit1 & bit2) ^ ((bit1 ^ 0b1) & bit3)

    def generate_gephi_sequence(self, count):
        result = 0
        for i in range(count):
            result = (result << 1) | self.generate_next_gephi()
        return result