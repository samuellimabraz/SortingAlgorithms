#include <vector>
#include <algorithm>
#include <iostream>
#include <string>
#include <utility>

#include "SortAlgorithm.h"

using sorting::SortingMethod;
using sorting::SortAlgorithm;

template<typename T>
void runTest(SortingMethod method) {
    SortAlgorithm<T> sorter;
    sorter.setSortingMethod(method);

    // Gera dados aleatórios
    std::vector<T> data(1000);
    std::generate(data.begin(), data.end(), rand);

    // Faz uma cópia dos dados e ordena usando std::sort para comparação
    std::vector<T> expectedData = data;
    std::sort(expectedData.begin(), expectedData.end());

    // Ordena os dados usando o algoritmo de ordenação atual
    sorter.sort(data, data.size());

    // Verifica se os dados estão corretamente ordenados
    if (data != expectedData)
        std::cout << "\033[1;31mTest failed for sorting method: " << sorter.getSortingMethodName() << "\033[0m\n";
    else 
        std::cout << "\033[1;32mTest passed for sorting method: \033[0m " << sorter.getSortingMethodName() << "\n";
    
}

template<typename T>
void runAllTests() {
    std::vector<SortingMethod> methods = {
        SortingMethod::BubbleSort,
        SortingMethod::SelectionSort,
        SortingMethod::InsertionSort,
        SortingMethod::ShellSort,
        SortingMethod::MergeSort,
        SortingMethod::QuickSort
    };

    for (auto& method : methods) {
        runTest<T>(method);
    }
    std::cout << "\n";
}

int main() {

    std::cout << "Running tests for \033[1;34mint\033[0m...\n";
    runAllTests<int>();
    std::cout << "Running tests for \033[1;34mdouble\033[0m...\n";
    runAllTests<double>();
    std::cout << "Running tests for \033[1;34mfloat\033[0m...\n";
    runAllTests<float>();
    std::cout << "Running tests for \033[1;34mstring\033[0m...\n";
    runAllTests<std::string>();

    return 0;
}

// g++ -I.\include\ .\test\test.cpp -o .\test\test
