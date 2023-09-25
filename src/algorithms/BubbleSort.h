#pragma once

#include "SortingAlgorithm.h"

namespace sorting {
    
template <typename T>
class BubbleSort : public SortingAlgorithm<T> {
public:
    void sort(std::vector<T>& data, int n) override
    {
        bool swapped;
        for (int i = 0; i < n; i++)
        {   
            swapped = false;
            for (int j = 0; j < n-1-i; j++)
            {
                if (data[j+1] < data[j])
                {
                    swap(data[j], data[j+1]);
                    swapped = true;
                }
            }
            // The data is already sorted
            if (!swapped)
                break;
        }
    }

    std::string getName() const override { return "Bubble Sort"; }
};

} // namespace sorting