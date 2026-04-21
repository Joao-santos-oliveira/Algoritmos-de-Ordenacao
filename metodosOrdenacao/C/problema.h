#ifndef PROBLEMA_H
#define PROBLEMA_H

enum {
    ESCOLHER_EM_EXECUCAO = 0,
    RADIX_SORT,
    COUNTING_SORT,
    PIGEONHOLE_SORT,
    TODOS,
};

#define INPUT1 "inputs/input1.dat"
#define INPUT2 "inputs/input2.dat"
#define INPUT3 "inputs/input3.dat"
#define INPUT4 "inputs/input4.dat"
#define INPUT5 "inputs/input5.dat"
#define INPUT6 "inputs/input6.dat"

typedef struct {
    int* lista;
    int tamanho;

    char nome_input[50];
    int algoritmo_usado;
    int quantidade_execucoes;
} problema;

void ler_input(problema* prob, char* filename);

void obter_nome_input(int input, char* nome_input);

void obter_algoritmo_usado(int algoritmo, int* algoritmo_usado);

void obter_quantidade_execucoes(int quantidade_execucoes, int* quantidade_execucoes_obtida);

problema* criar_problema(int input, int algoritmo, int quantidade_execucoes);

void criar_output(problema* prob, double* lista_tempos);

#endif /* PROBLEMA_H */