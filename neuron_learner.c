#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

// Activation function: Sigmoid
double sigmoid(double x) {
    return 1.0 / (1.0 + exp(-x));
}

// Derivative of sigmoid: Used for calculating the "error gradient"
double sigmoid_derivative(double x) {
    return x * (1.0 - x);
}

int main() {
    srand((unsigned int)time(NULL));

    // Training Data (OR Gate)
    double inputs[4][2] = {{0,0}, {0,1}, {1,0}, {1,1}};
    double targets[4] = {0, 1, 1, 1};

    // AI's "Brain": 2 weights and 1 bias
    double w1 = (double)rand() / RAND_MAX;
    double w2 = (double)rand() / RAND_MAX;
    double bias = (double)rand() / RAND_MAX;

    double learning_rate = 0.1;
    int epochs = 10000; // How many times to practice

    printf("Starting training...\n");

    // Training Loop
    for (int i = 0; i < epochs; i++) {
        for (int j = 0; j < 4; j++) {
            // 1. Forward Pass (Prediction)
            double sum = inputs[j][0] * w1 + inputs[j][1] * w2 + bias;
            double prediction = sigmoid(sum);

            // 2. Calculate Error
            double error = targets[j] - prediction;

            // 3. Backward Pass (Gradient Descent / Adjustment)
            // This is where the AI "learns" by adjusting weights
            double gradient = error * sigmoid_derivative(prediction);
            
            w1 += gradient * inputs[j][0] * learning_rate;
            w2 += gradient * inputs[j][1] * learning_rate;
            bias += gradient * learning_rate;
        }
    }

    printf("Training complete!\n\n");

    // Test the trained AI
    printf("Test Results:\n");
    for (int i = 0; i < 4; i++) {
        double sum = inputs[i][0] * w1 + inputs[i][1] * w2 + bias;
        double result = sigmoid(sum);
        printf("In: %.0f, %.0f | Target: %.0f | AI Prediction: %.4f\n", 
               inputs[i][0], inputs[i][1], targets[i], result);
    }

    return 0;
}