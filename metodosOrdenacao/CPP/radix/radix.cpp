#include <vector>
#include <algorithm>

#include "radix.hpp"
#include <iostream>

using namespace std;

int RadixSort::getMaxValue(const vector<int>& list) const {

    int maxValue = list[0];

    for (size_t i = 1; i < list.size(); i++) {

        if (list[i] > maxValue) {
            maxValue = list[i];
        }
    }

    return maxValue;
}

void RadixSort::sort(vector<int> list) {

    if (list.empty()) {
        return;
    }
    int maxValue = getMaxValue(list);

    vector<int> auxiliaryList(list.size());

    vector<int> count(10, 0);

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

        list = auxiliaryList;

        exponent *= 10;
    }
}