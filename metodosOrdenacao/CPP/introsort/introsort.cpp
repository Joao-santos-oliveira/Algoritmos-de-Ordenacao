#include <iostream>
#include <vector>
#include <cmath>

#include "introsort.hpp"
using namespace std;

void IntroSort::InsertionSort(vector<int>& list, int left, int right) {
    for (int i = left + 1; i <= right; i++) {
        int atual = list[i];
        int j = i - 1;
        while (j >= left && list[j] > atual) {
            list[j + 1] = list[j];
            j--;
        }
        list[j + 1] = atual;
    }
}

void IntroSort::Heapfy(vector<int>& list, int left, int n, int i) {
    // FIX: recebe 'left' para converter entre índices locais e absolutos
    while (true) {
        int maior = i;
        int esq   = 2 * (i - left) + 1 + left;
        int dir   = 2 * (i - left) + 2 + left;

        if (esq < n && list[esq] > list[maior]) maior = esq;
        if (dir < n && list[dir] > list[maior]) maior = dir;

        if (maior == i) break;

        swap(list[i], list[maior]);
        i = maior;  // iterativo: elimina recursão de cauda e evita stack overflow
    }
}

void IntroSort::HeapSort(vector<int>& list, int left, int right) {
    int n = right + 1;  // FIX: limite absoluto, não tamanho relativo

    // Constrói o heap máximo na faixa [left, right]
    for (int i = left + (right - left) / 2; i >= left; i--)
        Heapfy(list, left, n, i);

    // Extrai elementos do heap em ordem decrescente
    for (int i = right; i > left; i--) {
        swap(list[left], list[i]);
        Heapfy(list, left, i, left);
    }
}

int IntroSort::Partition(vector<int>& list, int left, int right) {
    // FIX: pivô mediana-de-3 — evita O(n²) em arrays ordenados/quase-ordenados
    int mid = left + (right - left) / 2;
    if (list[left] > list[mid])   swap(list[left],  list[mid]);
    if (list[left] > list[right]) swap(list[left],  list[right]);
    if (list[mid]  > list[right]) swap(list[mid],   list[right]);
    // Agora list[mid] é a mediana; coloca como pivô em right-1
    swap(list[mid], list[right - 1]);
    int pivo = list[right - 1];

    int i = left;
    int j = right - 1;
    while (true) {
        while (list[++i] < pivo) {}
        while (list[--j] > pivo) {}
        if (i >= j) break;
        swap(list[i], list[j]);
    }
    swap(list[i], list[right - 1]);
    return i;
}

void IntroSort::QuickSort(vector<int>& list, int left, int right, int depthLimit) {
    if (right - left < 16) {
        InsertionSort(list, left, right);
        return;
    }
    if (depthLimit == 0) {
        HeapSort(list, left, right);
        return;
    }
    int pivo = Partition(list, left, right);
    QuickSort(list, left,      pivo - 1, depthLimit - 1);
    QuickSort(list, pivo + 1,  right,    depthLimit - 1);
}

void IntroSort::sort(vector<int> list) {
    
    if (list.size() < 2) return;
    int depthLimit = 2 * (int)log2((double)list.size());
    QuickSort(list, 0, (int)list.size() - 1, depthLimit);
}