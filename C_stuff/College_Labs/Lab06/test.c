#include <stdio.h>

int main()
{

    int n;
    char c;

    scanf("%d", &n);

    c = n + '0';
    printf("%c\n", c);
    int a = (int)c - 48;
    printf("int->char->int%d\n", a);

    c -= '0';
    printf("%d\n", c);

    return 0;
}