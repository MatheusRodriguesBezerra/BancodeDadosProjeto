i = 0
cant = []
band = []
while i < 81:
    a,b = map(int,input().split())
    band.append(a)
    cant.append(b)
    i = i+1
i = 0
resultado = ""
while i < 81:
    resultado = resultado + f'({band[i]},{cant[i]}),'
    i = i + 1 
print(resultado)