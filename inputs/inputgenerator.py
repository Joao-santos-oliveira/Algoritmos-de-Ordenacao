import random

# Parametros para geração de inputs : -------
entrada = 10 ** 7
valor_minimo = 1
valor_maximo = 10 ** 4
arquivo_saida = 'inputs/input6.dat'

random.seed(42)
# -------------------------------------------

def gerar_inputs(tamanho : int, min : int, max : int) -> list:
    inputs = []
    for _ in range(tamanho):
        inputs.append(random.randint(min, max))
    return inputs

def salvar_inputs(arquivo : str, numeros : list):
    with open(arquivo, 'w') as file:
        file.write(str(len(numeros)) + '\n\n')
        file.write('\n'.join(map(str, numeros)))


numeros = gerar_inputs(entrada, valor_minimo, valor_maximo)
salvar_inputs(arquivo_saida, numeros)

