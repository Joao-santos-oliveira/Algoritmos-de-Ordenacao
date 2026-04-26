#include <iostream>
#include <vector>

#include "radix.hpp"
#include "problema.hpp"

#define IMPRIMIR_LISTA 0

using namespace std;

int adquirir_maior_valor(vector<int> lista){
    int maior = lista[0];
    for(int valor : lista){
        if (valor > maior) maior = valor;
    }
    return maior;
}

void counting_sort_simplificado(vector<int> &lista, vector<int> &lista_aux, int expo){
    int count[10] = {0, 0, 0, 0, 0, 0 ,0, 0, 0, 0};
    int digito = 0;
    int tamanho = lista.size();

    for (int i = 0; i < tamanho; i++){
        count[(lista[i] / expo) % 10]++;
    }
    
    for (int i = 1; i < 10; i++){
        count[i] += count[i - 1];
    }

    for(int i = tamanho - 1; i >= 0; i--){
        digito = (lista[i] / expo) % 10;
        lista_aux[count[digito] - 1] = lista[i];
        count[digito]--;
    }

    for(int i = 0; i < tamanho; i++){
        lista[i] = lista_aux[i];
    }
}

void radix_sort(vector<int> lista){
    vector<int> lista_auxiliar(lista.size());

    int maior_valor = adquirir_maior_valor(lista);
    
    int expo = 1;

    if (IMPRIMIR_LISTA) exibir_lista(lista);

    while (maior_valor / expo > 0){
        counting_sort_simplificado(lista, lista_auxiliar, expo);
        expo *= 10;
    }

    if (IMPRIMIR_LISTA) {cout << "Lista Organizada: " << endl; exibir_lista(lista);}
}
