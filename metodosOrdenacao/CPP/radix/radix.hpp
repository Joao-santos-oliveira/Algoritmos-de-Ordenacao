#ifndef RADIX_H
#define RADIX_H

#include <iostream>
#include <vector>

using namespace std;

int adquirir_maior_valor(vector<int> lista);

void counting_sort_simplificado(vector<int> &lista, vector<int> &lista_aux, int expo);

void radix_sort(vector<int> lista);


#endif /* RADIX_H */