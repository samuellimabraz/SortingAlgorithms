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

const int INTEGER_TYPE = 1;
const int STRING_TYPE = 2;
string INPUT_FILE_PATH;
string OUTPUT_FILE_PATH;
vector<int> sizes;

template <typename T>
void sortAndWrite(vector<T>& data, SortAlgorithm<T>& sorter, FileHandler& outputFileHandler, int size) {
    // Perform the sorting operation and measure the execution time
    cout << "Starting sort...\n";
    int time = sorter.sort(data, size);
    cout << "Execution Time: " << time << " miliseconds" << '\n'; 

    // Write the sorting method, input size, and execution time to the output file
    outputFileHandler.write( 
        {sorter.getSortingMethodName() + "," + std::to_string(size) + "," + std::to_string(time)}, 
        true
    );
}

template <typename T>
void runAllSortAlgorithms(FileHandler& inputFileHandler, FileHandler& outputFileHandler, vector<int>& sizes) {
    SortAlgorithm<T> sorter;
    vector<T> data;
    data.reserve(*std::max_element(sizes.begin(), sizes.end()));

    // Write the header row to the file
    outputFileHandler.write({"Sorting Method,Input Size,Execution Time"}, false);

    // Create vectors of different sizes to sort
    auto algorithms = sorter.getAlgorithms();

    for (const auto& it : algorithms) {
        auto method = it.first;
            
        sorter.setSortingMethod(method);
        cout << "Sorting Method: " << sorter.getSortingMethodName() << '\n';

        for (int size : sizes) {
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
        OUTPUT_FILE_PATH = "output\\sorting_times_int.csv";
        sizes = {1000, 5000, 10000, 20000, 50000, 100000};
        dataType = INTEGER_TYPE;

    } else if (opt == 's') {
        INPUT_FILE_PATH = "resource\\aurelio40000.txt";
        OUTPUT_FILE_PATH = "output\\sorting_times_string.csv";
        sizes = {1000, 5000, 10000, 15000, 20000, 30000, 40000};
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
            runAllSortAlgorithms<int>(inputFileHandler, outputFileHandler, sizes);
        } else if (dataType == STRING_TYPE) {
            runAllSortAlgorithms<string>(inputFileHandler, outputFileHandler, sizes);
        }

    } catch (const std::exception& e) {
        std::cerr << "Erro no programa principal: " << e.what() << '\n';
        return 1;
    }

    return 0;
}

