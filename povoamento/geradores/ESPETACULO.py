i = 0
palcos = []
datas = []
while i < 55:
    a,b,c = map(int,input().split())
    palcos.append(b)
    datas.append(c)
    i = i+1
i = 0
resultado = ""
while i < 55:
    resultado = resultado + f'({i+1},{palcos[i]},{datas[i]}),'
    i = i + 1 
print(resultado)