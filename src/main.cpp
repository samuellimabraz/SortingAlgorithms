#include <algorithm>
#include <getopt.h>
#include <iostream>
#include <stdexcept>
#include <string>
#include <memory>
#include <map>
#include <vector>
#include <fstream>

#include "SortAlgorithm.h"
#include "FileHandler.h"

using std::cout;
using std::string;
using std::vector;
using sorting::SortAlgorithm;
using sorting::SortingMethod;

const int INTEGER_TYPE = 1;
const int STRING_TYPE = 2;
string INPUT_FILE_PATH;
string OUTPUT_FILE_PATH;

template <typename T>
void sortAndWrite(vector<T>& data, SortAlgorithm<T>& sorter, FileHandler& outputFileHandler, int size) {
    // Perform the sorting operation and measure the execution time
    cout << "Starting sort...\n";
    int time, n;
    const vector<T> copyData(data);

    if (sorter.getSortingMethod() == SortingMethod::ShellSort || sorter.getSortingMethod() == SortingMethod::MergeSort || sorter.getSortingMethod() == SortingMethod::QuickSort) {
        n = 10;
    } else {
        n = 2;
    }

    for (int i = 0; i < n; i++) {
        time += sorter.sort(data, size);
        data = copyData;
    }
    time /= n;
    
    cout << "Execution Time: " << time << " miliseconds" << '\n'; 

    // Write the sorting method, input size, and execution time to the output file
    outputFileHandler.write( 
        {sorter.getSortingMethodName() + "," + std::to_string(size) + "," + std::to_string(time)}, 
        true
    );
}

template <typename T>
void runAllSortAlgorithms(FileHandler& inputFileHandler, FileHandler& outputFileHandler) {
    SortAlgorithm<T> sorter;
    vector<T> data;

    int total = inputFileHandler.getSize();
    int increment = total / 20;
    data.reserve(total);

    cout << "Total: " << total << '\n';
    cout << "Increment: " << increment << '\n';

    // Write the header row to the file
    outputFileHandler.write({"Sorting Method,Input Size,Execution Time"}, false);

    // Create vectors of different sizes to sort
    auto algorithms = sorter.getAlgorithms();

    for (const auto& it : algorithms) {
        auto method = it.first;
            
        sorter.setSortingMethod(method);
        cout << "Sorting Method: " << sorter.getSortingMethodName() << '\n';

        for (int size = increment; size < total; size += increment) {
            data = inputFileHandler.getSlicelines<T>(size);
            cout << "Size: " << size << '\n'; 

            // Call the isolated sorting function
            sortAndWrite(data, sorter, outputFileHandler, size);
        }
    }
}

int handleCommandLineArguments(int argc, char *argv[]) {
    int dataType;

    int opt = getopt(argc, argv, "is");
    if (opt == 'i') {
        INPUT_FILE_PATH = "resource\\numbers.csv";
        OUTPUT_FILE_PATH = "output\\times\\sorting_times_int.csv";
        dataType = INTEGER_TYPE;

    } else if (opt == 's') {
        INPUT_FILE_PATH = "resource\\aurelio40000.txt";
        OUTPUT_FILE_PATH = "output\\times\\sorting_times_string.csv";
        dataType = STRING_TYPE;
    } else {
        throw std::invalid_argument("Usage: [-i] [-s]");
    }

    return dataType;
}

int main(int argc, char *argv[])
{ 
    std::setbuf(stdout, NULL);
    std::setbuf(stderr, NULL);

    try
    {
        // Handle command line arguments
        int dataType = handleCommandLineArguments(argc, argv);

        FileHandler inputFileHandler(INPUT_FILE_PATH, true); // Create a FileHandler object to read the input file
        FileHandler outputFileHandler(OUTPUT_FILE_PATH, false); // Create a FileHandler object to write the output file

        cout << "Sorting Algorithm for " << (dataType == INTEGER_TYPE ? "integers" : "strings") << '\n';
        if (dataType == INTEGER_TYPE) {
            runAllSortAlgorithms<int>(inputFileHandler, outputFileHandler);
        } else if (dataType == STRING_TYPE) {
            runAllSortAlgorithms<string>(inputFileHandler, outputFileHandler);
        }

    } catch (const std::exception& e) {
        std::cerr << "Erro no programa principal: " << e.what() << '\n';
        return 1;
    }

    cout << "Programa finalizado com sucesso!\n";

    return 0;
}

