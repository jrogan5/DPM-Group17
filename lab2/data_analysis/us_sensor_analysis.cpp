/*
J. Rogan 

Reads a file of data formatted as a column vector and calculates 
the minimum, maximum, mean, and standard deviation of the data. 

*/

#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>
#include <limits>

double calculateMean(const std::vector<double>& data) {
    double sum = 0.0;
    for (double value : data) {
        sum += value;
    }
    return sum / data.size();
}

double calculateStandardDeviation(const std::vector<double>& data, double mean) {
    double sum = 0.0;
    for (double value : data) {
        sum += (value - mean) * (value - mean);
    }
    return std::sqrt(sum / data.size());
}

double min_element(const std::vector<double>& data) {
    double min = std::numeric_limits<double>::max();
    for (double value : data) {
        if (value < min) {
            min = value;
        }
    }
    return min;
}

double max_element(const std::vector<double>& data) {
    double max = 0.0;
    for (double value : data) {
        if (std::isnan(value)) {
            continue;
        }
        if (value > max) {
            max = value;
            std::cout << "Current Max: " << max << std::endl;
        }
    }
    return max;
}

int main() {
    std::string filename;
    std::cout << "Enter the file name: ";
    std::cin >> filename;

    std::ifstream file(filename);
    if (!file.is_open()) {
        std::cerr << "Error opening file: " << filename << std::endl;
        return 1;
    }

    std::vector<double> data;
    double value;
    while (file >> value) {
        data.push_back(value);
    }
    file.close();

    if (data.empty()) {
        std::cerr << "No data found in file: " << filename << std::endl;
        return 1;
    }

    double min = min_element(data);
    double max = max_element(data);
    double mean = calculateMean(data);
    double stddev = calculateStandardDeviation(data, mean);

    std::cout << "Minimum: " << min << std::endl;
    std::cout << "Maximum: " << max << std::endl;
    std::cout << "Mean: " << mean << std::endl;
    std::cout << "Standard Deviation: " << stddev << std::endl;

    return 0;
}