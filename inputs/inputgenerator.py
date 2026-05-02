from tqdm import tqdm
import random

# Parametros para geração de inputs : -------
entrada = 10 ** 7
valor_minimo = 1
valor_maximo = 10 ** 4
arquivo_saida = 'inputs/input7.dat'

random.seed(42)
# -------------------------------------------


def gerar_inputs(tamanho: int, min: int, max: int) -> list:
    inputs = []

    # Barra de progresso na geração
    for _ in tqdm(range(tamanho), desc="Gerando números", unit="num"):
        inputs.append(random.randint(min, max))

    return inputs


def salvar_inputs(arquivo: str, numeros: list):
    with open(arquivo, 'w') as file:
        file.write(str(len(numeros)) + '\n\n')

        # Barra de progresso na escrita
        for numero in tqdm(numeros, desc="Salvando arquivo", unit="num"):
            file.write(str(numero) + ',')


numeros = gerar_inputs(entrada, valor_minimo, valor_maximo)
salvar_inputs(arquivo_saida, numeros)