#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <time.h>
#include <math.h>
#include <time.h>

void Free(float **mat, int R)
{
    for (int i = 0; i < R; i++)
    {
        free(mat[i]);
    }
    free(mat);
}

void Log(double error, int epoch)
{
    FILE *file = fopen("count.txt", "r");
    char line[32];
    while (fgets(line, sizeof(line), file) != NULL)
    {
        printf("%s", line);
    }
}

float **Transpose(float **mat, int R, int C)
{
    float **transposed = (float **)malloc(C * sizeof(float *));

    for (int i = 0; i < C; i++)
    {
        *(transposed + i) = calloc(R, sizeof(float));
        for (int j = 0; j < R; j++)
        {
            *(*(transposed + i) + j) = *(*(mat + j) + i);
        }
    }

    // Free(mat, R);

    return transposed;
}

float **Multiply(float **mat1, float **mat2, int R1, int C1, int R2, int C2)
{
    const int R = R1, C = C2;
    float **resultant = (float **)malloc(R * sizeof(float *));
    // printf("\nResultant Dimensions: %dx%d\n", R, C);
    for (int i = 0; i < R; i++)
    {
        *(resultant + i) = calloc(C, sizeof(float));
        for (int j = 0; j < C; j++)
        {
            *(*(resultant + i) + j) = i * C + j;
        }
    }

    float dot_sum = 0;
    // float *row = calloc(C1, sizeof(float));
    // float *column = calloc(R2, sizeof(float));

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

void GetCSVDimensions(const char *filename, int *numRows, int *numCols)
{
    FILE *file = fopen(filename, "r");

    if (file == NULL)
    {
        printf("Error opening file: %s\n", filename);
        return;
    }

    *numRows = 0;
    *numCols = 0;

    int columnsCounted = 0;

    char line[1024]; // Adjust the size based on your CSV file

    // Read each line of the file
    while (fgets(line, sizeof(line), file) != NULL)
    {
        (*numRows)++;

        // Count the number of columns in the current line
        char *token = strtok(line, ",");
        if (columnsCounted)
        {
            continue;
        }
        while (token != NULL)
        {
            (*numCols)++;
            token = strtok(NULL, ",");
        }
        columnsCounted = 1;
    }

    // Close the file
    fclose(file);
}

void displayMatrix(float **mat, int R, int C, const char *msg)
{
    printf("\n%s\n\n", msg);
    printf("[");
    for (int i = 0; i < R; i++)
    {
        printf("[");
        for (int j = 0; j < C; j++)
        {
            printf("%.5lf  ", *(*(mat + i) + j));
        }
        if (i == R - 1)
        {
            printf("]");
        }
        printf("]\n");
    }
}

void displayVector(float *vec, int length, char *msg)
{
    printf("\n%s\n\n", msg);
    for (unsigned int i = 0; i < length; i++)
    {
        printf("%.2lf\n", *(vec + i));
    }
    printf("\n");
}

float randVal(float left, float right)
{
    float randomNumber = sin(rand() * rand());
    return left + (right - left) * fabs(randomNumber);
}

float **Create(const char *filename, int *numRows, int *numCols, bool rand)
{
    //////////////////////////////////////
    //////////////////////////////////////

    if (!rand)
    {
        GetCSVDimensions(filename, numRows, numCols);
        printf("%s dimensions: %dx%d", filename, *numRows, *numCols);
    }

    if (*numRows == 0 || *numCols == 0)
    {
        printf("Invalid Number of Rows and Columns: [%d,%d]\n", *numRows, *numCols);
        return 1;
    }

    //////////////////////////////////////
    //////////////////////////////////////

    float **matrix = (float **)malloc((*numRows) * sizeof(float *));

    if (rand)
    {
        printf("\nRows: %d\nColumns: %d\n", (*numRows), (*numCols));

        for (int i = 0; i < (*numRows); i++)
        {
            *(matrix + i) = calloc((*numCols), sizeof(float));
            for (int j = 0; j < (*numCols); j++)
            {
                *(*(matrix + i) + j) = randVal(0, 5);
            }
        }
        return matrix;
    }

    FILE *f = fopen(filename, "r");
    int row = 0;
    if (f == NULL && !rand)
    {
        printf("Error: File Not Found..\nExiting..\n");
        return 1;
    }

    printf("\nReading %s\n", filename);

    char buffer[1024];

    while (fgets(buffer, sizeof(buffer), f))
    {
        *(matrix + row) = calloc((*numCols), sizeof(float));

        char *token = strtok(buffer, ",");
        int col = 0;

        while (token != NULL)
        {
            *(*(matrix + row) + col) = atof(token);
            // printf("[%d,%d]: %.2lf\n", row, col, atof(token));
            token = strtok(NULL, ",");
            col++;
        }

        row++;
    }

    fclose(f);

    return matrix;
}

void SplitXY(float **matrix, float **X, float *y, const int rows, const int cols)
{
    // printf("\t%d\n", cols - 1);
    for (int i = 0; i < rows; i++)
    {
        *(X + i) = calloc((cols - 1), sizeof(float));
        for (int j = 0; j < cols; j++)
        {
            // printf("J val: %d\n", j);
            if (j < (cols - 1))
            {
                // printf("Reached X assignment block: %d,%d\n", i, j);
                *(*(X + i) + j) = *(*(matrix + i) + j);
            }
            else
            {
                // printf("Reached y assignment block: %d,%d\n", i, j);
                *(y + i) = *(*(matrix + i) + j);
            }
        }
    }
    return;
}

float MeanSquaredError(float *y, float **y_pred, int length)
{
    float error = 0;
    for (int i = 0; i < length; i++)
    {
        // printf("Error for index %d: %f\n", i, (*(y + i) - *(*(y_pred + i))) * (*(y + i) - *(*(y_pred + i))));
        error += (*(y + i) - *(*(y_pred + i))) * (*(y + i) - *(*(y_pred + i)));
    }
    error /= length;
    return error;
}

float DerivativeBias(float *y, float **y_pred, int R, float stepSize, float bias)
{
    float derivative = 0;
    for (int i = 0; i < R; i++)
    {
        derivative += -1 * (*(y + i) - *(*(y_pred + i)));
    }

    derivative /= R / 2;
    return derivative * stepSize;
}

void **AddBias(float **mat1, float bias, int R, int C)
{
    for (int i = 0; i < R; i++)
    {
        for (int j = 0; j < C; j++)
        {
            *(*(mat1 + i) + j) += bias;
        }
    }
}

float *WeightCorrection(float stepSize, float **weights, float *y, float **y_pred, int numXRows, int numXCols, float **X)
{

    float *weight_correction = calloc(numXCols, sizeof(float));

    for (int col = 0; col < numXCols; col++)
    {
        for (int i = 0; i < numXRows; i++)
        {
            *(weight_correction + col) += -2 * (*(*(X + i) + col)) * ((*(y + i)) - (*(*(y_pred + i))));
        }
        *(weight_correction + col) /= numXRows / stepSize;
        // printf("Weight derivative for \'%d\'th weight: %f\n", col, *(weight_correction + col));
    }

    return weight_correction;
}
float R_Squared(float *y, float **y_pred, int rows)
{
    float tss = 0;
    float y_mean = 0;
    for (int i = 0; i < rows; i++)
    {
        y_mean += y[i] / rows;
    }
    for (int i = 0; i < rows; i++)
    {
        tss += (y[i] - y_mean) * (y[i] - y_mean);
    }
    float rss = rows * MeanSquaredError(y, y_pred, rows);

    return 1 - rss / tss;
}
void Epoch(float **weights, float *bias, float stepSize, float **X, float *y, int numXRows, int numXCols, float **y_pred, int *count)
{
    // printf("\n============== [START] Epoch %d ==============\n", *count);

    int numWeightRows = numXCols;
    y_pred = Multiply(X, weights, numXRows, numXCols, numWeightRows, 1);
    AddBias(y_pred, *bias, numXRows, 1);
    // displayMatrix(y_pred, numXRows, 1, "Resultant:");

    float error = MeanSquaredError(y, y_pred, numXRows);
    printf("\nEpoch %d Error <MSE>: %f\n", *count, error);
    printf("R_squared Value: %f", R_Squared(y, y_pred, numXRows));
    float biasCorrection = DerivativeBias(y, y_pred, numXRows, stepSize, *bias);
    // printf("\nBias Derivative: %f\n", biasCorrection);

    float *weightCorrection = WeightCorrection(stepSize, weights, y, y_pred, numXRows, numXCols, X);

    for (int i = 0; i < numXCols; i++)
    {
        // printf("\n%f\n", *(weightCorrection + i));
        *(*(weights + i)) -= *(weightCorrection + i);
    }

    *bias -= biasCorrection;

    // printf("\n============== [END] Epoch ====================\n");

    // printf("\nBias: %f\n", *bias);
    // displayMatrix(weights, numWeightRows, 1, "Weights: ");
    // printf("\n");
    *count += 1;

    return;
}

int main()
{
    srand((unsigned int)time(NULL));
    const char *filename = "Numbers2.csv";
    int numRows, numCols;

    // Getting full csv file
    float **file_matrix = Create(filename, &numRows, &numCols, false);
    // displayMatrix(file_matrix, numRows, numCols, filename);

    // Getting X matrix and y vector
    float **X = malloc((numRows - 1) * sizeof(float *));
    float *y = calloc(numRows, sizeof(float));
    SplitXY(file_matrix, X, y, numRows, numCols);
    // displayVector(y, numRows, "Y VALUES:");
    // displayMatrix(X, numRows, numCols - 1, "X VALUES:");

    // Weights
    int numWeightRows = numCols - 1;
    int numWeightCols = 1;
    float **weights = Create(NULL, &numWeightRows, &numWeightCols, true);
    float **initial_weights = Create(NULL, &numWeightRows, &numWeightCols, true);
    for (int i = 0; i < numWeightRows; i++)
    {
        for (int j = 0; j < numWeightCols; j++)
        {
            *(*(initial_weights + i) + j) = *(*(weights + i) + j);
        }
    }
    // displayMatrix(weights, numWeightRows, 1, "Weights:");

    // Bias
    float bias = randVal(0, 10);
    float initial_bias = bias;
    printf("\nBias: %f\n", bias);

    float **resultant;

    float stepSize = 0.03;

    int count = 1;

    // Epochs
    for (int i = 0; i < 200; i++)
    {
        Epoch(weights, &bias, stepSize, X, y, numRows, numCols - 1, resultant, &count);
    }

    Log(1.111, 1);

    printf("\n\n\n\n\n\nInitial Coefficients:");
    displayMatrix(initial_weights, numCols - 1, 1, "_");
    printf("\nFinal Coefficients:");
    displayMatrix(weights, numCols - 1, 1, "_");

    printf("Initial Bias: %f\nFinal Bias: %f\n", initial_bias, bias);

    Free(resultant, numRows);
    Free(weights, numWeightCols);
    Free(X, numRows);
    Free(file_matrix, numRows);
    return 0;
}
