import random
from Crypto.Cipher import AES
from Crypto import Random
import binascii

"""Вспомогательные функции(их 3)"""
#старая функция проверка допонения - необходима будет только для красивого вывода результата
#выход:
#если верно, то удаляет дополнение:ICE ICE BABY\x04\x04\x04\x04->ICE ICE BABY
#вход: строкаа в бинарном представлении
def old_inspection(bins):
    n=len(bins)
    j=bins[len(bins)-1]
    if (j>=n):
        return bins.decode("UTF-8")
    i=0
    while (i<j-1):
        if (bins[len(bins) - 2-i] != bins[len(bins)-1]):
            print("error")
            return 1
        i+=1
    return bins[0:len(bins)-j].decode("UTF-8")

#функция дополнения строки до необходимой длины 16
#например: YELLOW SUBMARINE -> YELLOW SUBMARINE\x04\x04\x04\x04
#вход: обычная строка
#выход: щбычная строка
def padding(s):
    k=16-len(s)%16 #сколько не хватает символов до кратности 16
    binstr=s.encode('UTF-8') #перевод в бинарное представление
    i=0
    while(i<k):
        binstr+=bytes([k])
        i+=1
    return binstr

#проверка допонения
#выход:
#если верно, то удаляет дополнение:ICE ICE BABY\x04\x04\x04\x04->ICE ICE BABY
#иначе: код ошибки "1"
#вход: код правильного выполнения "0"
def inspection(bins):
    n=len(bins)
    j=bins[len(bins)-1]
    if (j>=n):
        return 1
    i=0
    while (i<j-1):
        if (bins[len(bins) - 2-i] != bins[len(bins)-1]):
            return 1
        i+=1
    return 0


"""основные функции"""
#объявляем глобальный ключ
key=0

#функция выбора рандомной строки и шифрования их
#вход: ничего
#выход:зашифрованная строка
def random_string(i):
    string=[
        "V2l0aCB5b3VyIGZlZXQgaW4gdGhlIGFpciBhbmQgeW91ciBoZWFkIG9uIHRoZSBncm91bmQK",
        "VHJ5IHRoaXMgdHJpY2sgYW5kIHNwaW4gaXQhIFllYWhoIQo=",
        "WW91ciBoZWFkIHdpbGwgY29sbGFwc2UsIGJ1dCB0aGVyZSdzIG5vdGhpbmcgaW4gaXQK",
        "QW5kIHlvdSdsbCBhc2sgeW91cnNlbGY/Cg==",
        "V2hlcmUgaXMgbXkgbWluZD8K",
        "V2F5IG91dCwgaW4gdGhlIHdhdGVyIHNlZSBpdCBzd2ltbWluJyAK",
        "SSB3YXMgc3dpbW1pbicgaW4gdGhlIENhcnJpYmVhbgo=",
        "QW5pbWFscyB3b3VsZCBoaWRlIGJlaGluZCB0aGUgcm9ja3MuIFllYWhoIQo=",
        "RXhjZXB0IHRoZSBsaXR0bGUgZmlzaAo=",
        "QnV0IGhlIHRvbGQgbWUgZWFzdCB3YXMgd2VzdAo=",
        "VHJ5aW4nIHRvIHRhbGsgCg=="
    ]
    #s=string[random.randint(0,10)] #выбираем рандомно одну из 11 строк
    s=string[i]
    bins=binascii.a2b_base64(s)
    s=""
    for g in bins:
        s+=chr(g)
    print(s)
    global key
    key=Random.new().read(16) #задаем глобальный ключик))
    binstr=padding(s)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    msg = iv + cipher.encrypt(binstr)
    return msg

#функция проверки дополнения(она у нас есть: мы её можем использовать, но типа внутренность неизвестна)
#вход:шифр
#выход: true,если правильное дополнение
#false,если неправильное
def control_cookie(msg):
    global key
    cipher = AES.new(key, AES.MODE_CBC,msg[:16])
    binstr=cipher.decrypt(msg)
    if inspection(binstr):
        return False
    else:
        return True

#функция расшифровки 16 байтного блока с2 при использовании предыдущего блока с1
def padding_attac_to_block(c2,c1):
    s = bytearray(b'')  # готовая строка
    I = bytearray(b'')  # хранилище промежуточных значений
    # 16-й байт
    i = -1
    r = bytearray(b'1234567890123450')  # подстановочнная строка
    a = []  # массив, подходящих на позицию 16го байта символов
    while i < 255:
        i += 1
        r[15] = i
        msg1 = bytes(r) + c2
        if control_cookie(msg1) == True:
            a.append(i) #получили "?"
    for tt in a:  # выбор из списка нужного
        tt = tt ^ 1 ^ 2 #превращаем в =?^01^02=х^02
        i = -1
        r = bytearray(b'123456789012340')
        r.append(tt)
        while i < 255:
            i += 1
            r[14] = i
            msg1 = bytes(r) + c2
            if control_cookie(msg1) == True:
                s.append(tt ^ 2 ^ c1[15]) # tt^02=x -> s[15]=x^c[15]-последний элемент результирующей строки
                I.append(tt ^ 2) #tt=?^01^02=х^02 -> x=tt^02
    #анализируем с 15 байта по 0
    j = 2
    while j < 17:
        r = bytearray(b'')
        for g in range(0, 16 - j):
            r.append(1)
        r.append(0)
        I = I[::-1]
        for g in I:#перевернутое I добавляем в C'1=r
            r.append(g ^ j)
        I = I[::-1]
        i = -1
        a = []
        while i < 255:
            i += 1
            r[16 - j] = i
            msg1 = bytes(r) + c2
            if control_cookie(msg1) == True:
                a.append(i) # =?
        s.append(a[0] ^ j ^ c1[16 - j])
        I.append(a[0] ^ j) #=y=?^j
        j += 1
    #print(s)
    #print(bytes(s))
    s=s[::-1]
    s=bytes(s)
    return s

#функция padding_attac
#вход:шифр
#выход:расшифрованная атакой строка
def cbc_padding_attac(msg):
    n=len(msg)
    #print(n)
    s=""
    while n>16:
        c2 = msg[n - 16:n]  # получили последний блок
        c1 = msg[n - 32:n - 16]  # получили предпоследний блок
        #print(len(c2),len(c1))
        if n==len(msg):
            s=old_inspection(padding_attac_to_block(c2,c1))
        else:
            s=padding_attac_to_block(c2,c1).decode("UTF-8")+s
        #print(s)
        n-=16
    return s

i=0
while i<11:
    print(cbc_padding_attac(random_string(i)))
    i+=1



