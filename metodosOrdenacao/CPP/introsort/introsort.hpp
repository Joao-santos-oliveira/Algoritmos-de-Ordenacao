#ifndef INTROSORT_H
#define INTROSORT_H

#include "problema.hpp"
#include <vector>
using namespace std;

class IntroSort : public MetodoOrdenacao {
    private:
        void InsertionSort(vector<int>& list, int left, int right);
        void Heapfy(vector<int>& list, int n, int i);
        void HeapSort(vector<int>& list, int left, int right);
        void QuickSort(vector<int>& list, int left, int right, int depthLimit);
        int Partition(vector<int>& list, int left, int right);

    public:
        void sort(vector<int> list) override;
    
};
void intro_sort(vector<int> list);
#endif /* INTROSORT_H */