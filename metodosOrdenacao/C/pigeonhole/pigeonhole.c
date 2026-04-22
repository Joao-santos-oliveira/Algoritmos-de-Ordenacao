#include <stdio.h>
#include <stdlib.h>
#include "pigeonhole.h"

void pigeonhole_sort(int* lista, int tamanho){

    if(tamanho <= 0) return;

    int min = lista[0];
    int max = lista[0];

    for(int i = 1; i < tamanho; i++){
        if(lista[i] < min) min = lista[i];
        if(lista[i] > max) max = lista[i];
    }

    int range = max - min + 1;

    int* holes = (int*) calloc(range, sizeof(int));

    for(int i = 0; i < tamanho; i++){
        holes[lista[i] - min]++;
    }

    int index = 0;
    for(int i = 0; i < range; i++){
        while(holes[i] > 0){
            lista[index++] = i + min;
            holes[i]--;
        }
    }
    free(holes);
}
