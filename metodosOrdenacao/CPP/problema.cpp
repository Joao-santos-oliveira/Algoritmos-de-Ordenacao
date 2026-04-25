#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <ctime>
#include "problema.hpp"

using namespace std;

void ler_input(problema* prob, string filename){
    ifstream file(filename);
    if (!file.is_open()) {
        cout << "\033[31m Erro ao abrir arquivo\n";
        cout <<" Arquivo não encontrado ou inacessível: "<< filename <<"\n \033[0m";
        exit(1);
    }

    int tamanho = 0;
    file >> tamanho;
    vector<int> lista(tamanho);

    int valor;
    for(int i = 0; i < tamanho; file >> lista[i++]);

    prob->lista = lista;

    file.close();
}

string obter_nome_input(int input, string nome_input){
    if (input == ESCOLHER_EM_EXECUCAO) {
        do{
            cout << " Escolha o Input a ser usado:\n";
            cout << "1. Input 1\n2. Input 2\n3. Input 3\n4. Input 4\n5. Input 5\n6. Input 6\nResposta: ";
            
            cin >> input;
            
            if (input < 1 || input > 6) cout << "\n \033[31m Opção inválida. Por favor, escolha um número entre 1 e 6. \033[0m \n\n";
        } while (input < 1 || input > 6);

        switch (input) {
            case 1: nome_input = INPUT1; break;
            case 2: nome_input = INPUT2; break;
            case 3: nome_input = INPUT3; break;
            case 4: nome_input = INPUT4; break;
            case 5: nome_input = INPUT5; break;
            case 6: nome_input = INPUT6; break;
        }
    }

    return nome_input;
}

void obter_algoritmo_usado(int algoritmo, int* algoritmo_usado) {
    if (algoritmo == ESCOLHER_EM_EXECUCAO) {
        do {
            cout << "\n Escolha o algoritmo:\n1. Radix\n2. Counting\n3. intro Sort\n4. Todos\nResposta: ";
            
            cin >> algoritmo;
            if (algoritmo < 1 || algoritmo > 4)
                cout << "\n \033[31m Opção inválida.\033[0m\n\n";
        } while (algoritmo < 1 || algoritmo > 4);
    }
    *algoritmo_usado = algoritmo; // ✅ salva o valor
}

void obter_quantidade_execucoes(int quantidade_execucoes, int* quantidade_execucoes_obtida) {
    if (quantidade_execucoes == ESCOLHER_EM_EXECUCAO) {
        do {
            cout << "\n Digite a quantidade de execuções (1 ou mais): ";
            
            cin >> quantidade_execucoes;
            if (quantidade_execucoes < 1)
                cout << "\n \033[31m Quantidade inválida.\033[0m\n\n";
        } while (quantidade_execucoes < 1);
    }
    *quantidade_execucoes_obtida = quantidade_execucoes; // ✅ salva o valor
}

problema* criar_problema(int input, int algoritmo, int quantidade_execucoes){
    problema* prob = new problema;
    prob->algoritmo_usado = algoritmo;
    prob->quantidade_execucoes = quantidade_execucoes;

    prob->nome_input = obter_nome_input(input, prob->nome_input);
    obter_algoritmo_usado(algoritmo, &prob->algoritmo_usado);
    obter_quantidade_execucoes(quantidade_execucoes, &prob->quantidade_execucoes);
    ler_input(prob, prob->nome_input);

    return prob;
}

void criar_output(problema* prob, vector<double> lista_tempos){
    int nome_algoritmo = prob->algoritmo_usado;
    int quantidade_execucoes = prob->quantidade_execucoes;
    string nome_input = prob->nome_input;

    string nome_algoritmo_str;

    switch (nome_algoritmo) {
        case RADIX_SORT: nome_algoritmo_str = "Radix Sort"; break;
        case COUNTING_SORT: nome_algoritmo_str = "Counting Sort"; break;
        case INTRO_SORT: nome_algoritmo_str = "introsort Sort"; break;
    }

    string nome_arquivo = "outputs/output"  + nome_algoritmo_str + to_string(time(NULL)) + ".dat";

    ofstream file(nome_arquivo);

    if (!file.is_open()) {
        cout << "Erro ao criar o arquivo de saída.\n";
        return;
    }

    file << "Linguagem: C++" << endl;
    file << "Algoritmo: " << nome_algoritmo_str << endl;
    file << "Input: " << nome_input << endl;

    file << "Tempos de execução (em segundos):" << endl;;
    for (int i = 0; i < quantidade_execucoes; file << "Execução " <<  i << ": "<< lista_tempos[i++] << endl);
    
    file.close();
}

void exibir_lista(vector<int> lista){
    for (int valor : lista){
        cout << valor << " ";
    }
}