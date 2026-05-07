#ifndef COUNTING_HPP
#define COUNTING_HPP

#include <vector>
using namespace std;
class CountingSort {

private:
    vector<int> list;
    int getMaxValor() const;
    void buildVetorFrequencia(vector<int>& count, int maxValue) const;
    void rebuildSortedList(const vector<int>& count);

public:
    CountingSort(vector<int> list);
    vector<int> getList();
    void sort();
};

void counting_sort(vector<int> list);

#endif