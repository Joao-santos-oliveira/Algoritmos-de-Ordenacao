#ifndef COUNTING_HPP
#define COUNTING_HPP

#include "problema.hpp"
#include <vector>
using namespace std;
class CountingSort : public MetodoOrdenacao {

private:
    int getMaxValor(const vector<int>& list) const;
    void buildVetorFrequencia(vector<int>& list, vector<int>& count, int maxValue) const;
    void rebuildSortedList(vector<int>& list, const vector<int>& count);

public:
    void sort(vector<int> list) override;
};

#endif