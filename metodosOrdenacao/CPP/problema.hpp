#ifndef PROBLEMA_HPP
#define PROBLEMA_HPP

#include <vector>
#include <string>

using namespace std;
enum {
    ESCOLHER_EM_EXECUCAO = 0,
    RADIX_SORT,
    COUNTING_SORT,
    INTRO_SORT,
    TODOS,
};

#define INPUT1 "inputs/input1.dat"
#define INPUT2 "inputs/input2.dat"
#define INPUT3 "inputs/input3.dat"
#define INPUT4 "inputs/input4.dat"
#define INPUT5 "inputs/input5.dat"
#define INPUT6 "inputs/input6.dat"

typedef struct {
    vector<int> lista;

    string nome_input;
    int algoritmo_usado;
    int quantidade_execucoes;
} problema;

void ler_input(problema* prob, string filename);

string obter_nome_input(int input, string nome_input);

int obter_algoritmo_usado(int algoritmo, int algoritmo_usado);

int obter_quantidade_execucoes(int quantidade_execucoes, int quantidade_execucoes_obtida);

problema* criar_problema(int input, int algoritmo, int quantidade_execucoes);

void criar_output(problema* prob, vector<double> lista_tempos);

void exibir_lista(vector<int> lista);

#endif /* PROBLEMA_HPP*/