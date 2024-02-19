#include <stdio.h>
#include <stdlib.h>

double **Transpose(double **mat, int R, int C)
{
    double **transposed = (double **)malloc(C * sizeof(double *));

    for (int i = 0; i < C; i++)
    {
        *(transposed + i) = calloc(R, sizeof(double));
        for (int j = 0; j < R; j++)
        {
            *(*(transposed + i) + j) = *(*(mat + j) + i);
        }
    }

    // Free(mat, R);

    return transposed;
}

double **create(int R, int C)
{
    double **mat = (double **)malloc(R * sizeof(double *));

    for (int i = 0; i < R; i++)
    {
        *(mat + i) = calloc(C, sizeof(double));

        for (int j = 0; j < C; j++)
        {
            *(*(mat + i) + j) = i * C + j;
        }
    }

    return mat;
}

void displayMatrix(double **mat, int R, int C)
{
    printf("\n");
    for (int i = 0; i < R; i++)
    {
        for (int j = 0; j < C; j++)
        {
            printf("%-6.2lf", *(*(mat + i) + j));
        }
        printf("\n");
    }
}

double **multiply(double **mat1, double **mat2, int R1, int C1, int R2, int C2)
{
    const int R = R1, C = C2;
    double **resultant = (double **)malloc(R * sizeof(double *));
    printf("\nResultant Dimensions: %dx%d\n", R, C);
    for (int i = 0; i < R; i++)
    {
        *(resultant + i) = calloc(C, sizeof(double));
        for (int j = 0; j < C; j++)
        {
            *(*(resultant + i) + j) = i * C + j;
        }
    }

    double dot_sum = 0;
    // double *row = calloc(C1, sizeof(double));
    // double *column = calloc(R2, sizeof(double));

    for (int i = 0; i < R; i++)
    {
        for (int j = 0; j < C; j++)
        {
            dot_sum = 0;
            for (int k = 0; k < R2; k++)
            {
                // printf("%-6.2lf", *(*(mat2 + k) + j));
                // *(column + k) = *(*(mat2 + k) + j);
                // printf("\t%-6.2lf\n", *(*(mat1 + i) + k));
                // *(row + k) = *(*(mat1 + i) + k);
                dot_sum += (*(*(mat2 + k) + j)) * (*(*(mat1 + i) + k));
            }
            // printf("\n\ndot product for [%d,%d]: %.2lf", i, j, dot_sum);
            *(*(resultant + i) + j) = dot_sum;
        }
    }

    // free(row);
    // free(column);

    return resultant;
}

// Free up pointers
void Free(double **mat, int R)
{
    for (int i = 0; i < R; i++)
    {
        free(mat[i]);
    }
    free(mat);
}

int main()
{
    const int R1 = 4, C1 = 3, R2 = 3, C2 = 2;
    double **mat1 = create(R1, C1);
    printf("\n\n\n\nMatrix 1:\n");
    displayMatrix(mat1, R1, C1);
    double **mat2 = create(R2, C2);
    printf("\nMatrix 2:\n");
    displayMatrix(mat2, R2, C2);

    double **resultant = multiply(mat1, mat2, R1, C1, R2, C2);
    printf("Resultant:\n");
    displayMatrix(resultant, R1, C2);

    double **transposed_resultant = Transpose(resultant, R1, C2);
    Free(resultant, C1);
    displayMatrix(transposed_resultant, C2, R1);

    Free(mat1, R1);
    Free(mat2, R2);

    return 0;
}
