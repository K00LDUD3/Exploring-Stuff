#include <stdio.h>
#include <stdlib.h>
#include <string.h>

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

int main()
{

    int numRows, numCols;
    const char *filename = "Numbers.csv";
    GetCSVDimensions(filename, &numRows, &numCols);
    printf("%s dimensions: %dx%d", filename, numRows, numCols);

    FILE *f = fopen(filename, "r");
    if (f == NULL)
    {
        printf("Error: File Not Found..\nExiting..\n");
        return 1;
    }

    printf("file opened..\n");

    // Get csv file rows and columns

    char buffer[1024];
    int row = 0;
    double **X = (double **)malloc(numRows * sizeof(double *));

    while (fgets(buffer, sizeof(buffer), f))
    {
        *(X + row) = calloc(numCols, sizeof(double));

        char *token = strtok(buffer, ",");
        int col = 0;

        while (token != NULL)
        {
            *(*(X + row) + col) = atof(token);
            printf("[%d,%d]: %.2lf\n", row, col, atof(token));
            token = strtok(NULL, ",");
            col++;
        }

        row++;
    }

    fclose(f);
    return 0;
}