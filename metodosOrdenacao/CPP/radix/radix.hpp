#ifndef RADIX_HPP
#define RADIX_HPP

#include "problema.hpp"
#include <vector>

class RadixSort : public MetodoOrdenacao {
    private:
        int getMaxValue(const vector<int>& list) const;

    public:
        void sort(vector<int> list) override;
};

#endif