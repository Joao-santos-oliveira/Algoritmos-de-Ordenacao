from tqdm import tqdm

input_alvo = '6'  # Altere para o número do input desejado (1 a 6)
arquivo_entrada = f'inputs/input{input_alvo}.dat'
arquivo_saida_cord = f'inputs/input{input_alvo}_cord.dat'
arquivo_saida_dord = f'inputs/input{input_alvo}_dord.dat'

def ler_arquivo(arquivo: str) -> list:
    with open(arquivo, 'r') as file:
        file.readline()
        file.readline()

        # Lendo o conteudo linha por linha e convertendo para inteiro
        numeros = [int(line.strip()) for line in file]
    return numeros

def salvar_arquivo(arquivo: str, numeros: list):
    with open(arquivo, 'w') as file:
        file.write(str(len(numeros)) + '\n\n')

        for numero in tqdm(numeros, desc=f"Salvando {arquivo}", unit="num"):
            file.write(str(numero))
            if (numero != numeros[-1]):
                file.write('\n')

numeros :list = ler_arquivo(arquivo_entrada)

numeros_cord = sorted(numeros)
numeros_dord = sorted(numeros, reverse=True)

salvar_arquivo(arquivo_saida_cord, numeros_cord)
salvar_arquivo(arquivo_saida_dord, numeros_dord)