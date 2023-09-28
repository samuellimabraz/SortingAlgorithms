#pragma once

#include "ISortAlgorithm.h"

namespace sorting {
    
template <typename T>
class SelectionSort : public ISortAlgorithm<T> {
public:
    void sort(std::vector<T>& data, int n) override
    {
        int minIndex;
        for (int i = 0; i < n-1; i++)
        {
            minIndex = i;
            for (int j = i+1; j < n; j++)
            {
                if (data[j] < data[minIndex])
                    minIndex = j;
            }
            std::swap(data[minIndex], data[i]);
        }
    }

    std::string getName() const override { return "Selection Sort"; }
};

} // namespace sorting