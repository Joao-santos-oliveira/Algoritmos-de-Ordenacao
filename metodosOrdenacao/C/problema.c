#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

#include "problema.h"

void ler_input(problema* prob, char* filename){
    FILE *file = fopen(filename, "r");
    if (file == NULL) { 
        printf("\033[31m Erro ao abrir o arquivo.\n"); 
        printf(" Arquivo não encontrado ou inacessível: %s\n \033[0m", filename);
        exit(1);
    }
    
    int tamanho = 0;
    fscanf(file, "%d ", &tamanho);
    int* lista = (int *) malloc(sizeof(int) * tamanho);
    
    fscanf(file, "\n"); //pula a linha em branco

    for (int i = 0; i < tamanho; fscanf(file, "%d", &lista[i++]));
    
    fclose(file);
    prob->lista = lista;
    prob->tamanho = tamanho;
}

void obter_nome_input(int input, char* nome_input){
    if (input == ESCOLHER_EM_EXECUCAO) {
        do{
            printf(" Escolha o Input a ser usado:\n");
            printf("1. Input 1\n2. Input 2\n3. Input 3\n4. Input 4\n5. Input 5\n6. Input 6\nResposta: ");
            scanf("%d", &input);
            getchar(); // Limpar o buffer do teclado
            if (input < 1 || input > 6) printf("\n \033[31m Opção inválida. Por favor, escolha um número entre 1 e 6. \033[0m \n\n");
        } while (input < 1 || input > 6);
    }

    switch (input) {
            case 1: strcpy(nome_input, INPUT1); break;
            case 2: strcpy(nome_input, INPUT2); break;
            case 3: strcpy(nome_input, INPUT3); break;
            case 4: strcpy(nome_input, INPUT4); break;
            case 5: strcpy(nome_input, INPUT5); break;
            case 6: strcpy(nome_input, INPUT6); break;
        }
}

void obter_algoritmo_usado(int algoritmo, int* algoritmo_usado) {
    if (algoritmo == ESCOLHER_EM_EXECUCAO) {
        do {
            printf("\n Escolha o algoritmo:\n1. Radix\n2. Counting\n3. intro Sort\n4. Todos\nResposta: ");
            scanf("%d", &algoritmo);
            getchar();
            if (algoritmo < 1 || algoritmo > 4)
                printf("\n \033[31m Opção inválida.\033[0m\n\n");
        } while (algoritmo < 1 || algoritmo > 4);
    }
    *algoritmo_usado = algoritmo; // ✅ salva o valor
}

void obter_quantidade_execucoes(int quantidade_execucoes, int* quantidade_execucoes_obtida) {
    if (quantidade_execucoes == ESCOLHER_EM_EXECUCAO) {
        do {
            printf("\n Digite a quantidade de execuções (1 ou mais): ");
            scanf("%d", &quantidade_execucoes);
            getchar();
            if (quantidade_execucoes < 1)
                printf("\n \033[31m Quantidade inválida.\033[0m\n\n");
        } while (quantidade_execucoes < 1);
    }
    *quantidade_execucoes_obtida = quantidade_execucoes; // ✅ salva o valor
}


problema* criar_problema(int input, int algoritmo, int quantidade_execucoes){
    problema* prob = (problema*) malloc(sizeof(problema));
    prob->algoritmo_usado = algoritmo;
    prob->quantidade_execucoes = quantidade_execucoes;

    obter_nome_input(input, prob->nome_input);
    obter_algoritmo_usado(algoritmo, &prob->algoritmo_usado);
    obter_quantidade_execucoes(quantidade_execucoes, &prob->quantidade_execucoes);
    ler_input(prob, prob->nome_input);

    return prob;
}

void criar_output(problema* prob, double* lista_tempos){
    int nome_algoritmo = prob->algoritmo_usado;
    int quantidade_execucoes = prob->quantidade_execucoes;
    char nome_input[50];
    strcpy(nome_input, prob->nome_input);

    char nome_algoritmo_str[20];

    switch (nome_algoritmo) {
        case RADIX_SORT: strcpy(nome_algoritmo_str, "Radix Sort"); break;
        case COUNTING_SORT: strcpy(nome_algoritmo_str, "Counting Sort"); break;
        case INTRO_SORT: strcpy(nome_algoritmo_str, "introsort Sort"); break;
    }

    char nome_arquivo[100] = "outputs/output";
    char tempo[20];
    
    sprintf(tempo, "%ld", clock());

    strcat(nome_arquivo, tempo);
    strcat(nome_arquivo, ".dat");

    FILE *file = fopen(nome_arquivo, "w");

    if (file == NULL) {
        printf("Erro ao criar o arquivo de saída.\n");
        return;
    }

    fprintf(file, "Linguagem: C\n");
    fprintf(file, "Algoritmo: %s\n", nome_algoritmo_str);
    fprintf(file, "Input: %s\n", nome_input);

    fprintf(file, "Tempos de execução (em segundos):\n");
    for (int i = 0; i < quantidade_execucoes; fprintf(file, "Execução %d: %lf\n", i, lista_tempos[i++]));
    
    fclose(file);
}

void exibir_lista(int* lista, int tamanho){
    for(int i = 0; i < tamanho; i++){
        printf("%d, ", lista[i]);
    }
}