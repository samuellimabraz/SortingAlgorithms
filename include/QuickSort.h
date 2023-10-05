// QuickSort.h
#pragma once

#include "ISortAlgorithm.h"

namespace sorting {

template <typename T>
class QuickSort : public ISortAlgorithm<T> {
public:
    void sort(std::vector<T>& data, int n) override {
        quickSort(data, 0, n - 1);
    }

    void quickSort(std::vector<T>& data, int low, int high) {
        if (low < high) {
            int pivot = partition(data, low, high);
            quickSort(data, low, pivot - 1);
            quickSort(data, pivot + 1, high);
        }
    }

    int partition(std::vector<T>& data, int low, int high) {
        T pivot = data[low];
        int i = low, j = high;

        while(i < j)
        {
            while((data[i] <= pivot) && (i < high))
                i++;
            while((data[j] >= pivot) && (j > low))
                j--;

            if(i < j)
                std::swap(data[i], data[j]);
        }
        std::swap(data[low], data[j]);
        return j;
    }

    std::string getName() const override { return "Quick Sort"; }
};

} // namespace sorting
