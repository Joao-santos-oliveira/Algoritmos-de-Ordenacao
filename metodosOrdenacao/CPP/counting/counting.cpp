#include <iostream>
#include <vector>

#include "counting.hpp"

using namespace std;

CountingSort::CountingSort(vector<int>& list)
    : list(list) {}

vector<int> CountingSort::getList() {
    return this->list;
}

int CountingSort::getMaxValor() const {

    int maxValor = list[0];

    for (size_t i = 1; i < list.size(); i++) {

        if (list[i] > maxValor) {
            maxValor = list[i];
        }
    }

    return maxValor;
}

void CountingSort::buildVetorFrequencia(vector<int>& count, int maxValor) const {

    for (size_t i = 0; i < list.size(); i++) {
        count[list[i]]++;
    }
}

void CountingSort::rebuildSortedList(const vector<int>& count) {

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

void CountingSort::sort() {

    if (list.empty()) {
        return;
    }

    int maxValor = getMaxValor();

    vector<int> count(maxValor + 1, 0);

    buildVetorFrequencia(count, maxValor);

    rebuildSortedList(count);
}

void counting_sort(vector<int>& list) {

    CountingSort sorter(list);

    sorter.sort();
}