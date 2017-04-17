class Mersenne():
    n=624
    w=32
    r=31
    m=397
    a=0x9908B0DF
    u=11
    s=7
    t=15
    l=18
    b=0x9D2C5680
    c=0xEFC60000

    def __init__(self,seed):
        self.index = 0
        self.MT = [0 for i in range(624)]
        self.seed=0
        self.MT[0] = seed
        for i in range(1, 624):
            self.MT[i] = 0xffffffff & (0x6c078965 * (self.MT[i - 1] ^ (self.MT[i - 1] >> 30)) + i)

    def generate_numbers(self):
        for i in range(624):
            y=(self.MT[i] & 0x80000000) + (self.MT[(i + 1) % 624] & 0x7fffffff)#^0xFFFFFFFF
            self.MT[i] = self.MT[(i + 397) % 624] ^ (y>>1)
            if (y % 2) != 0:
                self.MT[i]= self.MT[i]^2567483615 # 0x9908b0df=a

    def  extract_number(self):
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

"""rand = Mersenne(100)
for i in range(100):
     print(rand.extract_number())"""








