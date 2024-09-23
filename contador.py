import time

contador = 0

while contador < 10:
    print(f'Contador: {contador}', end='\r')
    contador +=1
    time.sleep(1)