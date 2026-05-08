#include <iostream>
#include <vector>

#include "counting.hpp"

using namespace std;

int CountingSort::getMaxValor(const vector<int>& list) const {

    int maxValor = list[0];

    for (size_t i = 1; i < list.size(); i++) {

        if (list[i] > maxValor) {
            maxValor = list[i];
        }
    }

    return maxValor;
}

void CountingSort::buildVetorFrequencia(vector<int>& list, vector<int>& count, int maxValor) const {

    for (size_t i = 0; i < list.size(); i++) {
        count[list[i]]++;
    }
}

void CountingSort::rebuildSortedList(vector<int>& list, const vector<int>& count) {

    vector<int> frequencia = count;

    size_t indice = 0;

    for (size_t value = 0; value < frequencia.size(); value++) {

        while (frequencia[value] > 0) {

            list[indice] = static_cast<int>(value);

            indice++;

            frequencia[value]--;
        }
    }
}

void CountingSort::sort(vector<int> list) {
    if (list.empty()) {
        return;
    }

    int maxValor = getMaxValor(list);

    vector<int> count(maxValor + 1, 0);

    buildVetorFrequencia(list, count, maxValor);

    rebuildSortedList(list, count);
}