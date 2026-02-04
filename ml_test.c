#include <stdio.h>

// Number of training data points
#define N 4

int main() {
    // 1. Training Data
    // x = Input, y = Target (Correct Answer)
    // We want the machine to learn the relationship y = 2x
    double x[N] = {1.0, 2.0, 3.0, 4.0};
    double y[N] = {2.0, 4.0, 6.0, 8.0}; 

    // 2. Initialize Parameters
    double w = 0.0; // Weight (Slope)
    double b = 0.0; // Bias (Intercept)

    // Hyperparameters
    double learning_rate = 0.01; // How big of a step to take
    int epochs = 1000;           // Number of times to loop through the data

    printf("Start Training: Initial w=%.2f, b=%.2f\n", w, b);

    // 3. Training Loop (Gradient Descent)
    for (int i = 0; i < epochs; i++) {
        double dw = 0.0; // Gradient for w
        double db = 0.0; // Gradient for b

        // Loop through all data points
        for (int j = 0; j < N; j++) {
            // Forward pass: Calculate prediction
            double predict = w * x[j] + b;
            
            // Calculate Error: (Prediction - Target)
            double error = predict - y[j];

            // Accumulate gradients (Derived from Mean Squared Error)
            dw += error * x[j];
            db += error;
        }

        // Average the gradients
        dw = (2.0 / N) * dw;
        db = (2.0 / N) * db;

        // Update parameters (Move opposite to the gradient)
        w = w - learning_rate * dw;
        b = b - learning_rate * db;

        // Print progress every 100 epochs
        if ((i + 1) % 100 == 0) {
            printf("Epoch %d: w=%.4f, b=%.4f\n", i + 1, w, b);
        }
    }

    printf("\nTraining Complete!\n");
    printf("Final Model: y = %.4fx + %.4f\n", w, b);

    // 4. Prediction on new data
    double new_x = 5.0;
    double prediction = w * new_x + b;
    printf("Prediction: If x=%.1f, predicted y is %.2f\n", new_x, prediction);

    return 0;
}