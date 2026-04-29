#include <stdio.h>
#include <stdlib.h>
#include "introsort.h"
#include <math.h>

void swap(int* a, int* b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

void insertion_sort(int* lista, int inicio, int fim) {
    for (int i = inicio + 1; i <= fim; i++) {
        int chave = lista[i];
        int j = i - 1;

        while (j >= inicio && lista[j] > chave) {
            lista[j + 1] = lista[j];
            j--;
        }
        lista[j + 1] = chave;
    }
}

void heapify(int* lista, int n, int i, int offset) {
    int maior = i;
    int esq = 2*i + 1;
    int dir = 2*i + 2;

    if (esq < n && lista[offset + esq] > lista[offset + maior])
        maior = esq;

    if (dir < n && lista[offset + dir] > lista[offset + maior])
        maior = dir;

    if (maior != i) {
        swap(&lista[offset + i], &lista[offset + maior]);
        heapify(lista, n, maior, offset);
    }
}

void heap_sort(int* lista, int inicio, int fim) {
    int n = fim - inicio + 1;

    for (int i = n/2 - 1; i >= 0; i--)
        heapify(lista, n, i, inicio);

    for (int i = n - 1; i > 0; i--) {
        swap(&lista[inicio], &lista[inicio + i]);
        heapify(lista, i, 0, inicio);
    }
}

int partition(int* lista, int inicio, int fim) {
    int pivo = lista[fim];
    int i = inicio - 1;

    for (int j = inicio; j < fim; j++) {
        if (lista[j] <= pivo) {
            i++;
            swap(&lista[i], &lista[j]);
        }
    }

    swap(&lista[i + 1], &lista[fim]);
    return i + 1;
}

void introsort_util(int* lista, int inicio, int fim, int depth_limit) {
    int tamanho = fim - inicio + 1;

    // vetor pequeno
    if (tamanho < 16) {
        insertion_sort(lista, inicio, fim);
        return;
    }

    // heap, proteção contra pior caso
    if (depth_limit == 0) {
        heap_sort(lista, inicio, fim);
        return;
    }

    // quicksort
    int p = partition(lista, inicio, fim);

    introsort_util(lista, inicio, p - 1, depth_limit - 1);
    introsort_util(lista, p + 1, fim, depth_limit - 1);
}

void intro_sort(int* lista, int tamanho) {

    int depth_limit = 2 * log(tamanho);

    introsort_util(lista, 0, tamanho - 1, depth_limit);
}