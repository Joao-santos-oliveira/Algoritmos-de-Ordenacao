#ifndef COUNTING_HPP
#define COUNTING_HPP

#include <vector>

class CountingSort {

private:
    std::vector<int> list;

    int getMaxValue() const;
    void buildFrequencyVector(std::vector<int>& count, int maxValue) const;
    void rebuildSortedList(const std::vector<int>& count);

public:
    CountingSort(std::vector<int> list);

    std::vector<int> getList();

    void sort();
};

void counting_sort(std::vector<int> list);

#endif