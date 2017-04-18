from random import randint

class MT19937():
    def __init__(self,seed):
        if type(seed) == int:
            self.index = 0
            self.MT = [0 for i in range(624)]
            self.seed = 0
            self.MT[0] = seed
            for i in range(1, 624):
                self.MT[i] = 0xffffffff & (0x6c078965 * (self.MT[i - 1] ^ (self.MT[i - 1] >> 30)) + i)

        elif type(seed) == list and len(seed) == 624:
            self.index = 0
            self.MT = seed[:]

    def extract_number(self):
        if self.index == 0:
            self.generate_numbers()
        y=self.MT[self.index]
        # закалка
        y = y ^ (y >> 11);
        y = y ^ ((y << 7) & 0x9d2c5680);
        y = y ^ ((y << 15) & 0xefc60000);
        y = y ^ (y >> 18);
        self.index = (self.index + 1)%624
        return y

    def generate_numbers(self):
        for i in range(624):
            y=(self.MT[i] & 0x80000000) + (self.MT[(i + 1) % 624] & 0x7fffffff)#^0xFFFFFFFF
            self.MT[i] = self.MT[(i + 397) % 624] ^ (y>>1)
            if (y % 2) != 0:
                self.MT[i]= self.MT[i]^2567483615 # 0x9908b0df=a

    #новые
    @staticmethod
    def untemper(value):
        assert(value < 2**32)
        assert(value >= 0)

        y = value
        # Inverse  y = y ^ (y >> 18)
        y = y ^ (y >> 18)
        # Inverse  y = y ^ ((y << 15) & 0xefc60000)
        y = y ^ ((y & 0x1df8c) << 15)
        # Inverse  y = y ^ ((y << 7) & 0x9d2c5680)
        t = y
        t = ((t & 0x0000002d) << 7) ^ y
        t = ((t & 0x000018ad) << 7) ^ y
        t = ((t & 0x001a58ad) << 7) ^ y
        y = ((t & 0x013a58ad) << 7) ^ y

        # Inverse  y = y ^ (y >> 11)
        top = y & 0xffe00000
        mid = y & 0x001ffc00
        low = y & 0x000003ff

        y = top | ((top >> 11) ^ mid) | ((((top >> 11) ^ mid) >> 11) ^ low)

        return y

    @staticmethod
    def generate_clone(values):
        if type(values) != list:
            raise Exception
        if len(values) < 624:
            raise Exception
        values = values[:624]
        ret = MT19937([MT19937.untemper(v) for v in values])
        return ret





m = MT19937(randint(0, 2 ** 32 - 1))
values = [m.extract_number() for __ in range(624)]
n = MT19937.generate_clone(values)
mr = m.extract_number()
nr = n.extract_number()
if mr != nr:
     print("fail("+str(mr)+"!="+str(nr)+")")
else:
     print("good("+str(mr)+"=="+str(nr)+")")

"""Как я уже отмечал выше, если атакующий имеет 624 числа
сгенерированных с помощью Вихря Мерсенна этого достаточно
для того чтобы восстановить все внутреннее состояние и предугадывать
с вероятностью 100% все генерируемые в последующем числа.
"""
