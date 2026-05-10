#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "radix.h"
#include "problema.h"

#define IMPRIMIR_LISTA 0

int adquirir_maior_valor(int* list, int tamanho){
    int maior = list[0];
    for (int i = 1; i < tamanho; i++){
        if (list[i] > maior) maior = list[i];
    }

    return maior;
}

void counting_sort_simplificado(int** lista, int** lista_aux, int tamanho, int expo){
    int count[10] = {0};

    for (int i = 0; i < tamanho; i++){
        count[((*lista)[i] / expo) % 10]++;
    }
    
    for (int i = 1; i < 10; i++){
        count[i] += count[i - 1];
    }

    for(int i = tamanho - 1; i >= 0; i--){
        int digito = ((*lista)[i] / expo) % 10;
        (*lista_aux)[count[digito] - 1] = (*lista)[i];
        count[digito]--;
    }

    // 🔥 troca real (agora funciona)
    int* temp = *lista;
    *lista = *lista_aux;
    *lista_aux = temp;
}

//Radix Sort LSD
void radix_sort(int* lista, int tamanho){
    int* lista_auxiliar = (int *) malloc(sizeof(int) * tamanho);
    int* aux_original = lista_auxiliar;

    int maior_valor = adquirir_maior_valor(lista, tamanho);
    int expo = 1;

    if (IMPRIMIR_LISTA) {exibir_lista(lista, tamanho); printf("\n");}

    while (maior_valor / expo > 0){
        counting_sort_simplificado(&lista, &lista_auxiliar, tamanho, expo);
        expo *= 10;
    }

    if (IMPRIMIR_LISTA) {printf("Lista Organizada: \n"); exibir_lista(lista, tamanho); printf("\n");}
    

    free(aux_original);
}