i = 0
nomes = []
pais = []
while i < 128:
    nome = str(input())
    nac = str(input())
    nomes.append(nome)
    pais.append(nac)
    i = i+1
i = 0
resultado = ""
while i < 128:
    resultado = resultado + f'({i+1},"{nomes[i]}","{pais[i]}"),'
    i = i + 1 
print(resultado)