#include <iostream>
#include <vector>

#include "counting.hpp"

using namespace std;

CountingSort::CountingSort(vector<int> list)
    : list(list) {}

vector<int> CountingSort::getList() {
    return this->list;
}

int CountingSort::getMaxValue() const {

    int maxValue = list[0];

    for (size_t i = 1; i < list.size(); i++) {

        if (list[i] > maxValue) {
            maxValue = list[i];
        }
    }

    return maxValue;
}

void CountingSort::buildFrequencyVector(vector<int>& count, int maxValue) const {

    for (size_t i = 0; i < list.size(); i++) {
        count[list[i]]++;
    }
}

void CountingSort::rebuildSortedList(const vector<int>& count) {

    vector<int> frequency = count;

    size_t index = 0;

    for (size_t value = 0; value < frequency.size(); value++) {

        while (frequency[value] > 0) {

            list[index] = static_cast<int>(value);

            index++;

            frequency[value]--;
        }
    }
}

void CountingSort::sort() {

    if (list.empty()) {
        return;
    }

    int maxValue = getMaxValue();

    vector<int> count(maxValue + 1, 0);

    buildFrequencyVector(count, maxValue);

    rebuildSortedList(count);
}

void counting_sort(vector<int> list) {

    CountingSort sorter(list);

    sorter.sort();
}