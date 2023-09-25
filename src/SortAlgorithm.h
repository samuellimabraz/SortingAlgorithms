#pragma once
#include <map>
#include <memory>
#include <string>
#include <vector>
#include <ctime>

#include "algorithms\SortingAlgorithm.h"
#include "algorithms\BubbleSort.h"
#include "algorithms\SelectionSort.h"
#include "algorithms\InsertionSort.h"

namespace sorting {

enum class SortingMethod {
    BubbleSort = 0,
    SelectionSort = 1,
    InsertionSort = 2,
    ShellSort = 3,
    MergeSort = 4,
    QuickSort = 5,
};

template <typename T>
class SortAlgorithm
{
    public:
        /**
         * @brief Constructs a new SortAlgorithm object.
         * 
         * @details Initializes the available sorting algorithms and sets the default sorting method to Bubble Sort.
         */
        SortAlgorithm() : algorithms({
            {SortingMethod::BubbleSort, std::make_shared<BubbleSort<T>>()},
            {SortingMethod::SelectionSort, std::make_shared<SelectionSort<T>>()},
            {SortingMethod::InsertionSort, std::make_shared<InsertionSort<T>>()}
        }) , currentMethod(SortingMethod::BubbleSort)
        {
        }

        /**
         * @brief Sorts the given data using the current sorting method and returns the execution time in milliseconds.
         * 
         * @param data The data to sort.
         * @param n The number of elements in the data.
         * @return The execution time in milliseconds.
         */
        int sort(std::vector<T>& data, int n) const
        {  
            auto start = clock();
            // Delegate sorting to the selected algorithm
            algorithms.at(currentMethod)->sort(data, n);
            auto end = clock();
            return (int) ((end - start) * 1000 / CLOCKS_PER_SEC);
        }


        /**
         * @brief Gets the name of the current sorting method.
         * 
         * @return The name of the current sorting method.
         */
        std::string getSortingMethodName() 
        {
            return algorithms.at(currentMethod)->getName();
        }

        /**
         * @brief Sets the current sorting method.
         * 
         * @param method The sorting method to use.
         */
        void setSortingMethod(SortingMethod& method) { currentMethod = method; }

        /**
         * @brief Gets the current sorting method.
         * 
         * @return The current sorting method.
         */
        SortingMethod getSortingMethod() const { return currentMethod; }


        /**
         * @brief Returns the map of available sorting algorithms.
         * 
         * @return The map of available sorting algorithms.
         */
        const std::map<SortingMethod, std::shared_ptr<SortingAlgorithm<T>>>& getAlgorithms() const {
            return algorithms;
        }

    private:
        // Map of available sorting algorithms
        const std::map<SortingMethod, std::shared_ptr<SortingAlgorithm<T>>> algorithms;
        // Current sorting method
        SortingMethod currentMethod;
};

} // namespace sorting