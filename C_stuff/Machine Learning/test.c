#include <stdio.h>
#include <stdlib.h>


void display(double **arr, int *dims, int num_dims)
{
    if (num_dims == 1)
    {
        for (int i = 0; i < *dims; i++)
        {
            printf("%4.2lf", *(*arr + i));
        }
        return;
    }

    else if (num_dims == 2)
    {
        for (int i = 0; i < *dims; i++)
        {
            for (int j = 0; j < *(dims + 1); j++)
            {
                printf("%4.2lf ", *(*(arr + i) + j));
            }
            printf("\n");
        }
        return;
    }

    int *new_dims = malloc((num_dims - 1) * sizeof(int));
    for (int i = 1; i < num_dims; i++)
    {
        *(new_dims + i - 1) = *(dims + i);
    }

    for (int i = 0; i < *dims; i++)
    {
        display(*(arr + i), new_dims, num_dims - 1);
    }
}

int main()
{

    printf("\n");

    const int R1 = 2, C1 = 2, D1 = 2, R2 = 2, C2 = 1;

    double **mat1 = (double **)malloc(R1 * sizeof(double *));
    for (int i = 0; i < R1; i++)
    {
        *(mat1 + i) = (double **)malloc(C1 * sizeof(double *));
        for (int j = 0; j < C1; j++)
        {
            // printf("[%d,%d]: ", i, j);
            // scanf("%lf", &mat1[i][j]);
            *(*(mat1 + i) + j) = (double *)calloc(D1, sizeof(double));
        }
    }
    printf("\n");

    double **mat2 = malloc(R2 * sizeof(double *));
    for (int i = 0; i < R2; i++)
    {
        *(mat2 + i) = malloc(C2 * sizeof(double *));
        for (int j = 0; j < C2; j++)
        {
            printf("[%d,%d] : ", i, j);
            scanf("%lf", &mat2[i][j]);
        }
    }

    int dims[3] = {R1, C1, D1};
    display(mat1, dims, 3);

    // Free up pointers
    for (int i = 0; i < R1; i++)
    {
        free(mat1[i]);
    }
    free(mat1);

    for (int i = 0; i < R2; i++)
    {
        free(mat2[i]);
    }
    free(mat2);

    return 0;
}
