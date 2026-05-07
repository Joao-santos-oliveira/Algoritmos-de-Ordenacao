#include <vector>
#include <algorithm>

#include "radix.hpp"

using namespace std;

RadixSort::RadixSort(vector<int>& list)
    : list(list) {}

int RadixSort::getMaxValue() const {

    int maxValue = list[0];

    for (size_t i = 1; i < list.size(); i++) {

        if (list[i] > maxValue) {
            maxValue = list[i];
        }
    }

    return maxValue;
}

void RadixSort::sort() {

    if (list.empty()) {
        return;
    }

    int maxValue = getMaxValue();

    vector<int> auxiliaryList(list.size());

    vector<int> count(10);

    int exponent = 1;

    while (maxValue / exponent > 0) {

        fill(count.begin(), count.end(), 0);

        for (size_t i = 0; i < list.size(); i++) {

            int digit = (list[i] / exponent) % 10;

            count[digit]++;
        }

        for (size_t i = 1; i < count.size(); i++) {

            count[i] += count[i - 1];
        }

        for (int i = (int)list.size() - 1; i >= 0; i--) {

            int digit = (list[i] / exponent) % 10;

            auxiliaryList[count[digit] - 1] = list[i];

            count[digit]--;
        }

        for (size_t i = 0; i < list.size(); i++) {

            list[i] = auxiliaryList[i];
        }

        exponent *= 10;
    }
}

void radix_sort(vector<int> list) {

    RadixSort sorter(list);

    sorter.sort();
}