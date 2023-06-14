i = 0
bandas = []
pais = []
ni = []
while i < 19:
    banda = str(input())
    nac = str(input())
    n = int(input())
    bandas.append(banda)
    pais.append(nac)
    ni.append(n)
    i = i+1
i = 0
while i < 19:
    resultado = f'({i+1},"{bandas[i]}","{pais[i]}",{ni[i]}),'
    print(resultado)
    i = i + 1 