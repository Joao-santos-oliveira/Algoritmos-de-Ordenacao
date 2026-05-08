#include <iostream>
#include <vector>
#include <cmath>

#include "introsort.hpp"
using namespace std;

void IntroSort::InsertionSort(vector<int>& list, int left, int right){
    for (int i = left +1; i<= right; i++){
        int atual = list[i]; // Guarda o valor atual 
        int j = i  - 1;     //Começa a comparar com o anterior
        while (j>= left && list[j] >atual){  // Verifica se o valor atual é maior ou igual ao anterior e se o anterior é maior ou igual ao seu anterior
            list[j+1] = list[j];                // Passa o valor anterior para a posição atual
            j--;                                // Move para o próximo valor anterior
        }
        list[j+1] = atual;      // Insere o valor atual na posição correta
    }
}

void IntroSort::Heapfy(vector<int>& list, int n, int i){
    int maior=i; // Assume que o pai é o maior
    int esq = 2*maior +1 ; // Inicia o filho esquerdo
    int dir = 2*maior +2 ; // Inicia o filho direito
    if(esq < n && list[esq] > list[maior]){ // Verifica se o filho esquerdo é maior que o pai
        maior = esq;                        // Caso seja, o filho esquerdo se torna o maior
    }
    if(dir < n && list[dir] > list[maior]){ // Verifica se o filho direito é maior que o pai
        maior = dir;                        // Se for, o filho direito se torna o maior
    }
    if(maior != i){ // Se o maior não for o pai
        swap(list[i], list[maior]); // Troca o pai com o maior
        Heapfy(list, n, maior); // Chama recursivamente para o novo pai
    }       
}


void IntroSort::HeapSort(vector<int>& list, int left, int right){
    int n = right - left + 1;   // Calcula o tamanho do vetor
    for (int i = n / 2 - 1; i >= 0; i--){ // Constrói o heap
        Heapfy(list, n, i);
    }
    for (int i = n - 1; i > 0; i--){ // Extrai os elementos do heap
        swap(list[0], list[i]);     // Move o maior para o final
        Heapfy(list, i, 0);               // Chama recursivamente para o heap reduzido
    }       
}

void IntroSort::QuickSort(vector<int>& list, int left, int right, int depthLimit){
    if (right - left <= 16){
    InsertionSort(list, left, right);
    return;
    }
    if (depthLimit == 0){
        HeapSort(list, left, right);
        return;
    }
    else{
        int pivo = Partition(list, left, right); // Particiona o vetor e obtém o índice do pivô
        QuickSort(list, left, pivo - 1, depthLimit - 1); // Orden a a parte esquerda do pivô
        QuickSort(list, pivo + 1, right, depthLimit - 1); // Orden a a parte direita do pivô  
    }


}
int IntroSort::Partition(vector<int>& list, int left, int right){
    int pivo = list[right];             // último elemento como pivô
    int i = left - 1;                   // Índice do menor elemento
    for (int j = left; j < right; j++) {
        if (list[j] <= pivo) {          // Se o elemento atual é menor ou igual ao pivô
            i++;                        // Incrementa o índice do menor elemento
            swap(list[i], list[j]);     // Troca o elemento atual com o menor elemento
        }
    }
    swap(list[i + 1], list[right]); // Coloca o pivô na posição correta
    return i + 1; // Retorna a posição do pivô
}


void IntroSort::sort(vector<int> list) {
    int depthLimit = 2 * log2(list.size()); // Define o limite de profundidade
    QuickSort(list, 0, list.size() - 1, depthLimit); // Chama a função de ordenação
}   