// MergeSort.h
#pragma once

#include "ISortAlgorithm.h"

namespace sorting {

template <typename T>
class MergeSort : public ISortAlgorithm<T> {
public:
    void sort(std::vector<T>& data, int n) override {
        if (n > 1) {
            int mid = n / 2;
            std::vector<T> left(data.begin(), data.begin() + mid);
            std::vector<T> right(data.begin() + mid, data.end());

            sort(left, mid);
            sort(right, n - mid);

            int i = 0, j = 0, k = 0;
            while (i < mid && j < n - mid) {
                if (left[i] < right[j]) {
                    data[k++] = left[i++];
                } else {
                    data[k++] = right[j++];
                }
            }

            while (i < mid) {
                data[k++] = left[i++];
            }

            while (j < n - mid) {
                data[k++] = right[j++];
            }
        }
    }

    std::string getName() const override { return "Merge Sort"; }
};

} // namespace sorting






