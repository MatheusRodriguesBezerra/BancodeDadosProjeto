i = 0
esp = []
cant = []
while i < 128:
    a,b = map(int,input().split())
    esp.append(a)
    cant.append(b)
    i = i+1
i = 0
resultado = ""
while i < 128:
    resultado = resultado + f'({esp[i]},{cant[i]}),'
    i = i + 1 
print(resultado)