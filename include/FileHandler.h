#pragma once

#include <algorithm>
#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <ctime>
#include <stdexcept>

using std::string;
using std::vector;

/**
* @brief A class for reading and writing to files.
*
* The file must have a .txt or .csv extension.
*/
class FileHandler
{
    public:
        /**
         * @brief Constructs a new FileHandler object.
         * 
         * @param filePath The name of the file containing the lines.
         * @throws std::runtime_error if the file cannot be opened.
         */
        FileHandler(const string&, bool);

        /**
         * @brief Sets the file path.
         * 
         * @param filePath The name of the file containing the lines.
         * @throws std::invalid_argument if the file does not have a .txt or .csv extension.
        */
        void setFilePath(const string& filePath);

        /**
         * @brief Gets the file path.
         * 
         * @return The name of the file containing the lines.
        */
        std::string getFilePath() const { return filePath; }

        /**
         * @brief Writes the given lines to the file.
         * 
         * @param data The lines to write to the file.
         * @param append If true, the lines will be appended to the end of the file. Otherwise, the file will be overwritten.
         * @throws std::runtime_error if the file cannot be opened.
        */
        void write(const vector<string>&, bool);

        /**
         * @brief Gets n (size) lines from the file.
         * 
         * @param size The number of lines to get from the file.
         * @return A vector<T> containing the lines from the file.
         * @throws std::invalid_argument if size is less than or equal to 0.
         * 
         * @tparam T The type of data to return.
         * @details The type of data returned depends on the template parameter.
        */
        template <typename T>
        vector<T> getSlicelines(int size) {
            // If size is greater than or equal to the total number of lines, return all the lines.
            if (size >= lines.size()) 
                size = lines.size();
            else if (size <= 0)
                throw std::invalid_argument("Size must be greater than 0.");
            
            vector<T> data;
            data.reserve(size);
            
            std::transform(lines.begin(), lines.begin() + size, std::back_inserter(data),
                [](const string& str){
                    if constexpr (std::is_same<T, int>::value) {
                        return std::stoi(str);
                    } else if constexpr (std::is_same<T, float>::value) {
                        return std::stof(str);
                    } else if constexpr (std::is_same<T, double>::value) {
                        return std::stod(str);
                    } else if constexpr (std::is_same<T, string>::value) {
                        return str;
                    }
                }
            );

            return data;
        }

        int getSize() const { return lines.size(); }

    private:
        vector<string> lines;
        string filePath;

        /**
        * @brief Loads the lines from the file.
        * 
        * @throws std::runtime_error if the file cannot be opened.
        */
        void loadLines();

        bool endsWithExtension(const std::string& str, const std::string& extension);
};