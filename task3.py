from binascii import a2b_base64
from Crypto.Cipher import AES
import binascii
import re
from Crypto.Util import Counter
from Crypto import Random

"""вспомогательные f"""
class counter(object):
    value = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    def __init__(self):
        self.value = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')

    def __call__(self):
        buf = bytearray(self.value)
        self.value[8] = self.value[8] + 1
        return bytes(buf)

def new_s(st):
    p = re.compile('[a-z]+')
    s1 = p.findall(st)
    s=""
    for i in s1:
        s+=i
    return s
#получение числа сумма(pi-pср)
#вводим строку только! с латиницей, но любым регистром
def chasota(s):
    #s=tab_s(s)
    array=[ 8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.966, 0.153, 0.772, 4.025, 2.406, 6.749, 7.507, 1.929, 0.095, 5.987, 6.327, 9.056, 2.758, 0.978, 2.360, 0.150, 1.974, 0.074 ]
    array1=[]
    j=0
    #забиваем массив размера 26 нулями
    while j<26 :
        array1.append(0)
        j+=1
    j=0
    for i in s:
        if (0<=ord(i)-97<26):

            array1[ord(i)-97]+=1
            j+=1
        if (i==" "):
            j+=1
    if j<len(s)//3*2:
        return 100
    n=0
    j = 0
    if(len(s)!=0):
        while j < 26:
            n+=abs(array1[j]/len(s)-array[j]/100)
            j+=1
    else:
        n=10
    return n

#перевод в нижний регистр
def tab_s(s):
    i=0
    ss=""
    while(i<len(s)):
        if (ord(s[i])<91):
            ss+=chr(ord(s[i])-65+97)
        else:
            ss+=s[i]
        i+=1
    return ss

#генератор слова такой же длины, как s, из ключа k
def key_xor_word(s,k):
    n=len(s)//len(k)
    j=0
    s1=""
    while (j<n):
        s1+=k
        j+=1
    n=len(s)%len(k)
    j=0
    while(j<n):
        s1+=k[j]
        j+=1
    return s1

#вводи ключ k и строку s (ASCII)
#нам возвращается отксоренная строка в hex виде
def xorASCII_to_hex(s1,kl):
    s2 = key_xor_word(s1, kl)
    s3 = ""
    j = 0
    while (j < len(s1)):
        bins = (ord(s1[j]) ^ ord(s2[j]))
        bins1 = bins.to_bytes(1, byteorder="big")
        s3 += (binascii.b2a_hex(bins1)).decode('UTF-8')
        j += 1
    return s3


def chastota_plus_goodASCII_fromASCII(s):
    j = 0
    n1 = 100
    c=''
    good_string = ""
    while (j <= 255):
        s1=""
        i=0
        while (i<len(s)):
            h=j^ord(s[i])
            i+=1
            s1+=chr(h)
        s2=s1
        s1 = new_s(s1)
        n2 = chasota(s1)
        if (n1 > n2):
            n1 = n2;
            good_string = s2;
            c=chr(j)
        j += 1
    arr=[]
    arr.append(n1)
    arr.append(good_string)
    arr.append(c)
    #print(arr)
    return arr

def xor_one_char(string, char):
    result = ""
    for c in string:
        result += chr(ord(c) ^ ord(char))
    return result




