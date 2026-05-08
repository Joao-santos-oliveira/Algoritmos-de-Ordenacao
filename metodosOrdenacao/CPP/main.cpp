#include <iostream>
#include <vector>
#include <string>
#include <ctime>
#include <chrono>
#include <functional>
#include "problema.hpp"

#include "radix/radix.hpp"
#include "counting/counting.hpp"
#include "introsort/introsort.hpp"

// Altere para ESCOLHER_EM_EXECUCAO ou para os enums de Algoritmos
#define ALGORITMO_USADO         ESCOLHER_EM_EXECUCAO
// Altere para ESCOLHER_EM_EXECUCAO ou para um numero correspondente ao numero do input
#define INPUT_USADO             ESCOLHER_EM_EXECUCAO

// Altere para ESCOLHER_EM_EXECUCAO ou para um numero correspondente ao numero de excucoes
// Serve para calcular o tempo médio do algoritmo
#define QUANTIDADE_EXECUCOES    ESCOLHER_EM_EXECUCAO

// 0 - Falso, 1 - Verdadeiro
#define EXIBIR_INFORMAÇÕES      0

using namespace std;

void executar_algoritmo(problema* prob, MetodoOrdenacao* func_algoritmo){
    vector<double> lista_tempos(prob->quantidade_execucoes);

    for(int i = 0; i < prob->quantidade_execucoes; i++){
        if (EXIBIR_INFORMAÇÕES) cout << "\nExecução " <<  i + 1 << " em andamento..." << endl;
        
        auto start = chrono::high_resolution_clock::now();
        func_algoritmo->sort(prob->lista);
        auto end = chrono::high_resolution_clock::now();

        auto duracao = chrono::duration_cast<chrono::milliseconds>(end - start)/1000.0;
        lista_tempos[i] = duracao.count();
        
        if (EXIBIR_INFORMAÇÕES) cout << "Execução "<< i + 1 <<" concluída. Tempo gasto: "<< lista_tempos[i] << " segundos." << endl;
    };

    criar_output(prob, lista_tempos);
}


int main(){
    srand(42);

    problema* problema = criar_problema(INPUT_USADO, ALGORITMO_USADO, QUANTIDADE_EXECUCOES);
    MetodoOrdenacao* metodo_ordenacao;

    switch (problema->algoritmo_usado) {
        case RADIX_SORT: 
            metodo_ordenacao = new RadixSort();
            executar_algoritmo(problema, metodo_ordenacao);
            break;

        case COUNTING_SORT: 
            metodo_ordenacao = new CountingSort();
            executar_algoritmo(problema, metodo_ordenacao);
            break;

        case INTRO_SORT:
            metodo_ordenacao = new IntroSort();
            executar_algoritmo(problema, metodo_ordenacao);
            break;

        case TODOS:
            metodo_ordenacao = new RadixSort();
            problema->algoritmo_usado = RADIX_SORT;
            executar_algoritmo(problema, metodo_ordenacao);

            delete metodo_ordenacao;
            metodo_ordenacao = new CountingSort();
            problema->algoritmo_usado = COUNTING_SORT;
            executar_algoritmo(problema, metodo_ordenacao);

            delete metodo_ordenacao;
            metodo_ordenacao = new IntroSort();
            problema->algoritmo_usado = INTRO_SORT;
            executar_algoritmo(problema, metodo_ordenacao);
        break;

        default:
            printf("Algoritmo não implementado.\n");
        break;
    }

    printf("Algoritmos finalizados com sucesso...\n");
    delete metodo_ordenacao;
    delete problema;
    return 0;

}