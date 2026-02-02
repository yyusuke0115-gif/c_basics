#include <stdio.h>
#include <stdlib.h>
#include <time.h>

/**
 * Creates a 2D matrix (array of pointers) with random initial weights.
 * @param rows Number of rows
 * @param cols Number of columns
 * @return Pointer to the allocated matrix
 */
double** create_matrix(int rows, int cols) {
    // 1. Allocate memory for the row pointers
    double **m = (double **)malloc(rows * sizeof(double *));
    if (m == NULL) return NULL; // Safety check

    for (int i = 0; i < rows; i++) {
        // 2. Allocate memory for the actual data in each row
        m[i] = (double *)malloc(cols * sizeof(double));
        
        // 3. Initialize with small random weights (essential for AI)
        for (int j = 0; j < cols; j++) {
            m[i][j] = (double)rand() / RAND_MAX * 0.1;
        }
    }
    return m;
}

/**
 * Frees the memory allocated for the matrix.
 */
void free_matrix(double **m, int rows) {
    for (int i = 0; i < rows; i++) {
        free(m[i]);
    }
    free(m);
}

int main() {
    srand((unsigned int)time(NULL));

    int rows = 3;
    int cols = 4;

    // Build the AI's "brain" structure
    double **weights = create_matrix(rows, cols);

    if (weights == NULL) {
        printf("Memory allocation failed!\n");
        return 1;
    }

    printf("Successfully created a %dx%d weight matrix:\n", rows, cols);
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            printf("%.4f ", weights[i][j]);
        }
        printf("\n");
    }

    // Always clean up your memory!
    free_matrix(weights, rows);
    printf("Memory freed successfully.\n");

    return 0;
}