from binascii import a2b_base64
import binascii
from Crypto import Random
import re


"""вспомогательные f"""

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
    for i in s:
        array1[ord(i)-97]+=1
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


#готовим ключ
#key=Random.new().read(16)
s = []

#построчно считываем из файла и переводим в байты
with open('Lab2_breakctr3-b64.txt') as f:
    for line in f:
        curr_str = a2b_base64(line[:-1].encode())
        #s11=""
        #for i in curr_str:
         #   s11+=chr(i)
        #print(s11)
        s.append(curr_str)
f.close()

#статистика для английского алфавита
array = [8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.966, 0.153, 0.772, 4.025, 2.406, 6.749, 7.507,
         1.929, 0.095, 5.987, 6.327, 9.056, 2.758, 0.978, 2.360, 0.150, 1.974, 0.074]
i=0
for i in range(len(array)):
    array[i]=array[i]/100

#нахождение минимальной строки
msg=[]

min_len_s=1000
max_len_s=0
n=len(s) #количество строк
for bins in s:
    len_s=len(bins)  #ищем минимльную длину строки
    if len_s>max_len_s:
        max_len_s=len_s
    if len_s<min_len_s:
        min_len_s=len_s
#min_len_s=28
#деление на 28 строк для статистики для каждой
a=[]
for i in range(max_len_s):
    a.append("")
for ms in s:
    i=0
    for i in range(len(ms)):
        a[i]+=chr(ms[i])

good_s=""
key=""
#b=[]
for i in a:
    ss=chastota_plus_goodASCII_fromASCII(i)
    #b.append(ss[1])
    key+=ss[2]
print(key)
s1=""
k=0
for i in s:
    j=0
    s1=""
    while j<len(i):
        s1+=chr(i[j]^ord(key[j]))
        j+=1
    print("string "+str(k)+": "+s1)
    k+=1






