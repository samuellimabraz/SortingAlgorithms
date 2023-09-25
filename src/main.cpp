#include <iostream>
#include <stdexcept>
#include <string>
#include <memory>
#include <map>
#include <vector>
#include <fstream>

#include "SortAlgorithm.h"
#include "WordManager.h"

using std::cout;
using std::string;
using std::vector;
using sorting::SortAlgorithm;
using sorting::SortingMethod;

// Define the file paths for the input and output files
const string FILE_PATH = "resource\\aurelio40000.txt";
const string OUTPUT_FILE_PATH = "resource\\sorting_times.csv";

int main()
{ 
    try
    {
        WordManager wordManager(FILE_PATH); // Create a WordManager object to manage the input file
        SortAlgorithm<string> sorter; // Create a SortAlgorithm object to perform the sorting
        int time;

        // Create an output file stream to write the sorting times to a CSV file
        //std::ofstream outfile(OUTPUT_FILE_PATH);
        // Write the header row to the file
        //outfile << "Sorting Method,Input Size,Execution Time\n";
    
        // Create vectors of different sizes to sort
        vector<int> sizes = {1000, 5000, 10000, 15000, 20000, 30000, 40000};
        auto algorithms = sorter.getAlgorithms();

        for (auto it = algorithms.begin(); it != algorithms.end(); ++it) {
            auto method = it->first;
            //const auto& algorithm = it->second;
            sorter.setSortingMethod(method);
            cout << "Sorting Method: " << sorter.getSortingMethodName() << '\n';

            // for (int size : sizes) {
            //     vector<string> words = wordManager.getSliceWords(size);
            //     cout << "Tamanho do vetor: " << size << '\n'; 

            //     // Perform the sorting operation and measure the execution time
            //     time = sorter.sort(words, size);
            //     cout << "Execution Time: " << time << " miliseconds" << '\n'; 

            //     // Write the sorting method, input size, and execution time to the output file
            //     //outfile << sorter.getSortingMethodName() << "," << size << "," << time << "\n";
            // }
        }
    
    } catch (const std::exception& e) {
        std::cerr << "Erro no programa principal: " << e.what() << '\n';
        return 1;
    }

    return 0;
}
