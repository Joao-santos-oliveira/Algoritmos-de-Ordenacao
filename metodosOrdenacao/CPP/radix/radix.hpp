#ifndef RADIX_HPP
#define RADIX_HPP

#include <vector>

class RadixSort {

private:
    std::vector<int>& list;

    int getMaxValue() const;

public:
    RadixSort(std::vector<int>& list);

    void sort();
};

void radix_sort(std::vector<int> list);

#endif