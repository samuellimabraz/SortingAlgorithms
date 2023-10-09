#pragma once

#include "ISortAlgorithm.h"

namespace sorting {

template <typename T>
class ShellSort : public ISortAlgorithm<T> {
public:
    void sort(std::vector<T>& data, int n) override
    {
        T aux;
        int j, h;
        for (int h = n / 2; h > 0; h /= 2) {
            for (int i = h; i < n; ++i) {
                aux = data[i];
                
                for (j = i; (j >= h) && (data[j-h] > aux); j -= h) 
                    data[j] = data[j-h];
                
                data[j] = aux;
            }
        }
    }

    std::string getName() const override { return "Shell Sort"; }
};

}