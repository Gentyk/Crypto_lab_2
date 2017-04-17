from task5 import  Mersenne
from random import randint
import time

def attac_to_Mers():
    time.sleep(randint(10,20))#приостанавливаем на 10-20 секунд
    start=int(time.time())
    r=Mersenne(start)
    print("время старта: "+str(start))
    time.sleep(randint(10, 20))  # приостанавливаем на 10-20 секунд
    result=r.extract_number() #получили случайное число
    print("\nзначение: " + str(result))
    second_start=time.time()
    for i in range(2400):#40 минут на всякий пожарный
        t=second_start-i
        r2=Mersenne(int(t))
        v2=r2.extract_number()
        if (result==v2):
            print("\ntime= "+str(int(t))+"; value= "+str(v2))
            break

attac_to_Mers()




