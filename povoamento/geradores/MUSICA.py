i = 0
musicas = []
while i < 275:
    musica = str(input())
    musicas.append(musica)
    i = i+1
i = 0
resultado = ""
while i < 275:
    resultado = resultado + f'({musicas[i]}),'
    i = i + 1 
print(resultado)