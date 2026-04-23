#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#include "problema.h"

#include "radix/radix.h"
#include "counting/counting.h"
#include "introsort/introsort.h"

// Altere para ESCOLHER_EM_EXECUCAO ou para os enums de Algoritmos
#define ALGORITMO_USADO         ESCOLHER_EM_EXECUCAO
// Altere para ESCOLHER_EM_EXECUCAO ou para um numero correspondente ao numero do input
#define INPUT_USADO             ESCOLHER_EM_EXECUCAO

// Altere para ESCOLHER_EM_EXECUCAO ou para um numero correspondente ao numero de excucoes
// Serve para calcular o tempo médio do algoritmo
#define QUANTIDADE_EXECUCOES    ESCOLHER_EM_EXECUCAO

// 0 - Falso, 1 - Verdadeiro
#define EXIBIR_INFORMAÇÕES      0

void executar_algoritmo(problema* prob, void (*func_algoritmo) (int*, int)){
    double* lista_tempos = (double*) malloc(sizeof(double) * prob->quantidade_execucoes);
    int* lista = prob->lista;
    int tamanho = prob->tamanho;

    for(int i = 0; i < prob->quantidade_execucoes; i++){
        if (EXIBIR_INFORMAÇÕES) printf("\nExecução %d em andamento...\n", i + 1);
        clock_t start = clock();
        func_algoritmo(lista, tamanho);
        clock_t end = clock();
        lista_tempos[i] = (double)(end - start) / CLOCKS_PER_SEC;
        if (EXIBIR_INFORMAÇÕES) printf("Execução %d concluída. Tempo gasto: %lf segundos.\n", i + 1, lista_tempos[i]);
    };

    criar_output(prob, lista_tempos);
    free(lista_tempos);
}

int main(){
    srand(42);

    problema* problema = criar_problema(INPUT_USADO, ALGORITMO_USADO, QUANTIDADE_EXECUCOES);

    switch (problema->algoritmo_usado) {
        case RADIX_SORT: executar_algoritmo(problema, radix_sort); break;
        case COUNTING_SORT: executar_algoritmo(problema, counting_sort); break;
        case INTRO_SORT: executar_algoritmo(problema, intro_sort); break;
        
        case TODOS:
            problema->algoritmo_usado = RADIX_SORT;
            executar_algoritmo(problema, radix_sort);

            problema->algoritmo_usado = COUNTING_SORT;
            executar_algoritmo(problema, counting_sort);

            problema->algoritmo_usado = INTRO_SORT;
            executar_algoritmo(problema, intro_sort);
        break;

        default:
            printf("Algoritmo não implementado.\n");
        break;
    }

    printf("Algoritmos finalizados com sucesso...\n");
    free(problema->lista);
    free(problema);
    return 0;

}