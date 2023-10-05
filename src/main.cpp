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

/**
 * Sorts the data and writes the sorting method, input size, and execution time to the output file
 * @param data The data to be sorted
 * @param sorter The sorting algorithm to be used
 * @param outputFileHandler The FileHandler object to write the output file
 * @param size The size of the input data
 */
template <typename T>
void sortAndWrite(vector<T>& data, SortAlgorithm<T>& sorter, FileHandler& outputFileHandler, int size) {
    cout << "Starting sort...\n";
    int time, n = 2;
    const vector<T> copyData(data); // Create a copy of the data to be sorted

    // Run the sorting algorithm multiple times, in fast algorithms, to get a more accurate execution time
    if (sorter.getSortingMethod() == SortingMethod::ShellSort || sorter.getSortingMethod() == SortingMethod::MergeSort || sorter.getSortingMethod() == SortingMethod::QuickSort)
        n = 10;

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

/**
 * Runs all sorting algorithms on the given data
 * @param inputFileHandler The FileHandler object to read the input file
 * @param outputFileHandler The FileHandler object to write the output file
 */
template <typename T>
void runAllSortAlgorithms(FileHandler& inputFileHandler, FileHandler& outputFileHandler) {
    SortAlgorithm<T> sorter;
    vector<T> data;

    int total = inputFileHandler.getSize();
    // Increment the size of the input data by 5% each iteration, 20 executions in total
    int increment = total / 20;
    data.reserve(total);

    cout << "Total: " << total << '\n';
    cout << "Increment: " << increment << '\n';

    // Write the header row to the file
    outputFileHandler.write({"Sorting Method,Input Size,Execution Time"}, false);

    // Get all sorting algorithms
    auto algorithms = sorter.getAlgorithms();

    for (const auto& it : algorithms) {
        auto method = it.first;
            
        sorter.setSortingMethod(method);
        cout << "Sorting Method: " << sorter.getSortingMethodName() << '\n';

        for (int size = increment; size <= total; size += increment) {
            data = inputFileHandler.getSlicelines<T>(size);
            cout << "Size: " << size << '\n'; 

            // Call the isolated sorting function
            sortAndWrite(data, sorter, outputFileHandler, size);
        }
    }
}


/**
 * Handles the command line arguments
 * @param argc The number of arguments
 * @param argv The arguments
 * @return The data type to be used (integer or string)
 */
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
    // Disable buffering on stdout and stderr, for use with the Python script
    std::setbuf(stdout, NULL);
    std::setbuf(stderr, NULL);

    try
    {
        int dataType = handleCommandLineArguments(argc, argv);

        FileHandler inputFileHandler(INPUT_FILE_PATH, true);
        FileHandler outputFileHandler(OUTPUT_FILE_PATH, false); 

        cout << "Sorting Algorithm for " << (dataType == INTEGER_TYPE ? "integers" : "strings") << '\n';
        if (dataType == INTEGER_TYPE)
            runAllSortAlgorithms<int>(inputFileHandler, outputFileHandler);
        else if (dataType == STRING_TYPE) 
            runAllSortAlgorithms<string>(inputFileHandler, outputFileHandler);
        
    } catch (const std::exception& e) {
        std::cerr << "Erro no programa principal: " << e.what() << '\n';
        return 1;
    }

    cout << "Programa finalizado com sucesso!\n";

    return 0;
}