"""Основной код"""
sBase64=[
"SXQgd2FzIG1hbnkgYW5kIG1hbnkgYSB5ZWFyIGFnbywK",
"SW4gYSBraW5nZG9tIGJ5IHRoZSBzZWEsCg==",
"VGhhdCBhIG1haWRlbiB0aGVyZSBsaXZlZCB3aG9tIHlvdSBtYXkga25vdwo=",
"QnkgdGhlIG5hbWUgb2YgQW5uYWJlbCBMZWU7Cg==",
"QW5kIHRoaXMgbWFpZGVuIHNoZSBsaXZlZCB3aXRoIG5vIG90aGVyIHRob3VnaHQK",
"VGhhbiB0byBsb3ZlIGFuZCBiZSBsb3ZlZCBieSBtZS4K",
"SSB3YXMgYSBjaGlsZCBhbmQgc2hlIHdhcyBhIGNoaWxkLAo=",
"SW4gdGhpcyBraW5nZG9tIGJ5IHRoZSBzZWEsCg==",
"QnV0IHdlIGxvdmVkIHdpdGggYSBsb3ZlIHRoYXQgd2FzIG1vcmUgdGhhbiBsb3Zl4oCUCg==",
"SSBhbmQgbXkgQW5uYWJlbCBMZWXigJQK",
"V2l0aCBhIGxvdmUgdGhhdCB0aGUgd2luZ8OoZCBzZXJhcGhzIG9mIEhlYXZlbgo=",
"Q292ZXRlZCBoZXIgYW5kIG1lLgo=",
"QW5kIHRoaXMgd2FzIHRoZSByZWFzb24gdGhhdCwgbG9uZyBhZ28sCg==",
"SW4gdGhpcyBraW5nZG9tIGJ5IHRoZSBzZWEsCg==",
"QSB3aW5kIGJsZXcgb3V0IG9mIGEgY2xvdWQsIGNoaWxsaW5nCg==",
"TXkgYmVhdXRpZnVsIEFubmFiZWwgTGVlOwo=",
"U28gdGhhdCBoZXIgaGlnaGJvcm4ga2luc21lbiBjYW1lCg==",
"QW5kIGJvcmUgaGVyIGF3YXkgZnJvbSBtZSwK",
"VG8gc2h1dCBoZXIgdXAgaW4gYSBzZXB1bGNocmUK",
"SW4gdGhpcyBraW5nZG9tIGJ5IHRoZSBzZWEuCg==",
"VGhlIGFuZ2Vscywgbm90IGhhbGYgc28gaGFwcHkgaW4gSGVhdmVuLAo=",
"V2VudCBlbnZ5aW5nIGhlciBhbmQgbWXigJQK",
"WWVzIeKAlHRoYXQgd2FzIHRoZSByZWFzb24gKGFzIGFsbCBtZW4ga25vdywK",
"SW4gdGhpcyBraW5nZG9tIGJ5IHRoZSBzZWEpCg==",
"VGhhdCB0aGUgd2luZCBjYW1lIG91dCBvZiB0aGUgY2xvdWQgYnkgbmlnaHQsCg==",
"Q2hpbGxpbmcgYW5kIGtpbGxpbmcgbXkgQW5uYWJlbCBMZWUuCg==",
"QnV0IG91ciBsb3ZlIGl0IHdhcyBzdHJvbmdlciBieSBmYXIgdGhhbiB0aGUgbG92ZQo=",
"T2YgdGhvc2Ugd2hvIHdlcmUgb2xkZXIgdGhhbiB3ZeKAlAo=",
"T2YgbWFueSBmYXIgd2lzZXIgdGhhbiB3ZeKAlAo=",
"QW5kIG5laXRoZXIgdGhlIGFuZ2VscyBpbiBIZWF2ZW4gYWJvdmUK",
"Tm9yIHRoZSBkZW1vbnMgZG93biB1bmRlciB0aGUgc2VhCg==",
"Q2FuIGV2ZXIgZGlzc2V2ZXIgbXkgc291bCBmcm9tIHRoZSBzb3VsCg==",
"T2YgdGhlIGJlYXV0aWZ1bCBBbm5hYmVsIExlZTsK",
"Rm9yIHRoZSBtb29uIG5ldmVyIGJlYW1zLCB3aXRob3V0IGJyaW5naW5nIG1lIGRyZWFtcwo=",
"T2YgdGhlIGJlYXV0aWZ1bCBBbm5hYmVsIExlZTsK",
"QW5kIHRoZSBzdGFycyBuZXZlciByaXNlLCBidXQgSSBmZWVsIHRoZSBicmlnaHQgZXllcwo=",
"T2YgdGhlIGJlYXV0aWZ1bCBBbm5hYmVsIExlZTsK",
"QW5kIHNvLCBhbGwgdGhlIG5pZ2h0LXRpZGUsIEkgbGllIGRvd24gYnkgdGhlIHNpZGUK",
"T2YgbXkgZGFybGluZ+KAlG15IGRhcmxpbmfigJRteSBsaWZlIGFuZCBteSBicmlkZSwK",
"SW4gaGVyIHNlcHVsY2hyZSB0aGVyZSBieSB0aGUgc2Vh4oCUCg==",
"SW4gaGVyIHRvbWIgYnkgdGhlIHNvdW5kaW5nIHNlYS4K"
]

