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
            int pi = partition(data, low, high);
            quickSort(data, low, pi - 1);
            quickSort(data, pi + 1, high);
        }
    }

    int partition(std::vector<T>& data, int low, int high) {
        T pivot = data[high];
        int i = low - 1;

        for (int j = low; j < high; j++) {
            if (data[j] < pivot) {
                i++;
                std::swap(data[i], data[j]);
            }
        }

        std::swap(data[i + 1], data[high]);
        return i + 1;
    }

    std::string getName() const override { return "Quick Sort"; }
};

} // namespace sorting
