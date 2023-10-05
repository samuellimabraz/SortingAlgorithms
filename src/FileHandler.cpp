
#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <ctime>
#include <stdexcept>

#include "FileHandler.h"

using std::string;
using std::vector;

/**
 * Constructor for FileHandler
 * @param filePath The path to the file to be read
 * @param loadLines Whether or not to load and store the lines of the file
 */
FileHandler::FileHandler(const string& filePath, bool loadLines=true) : filePath(filePath)
{
    setFilePath(filePath);
    if (loadLines) this->loadLines();
}

/**
 * Sets the path to the file to be read
 * @param filePath The path to the file to be read
 */
void FileHandler::setFilePath(const string& filePath) { 
    if (this->endsWithExtension(filePath, ".txt") || this->endsWithExtension(filePath, ".csv"))
        this->filePath = filePath; 
    else
        throw std::invalid_argument("File must be a .txt or .csv file.");
}

/**
 * Writes the given data to the file
 * @param data The data to be written to the file
 * @param append Whether or not to append the data to the file
 * @throws runtime_error if the file cannot be opened
*/
void FileHandler::write(const vector<string>& data, bool append = false)
{
    std::ofstream outputFile(filePath, append ? std::ios_base::app : std::ios_base::out);
    if (!outputFile.is_open())
        throw std::runtime_error("Failed to open the output file for writing.");

    for (const string& line : data)
        outputFile << line << '\n';

    outputFile.close();
    this->loadLines();
}

/**
 * Reads the file and stores each line in the lines vector
 * @throws runtime_error if the file cannot be opened
 */
void FileHandler::loadLines()
{
    std::ifstream file(this->filePath);
    if (!file.is_open())
        throw std::runtime_error("Failed to open file");

    string line;
    int i = 0;
    while (getline(file, line)) 
        if (i++ > 0)
            lines.push_back(line);
    
    file.close();
}

/**
 * Returns the number of lines in the file
 * @return The number of lines in the file
 */
bool FileHandler::endsWithExtension(const std::string& str, const std::string& extension) {
    if (str.length() >= extension.length()) {
        return (str.compare(str.length() - extension.length(), extension.length(), extension) == 0);
    }
    return false;
}
