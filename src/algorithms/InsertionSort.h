// InsertionSort.h
#pragma once
#include "SortingAlgorithm.h"

namespace sorting {

template <typename T>
class InsertionSort : public SortingAlgorithm<T> {
public:
    void sort(std::vector<T>& data, int n) override {
        int j;
        T aux;

        for (int i = 1; i < n; i++)
        {
            aux = data[i];
            // Laço interno: caminha para trás, deslocando
            // os elementos maiores que o aux
            for (j = i - 1; (j >= 0) && (aux < data[j]); j--)
                data[j+1] = data[j];

            data[j+1] = aux;
        }
    }

    std::string getName() const override { return "Insertion Sort"; }
};

} // namespace sorting