#1) переводим в ascii
s=[] #массив открытых текстов
for st in sBase64:
    bins=a2b_base64(st)
    s1=""
    for i in bins:
        s1+=chr(i)
    s.append(s1)

#2)шифруем
print("шифруем")
key=Random.new().read(16)
msg=[]#массив зашифрованного
for st in s:
    ctr = counter()
    result = ""
    for i in range(len(st) // 16):#поблочно(пока есть блоки по 16 - шифруем)
        count = ctr()
        cipher = AES.new(key, AES.MODE_ECB)
        keystream = cipher.encrypt(count)
        for j in range(16):
            result += chr(keystream[j] ^ ord(st[i * 16 + j]))
    if len(st) % 16 > 0: #остаточек
        count = ctr()
        cipher = AES.new(key, AES.MODE_ECB)
        keystream = cipher.encrypt(count)
        for j in range(len(st) % 16):
            result += chr(keystream[j] ^ ord(st[(i + 1) * 16 + j]))
    msg.append(result)

#3)находим минамыльную длину строк
min=1000
max=0
for st in msg:
    if len(st)<min:
        min=len(st)
    if len(st) > max:
        max = len(st)

print(str(min)+" "+str(max))

good=[]
key_good=""
#4)начинаем по столбикам вырезать списки
print("анализ")
for i in range(max):
    #print(str(i)+" столбик")
    column = ""
    for st in msg:
        if i<len(st):
            column += st[i]  # вырезаем столбец и записываем в строку

    #набываем в список "a" символы из колонки(column) и считаем количество каждого
    a = {}
    for c in column:
        if a.get(c) == None: #dict.get(key[, default]) - возвращает значение ключа,
                             # но если его нет, не бросает исключение,
                             # а возвращает default (по умолчанию None).
            a[c] = 1
        else:
            a[c] += 1

    #записываем в массив "b" наши сиволы и их количество
    b = []
    while True:
        try:
            item = a.popitem() #pop
            b.append([item[1], item[0]])
        except:
            break
    b.sort(reverse=True)

    model_eng = [" ", "e", "t", "a", "o", "i", "n", "s", "h", "r", "d", "l", "c", "u", "m", "w", "f", "g", "y",
                 "p", "b", "v", "k", "x", "j", "q", "z"]
    columns_strs = []
    n1=1000
    good_str=""
    for c in model_eng:
        buf_str = xor_one_char(column, chr(ord(c) ^ ord(b[0][1]))) #берем самый часто повторяющийся
                                                                  #  символ в строке ^c и ксорим
                                                                  # с строкой column
        z=chasota(buf_str)
        if z < n1:
            n1=z
            good_str=buf_str
            k=chr(ord(c) ^ ord(b[0][1]))
    key_good+=k
    #print(good_str)
    good.append(good_str)


print("результат:")
for j in range(len(s)):
    s1=""
    for i in range(min):
        #print(str(i)+" "+str(j))
        s1+=good[i][j]
    print(s1)
print("ключ :"+str(key_good)+"")

print("\nрезультат 2:")
j=0
for st in msg:
    s1=""
    for i in range(len(st)):
        s1+=chr(ord(st[i])^ord(key_good[i]))
    print("строка "+str(j)+":"+s1)
    j+=1












