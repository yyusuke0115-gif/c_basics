#include <stdio.h>

// Number of data samples
#define N 4
// Number of features (input variables)
// Here we use 2 features: Study Hours and Sleep Hours
#define FEATURES 2

int main() {
    // 1. Training Data
    // x[sample_index][feature_index]
    // {Study Hours, Sleep Hours}
    double x[N][FEATURES] = {
        {1.0, 5.0},  // Student A: 1h study, 5h sleep (Sleep deprived)
        {2.0, 6.0},  // Student B: 2h study, 6h sleep
        {3.0, 7.0},  // Student C: 3h study, 7h sleep
        {4.0, 8.0}   // Student D: 4h study, 8h sleep (Ideal)
    };

    // Target Data (Test Scores)
    // Higher study and sleep time -> Higher score
    double y[N] = {15.0, 25.0, 35.0, 45.0};

    // 2. Initialize Parameters
    // We need a weight for every feature (w1, w2)
    double w[FEATURES] = {0.0, 0.0};
    double b = 0.0;

    // Hyperparameters
    double learning_rate = 0.01;
    int epochs = 2000; // More epochs because it's more complex

    printf("Start Training: Multiple Regression (Features=%d)\n", FEATURES);

    // 3. Training Loop
    for (int i = 0; i < epochs; i++) {
        double dw[FEATURES] = {0.0, 0.0}; // Gradients for w1, w2
        double db = 0.0;

        // Loop through all data samples
        for (int j = 0; j < N; j++) {
            
            // --- Calculate Prediction (Dot Product) ---
            // predict = w1*x1 + w2*x2 + ... + b
            double predict = b;
            for (int k = 0; k < FEATURES; k++) {
                predict += w[k] * x[j][k];
            }

            // Calculate Error
            double error = predict - y[j];

            // --- Accumulate Gradients ---
            for (int k = 0; k < FEATURES; k++) {
                // Gradient for w[k] += error * input[k]
                dw[k] += error * x[j][k];
            }
            db += error;
        }

        // Update Parameters (Average the gradients)
        for (int k = 0; k < FEATURES; k++) {
            w[k] = w[k] - learning_rate * (2.0 / N * dw[k]);
        }
        b = b - learning_rate * (2.0 / N * db);

        // Print progress
        if ((i + 1) % 400 == 0) {
            printf("Epoch %d: w1=%.2f, w2=%.2f, b=%.2f\n", i + 1, w[0], w[1], b);
        }
    }

    printf("\nTraining Complete!\n");
    printf("Model Formula: y = %.2fx1 + %.2fx2 + %.2f\n", w[0], w[1], b);

    // 4. Prediction on New Data
    // What if someone studies 5 hours and sleeps 8 hours?
    double new_x[FEATURES] = {5.0, 8.0};
    
    double prediction = b;
    for (int k = 0; k < FEATURES; k++) {
        prediction += w[k] * new_x[k];
    }

    printf("Prediction Test: Study %.1fh, Sleep %.1fh -> Predicted Score: %.2f\n", 
           new_x[0], new_x[1], prediction);

    return 0;
}