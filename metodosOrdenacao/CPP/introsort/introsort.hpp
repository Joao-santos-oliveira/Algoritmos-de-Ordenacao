#ifndef INTROSORT_H
#define INTROSORT_H

#include <vector>
class IntroSort{
    private:
        vector<int> list;
        void InsertionSort(int left, int right);
        void HeapSort(int left, int right);
        void quickSort(int left, int right, int depthLimit);
        int partition(int left, int right);
    public:
        IntroSort(vector<int> list);
        vector<int> getList();
        void sort();
    
};
void IntroSort(vector<int> list);
#endif /* INTROSORT_H */