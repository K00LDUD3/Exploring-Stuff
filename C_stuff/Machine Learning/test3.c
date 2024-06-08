#include <stdio.h>

int main()
{
    float x = 0.00f;
    for (int i = 0; i < 6; i++)
    {
        x += 0.5;
        float y = 0.8647 * x + 0.2923;
        printf("%f , %f\n", x, y);
    }
}