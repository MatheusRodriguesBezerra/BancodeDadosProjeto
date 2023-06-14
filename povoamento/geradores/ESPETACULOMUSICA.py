i = 1
j = 1
resultado = ""
while i < 56:
    n = 1
    while n < 6:
        resultado = resultado + f'({i},{j}),'
        j = j + 1
        n = n + 1
    i = i + 1
print(resultado)