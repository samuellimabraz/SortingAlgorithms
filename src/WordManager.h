#ifndef WORDMANAGER_H
#define WORDMANAGER_H

#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <random>
#include <ctime>
#include <stdexcept>

using std::string;
using std::vector;

class WordManager
{
    public:
        /**
         * @brief Constructs a new WordManager object.
         * 
         * @param filename The name of the file containing the words.
         * @throws std::runtime_error if the file cannot be opened.
         */
        WordManager(const string& filename)
        {
            try 
            {
                this->filename = filename;
                loadWords();
            }
            catch (const std::exception& e)
            {
                std::cerr << "Exception: " << e.what() << '\n';
            }

        }

        /**
        * @brief Loads the words from the file.
        * 
        * @throws std::runtime_error if the file cannot be opened.
        */
        void loadWords()
        {
            std::ifstream file(this->filename);
            if (!file.is_open())
                throw std::runtime_error("Failed to open file");

            string word;
            while (getline(file, word)) 
                words.push_back(word);
            
            file.close();
        }

        /**
         * @brief Gets a slice of the words.
         * 
         * @param size The number of words to return.
         * @return A vector containing the first 'size' words.
         */
        vector<string> getSliceWords(int size) 
        {
            int totalWords = words.size();

            // If size is greater than or equal to the total number of words, return all the words.
            if (size >= totalWords) 
                return words;

            // Criando iteradores para os índices de início e fim
            vector<string>::iterator startIterator = words.begin();
            vector<string>::iterator endIterator = words.begin() + size;
            
            return vector<string>(startIterator, endIterator);
        }

    private:
        vector<string> words;
        string filename;
};

#endif // WORDMANAGER_H