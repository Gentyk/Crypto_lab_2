from Crypto.Cipher import AES
import binascii
from Crypto.Util import Counter


key=b'YELLOW SUBMARINE'
s="Or6kII/NM5bDyWwvTGC3B6KFCPz9H2Cxvakxs/uGFmENxPykZx4XJqb62VPGj6rj7w=="
bins=binascii.a2b_base64(s)

#iv = b'00000000000000'
ctr = Counter.new(64, prefix=b'\x00'*8, initial_value=0, little_endian=True)
"""
nbits(Целое число) - Длина требуемого счетчика, в битах. Оно должно быть кратно 8.
prefix(Байт строка) - Константа префикс счетчика блока. По умолчанию не используется префикс.
#suffix(Байт строка) - Константа Постфиксное счетчика блока. По умолчанию, не используется суффикс.
initial_value(Целое число) - начальное значение счетчика. Значение по умолчанию равно 1.
little_endian(Логическое) - Если True, номер счетчика будет закодирован в маленьком формате с обратным
порядком байтов. Если False (по умолчанию), в большом формате с обратным порядком байтов.
"""

cipher = AES.new(key, AES.MODE_CTR,counter=ctr)
msg =cipher.decrypt(bins)
#print(msg)

sss=""
for j in msg:
    sss+=chr(j)
print(sss)
