#pragma once

#include "ISortAlgorithm.h"

namespace sorting {
    
template <typename T>
class SelectionSort : public ISortAlgorithm<T> {
public:
    void sort(std::vector<T>& data, int n) override
    {
        int minIndex, maxIndex;
        for (int start = 0, end = n-1; start < end; start++, end--)
        {
            minIndex = maxIndex = start;
            for (int i = start; i <= end; i++)
            {
                if (data[i] > data[maxIndex])
                    maxIndex = i;
                if (data[i] < data[minIndex])
                    minIndex = i;
            }
            std::swap(data[start], data[minIndex]); // Coloca o menor elemento no início
            
            if(maxIndex == start) // Se o máximo estava na posição inicial, ele foi trocado com o mínimo
                maxIndex = minIndex;

            std::swap(data[end], data[maxIndex]); // Coloca o maior elemento no final
        }
    }

    std::string getName() const override { return "Selection Sort"; }
};

} // namespace sorting