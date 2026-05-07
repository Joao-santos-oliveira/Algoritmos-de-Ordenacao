import os
''' Exemplo de output do comparador:
Linguagem: RUST
Algoritmo: Radix Sort
Input: inputs/input6.dat
Tempos de execução (em segundos):
Execução 0: 0.704212739
Execução 1: 0.600579389
Execução 2: 0.663947202
'''


def adquirir_quantidade_numeros(input: str) -> int:
    with open(input, 'r') as file:
        quantidade = int(file.readline().strip())
    return quantidade
    
class Grafico:
    def __init__(self, linguagem: str, algoritmo: str, input_file: str, tempos: list):
        self.linguagem = linguagem
        self.algoritmo = algoritmo
        self.input_file = input_file
        self.tempos : dict(int, float) = {}

diretorio_outputs = "../outputs/"

def adquirirGrafico(linguagem: str, algoritmo: str, input_file: str, graficos: dict(str, Grafico)) -> Grafico:
    key = f"{linguagem}_{algoritmo}_{input_file}"
    if key in graficos:
        return graficos[key]
    novo_grafico = Grafico(linguagem, algoritmo, input_file, [])
    graficos[key] = novo_grafico
    return novo_grafico

def comparar_algoritmos():
    arquivos = os.listdir(diretorio_outputs)
    graficos : dict(str, Grafico) = {}
    
    for arquivo in arquivos:
        if arquivo.endswith('.dat'):
            diretorio = os.path.join(diretorio_outputs, arquivo)
            with open(diretorio, 'r') as f:
                #Linha 1: Linguagem: RUST
                linguagem = f.readline().split(":")[1].strip()
                #Linha 2: Algoritmo: Radix Sort
                algoritmo = f.readline().split(":")[1].strip()

                f.readline()  # Ignorar a terceira linha
                f.readline()  # Ignorar a quarta linha

                tempos :list = []
                for line in f:
                    if line.startswith("Execução"):
                        tempo = float(line.split(":")[1].strip())
                        tempos.append(tempo)

                tempo_medio = sum(tempos) / len(tempos)

                grafico = adquirirGrafico(linguagem, algoritmo, arquivo, graficos)

                grafico.tempos[adquirir_quantidade_numeros(diretorio)] = tempo_medio

            

                   
