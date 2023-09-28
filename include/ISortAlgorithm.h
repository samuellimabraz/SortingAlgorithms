// ISortingAlgorithm.h
#pragma once

#include <vector>
#include <string>

namespace sorting {

/**
 * @brief Interface that defines a contract for sorting algorithms.
 * 
 * @tparam T The type of data to sort.
 */
template <typename T>
class ISortAlgorithm {
public:
    /**
     * @brief Sorts the given data in place.
     * 
     * @param data The data to sort.
     * @param n The number of elements in the data.
     */
    virtual void sort(std::vector<T>& data, int n) = 0;

    /**
     * @brief Gets the name of the sorting algorithm.
     * 
     * @return The name of the sorting algorithm.
     */
    virtual std::string getName() const = 0;
};

} // namespace sorting