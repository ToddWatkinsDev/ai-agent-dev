#include <iostream>
#include <string>
#include <sstream>
#include <cmath>

using namespace std;

class Calculator {
private:
    double num1, num2;
    char operation;

public:
    // Constructor
    Calculator() : num1(0), num2(0), operation('+') {}

    // Method to get input from user
    void getInput() {
        cout << "\n=== Simple Calculator ===" << endl;
        cout << "Enter first number: ";
        cin >> num1;
        
        cout << "Enter operation (+, -, *, /, ^, s for square root): ";
        cin >> operation;
        
        if (operation != 's') {
            cout << "Enter second number: ";
            cin >> num2;
        }
    }

    // Method to perform calculation
    double calculate() {
        double result = 0;
        
        switch(operation) {
            case '+':
                result = num1 + num2;
                break;
            case '-':
                result = num1 - num2;
                break;
            case '*':
                result = num1 * num2;
                break;
            case '/':
                if (num2 != 0) {
                    result = num1 / num2;
                } else {
                    cout << "Error: Division by zero!" << endl;
                    return 0;
                }
                break;
            case '^':
                result = pow(num1, num2);
                break;
            case 's':
            case 'S':
                if (num1 >= 0) {
                    result = sqrt(num1);
                } else {
                    cout << "Error: Cannot calculate square root of negative number!" << endl;
                    return 0;
                }
                break;
            default:
                cout << "Error: Invalid operation!" << endl;
                return 0;
        }
        
        return result;
    }

    // Method to display result
    void displayResult(double result) {
        cout << "\nResult: " << result << endl;
        cout << "=========================\n" << endl;
    }
};

int main() {
    Calculator calc;
    char continueCalc = 'y';
    
    cout << "\n**** C++ Calculator Application ****" << endl;
    cout << "This calculator was written by an AI agent." << endl;
    
    while (continueCalc == 'y' || continueCalc == 'Y') {
        calc.getInput();
        double result = calc.calculate();
        calc.displayResult(result);
        
        cout << "Do you want to perform another calculation? (y/n): ";
        cin >> continueCalc;
    }
    
    cout << "\nThank you for using the AI-powered calculator!" << endl;
    return 0;
}
