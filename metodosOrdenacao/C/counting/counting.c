#include <stdio.h>
#include <stdlib.h>
#include "counting.h"

void counting_sort(int* lista, int tamanho){

    int maior_valor = adquirir_maior_valor_c(lista, tamanho);

    int* count = malloc((maior_valor+1) * sizeof(int));

    for (int i = 0; i < maior_valor + 1; i++){
        count[i] = 0;
    }
    for(int i = 0; i <tamanho; i++){
        count[lista[i]]++;
    }
    for (int i = 1; i < maior_valor + 1; i++){
        count[i] += count[i-1];
    }

    int* aux = malloc(tamanho * sizeof(int));

    for(int i = tamanho-1; i > -1; i--){
        int valor = lista[i];
        aux[count[valor]-1] = valor;
        count[valor]--;
    }
    for(int i = 0; i <tamanho; i++){
        lista[i] = aux[i];
    }

    free(count);
    free(aux);

}

int adquirir_maior_valor_c(int* list, int tamanho){
    int maior = list[0];
    for (int i = 1; i < tamanho; i++){
        if (list[i] > maior) maior = list[i];
    }

    return maior;
}