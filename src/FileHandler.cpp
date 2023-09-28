
#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <ctime>
#include <stdexcept>

#include "FileHandler.h"

using std::string;
using std::vector;

FileHandler::FileHandler(const string& filePath, bool load=true) : filePath(filePath)
{
    setFilePath(filePath);
    if (load) loadLines();
}

void FileHandler::setFilePath(const string& filePath) { 
    if (this->endsWithExtension(filePath, ".txt") || this->endsWithExtension(filePath, ".csv"))
        this->filePath = filePath; 
    else
        throw std::invalid_argument("File must be a .txt or .csv file.");
}

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

void FileHandler::loadLines()
{
    std::ifstream file(this->filePath);
    if (!file.is_open())
        throw std::runtime_error("Failed to open file");

    string line;
    while (getline(file, line)) 
        lines.push_back(line);
    
    file.close();
}

bool FileHandler::endsWithExtension(const std::string& str, const std::string& extension) {
    if (str.length() >= extension.length()) {
        return (str.compare(str.length() - extension.length(), extension.length(), extension) == 0);
    }
    return false;
}
