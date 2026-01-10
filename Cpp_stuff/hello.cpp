#include <iostream>
using namespace std;

namespace first
{
    int x = 10;
    // int y = 20;
    // int z = 30;
}

namespace second
{
    int x = 20;
}

int main()
{
    // cout << "Hello World" << endl;
    // cout << "Hello World";

    // char a = 65.9;
    // int b = 20;
    // int c = a + b;
    // cout << a << endl;

    // float a = 2.5;
    // float b = 3.5;
    // float c = a + b;
    // cout << c << endl;

    // string name = "Abhinav";
    // cout << name << endl;
    // // cout << name << endl;

    int x = 0;

    cout << x << endl;
    cout << first::x << endl;
    cout << second::x << endl;

    // second::y = 100;
    cout << second::y << endl;
    return 0;
}