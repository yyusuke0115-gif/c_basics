#include <stdio.h>

int main() {
    // 2x3の行列（入力データのようなもの）
    double A[2][3] = {
        {1.0, 2.0, 3.0},
        {4.0, 5.0, 6.0}
    };

    // 3x2の行列（重みパラメータのようなもの）
    double B[3][2] = {
        {7.0, 8.0},
        {9.0, 10.0},
        {11.0, 12.0}
    };

    // 結果を格納する2x2の行列
    double C[2][2] = {0};

    // 行列掛け算のアルゴリズム（AIの基本演算）
    for (int i = 0; i < 2; i++) {
        for (int j = 0; j < 2; j++) {
            for (int k = 0; k < 3; k++) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }

    // 結果表示
    printf("Result matrix:\n");
    for (int i = 0; i < 2; i++) {
        for (int j = 0; j < 2; j++) {
            printf("%f ", C[i][j]);
        }
        printf("\n");
    }

    return 0;
}