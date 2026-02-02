#include <stdio.h>
#include <math.h>

// シグモイド関数: 数値を0~1に押し込める
double sigmoid(double x) {
    return 1.0 / (1.0 + exp(-x));
}

// ReLU関数: 0以下なら0、0より大きければそのまま（今の主流）
double relu(double x) {
    return x > 0 ? x : 0;
}

int main() {
    double test_val = -2.0;
    printf("Input: %.2f -> Sigmoid: %.4f, ReLU: %.4f\n", 
            test_val, sigmoid(test_val), relu(test_val));
    return 0;
}