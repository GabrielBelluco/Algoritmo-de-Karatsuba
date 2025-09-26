#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef unsigned char digit; 

#define MIN_CARACTERES_KARATSUBA 32

/* ---- Prototipos ---- */
void ler_numero(int num_digitos, digit *A);
void imprimir_sem_zeros(const digit *C, int len);
void soma_vec(int len_A, const digit *A, int len_B, const digit *B, int len_C, digit *C);
void sub_vec (int len_A, const digit *A, int len_B, const digit *B, int len_C, digit *C);
void mult_trad(int num_digitos, const digit *A, const digit *B, int result_len, digit *C);
void somar_com_deslocamento10(digit *C, int len_C, const digit *X, int len_X, int shift);
void karatsuba(int num_digitos, const digit *A, const digit *B, int result_len, digit *C);

int main(void) {
    int num_digitos;
    if (scanf("%d", &num_digitos) != 1) return 0;
    getchar();

    digit *X = malloc(num_digitos * sizeof(digit));
    digit *Y = malloc(num_digitos * sizeof(digit));
    digit *Z = calloc(2 * num_digitos, sizeof(digit));
  if (!X || !Y || !Z) {
        fprintf(stderr, "Erro de memória\n");
        return 1;
    }

    ler_numero(num_digitos, X);
    ler_numero(num_digitos, Y);

    karatsuba(num_digitos, X, Y, 2 * num_digitos, Z);
    imprimir_sem_zeros(Z, 2 * num_digitos);

    free(X); free(Y); free(Z);
    return 0;
}

/* Lê exalen_ente n dígitos '0'..'9' (MSB->LSB em A[0..num_digitos-1]) */
void ler_numero(int num_digitos, digit *A) {
    for (int i = 0; i < num_digitos; i++) {
        int ch = getchar();
        while (ch == '\r' || ch == '\n') ch = getchar();
        A[i] = (digit)(ch - '0');
    }
    int ch;
    while ((ch = getchar()) != EOF && ch != '\n'); /* descarta resto da linha */
}

/* Imprime sem zeros à esquerda (ex.: 00056088 -> 56088) */
void imprimir_sem_zeros(const digit *C, int len) {
    int i = 0;
    while (i < len && C[i] == 0) i++;
    if (i == len) { puts("0"); return; }
    for (; i < len; i++) printf("%u", (unsigned)C[i]);
    putchar('\n');
}

/* Soma A+B -> C (todos MSB->LSB). len_C >= max(len_A, len_B)+1 */
void soma_vec(int len_A, const digit *A, int len_B, const digit *B, int len_C, digit *C) {
    int ia = len_A - 1, ib = len_B - 1, ic = len_C - 1, carry = 0;
    while (ic >= 0) {
        int va = (ia >= 0) ? A[ia--] : 0;
        int vb = (ib >= 0) ? B[ib--] : 0;
        int result = va + vb + carry;
        C[ic--] = (digit)(result % 10);
        carry = result / 10;
    }
}

/* Subtrai A-B -> C (A >= B), todos MSB->LSB */
void sub_vec(int len_A, const digit *A, int len_B, const digit *B, int len_C, digit *C) {
    int ia = len_A - 1, ib = len_B - 1, ic = len_C - 1, borrow = 0;
    while (ic >= 0) {
        int va = (ia >= 0) ? A[ia--] : 0;
        int vb = (ib >= 0) ? B[ib--] : 0;
        int result = va - vb - borrow;
        if (result < 0) { result += 10; borrow = 1; } else borrow = 0;
        C[ic--] = (digit)result;
    }
}

/* Multiplicação tradicional O(n^2): A(num_digitos)*B(num_digitos) -> C(2*num_digitos) */
void mult_trad(int num_digitos, const digit *A, const digit *B, int result_len, digit *C) {
    for (int i = 0; i < result_len; i++) C[i] = 0;

    for (int ib = num_digitos - 1; ib >= 0; ib--) {
        int carry = 0;
        for (int ia = num_digitos - 1; ia >= 0; ia--) {
            int desloca = (num_digitos - 1 - ia) + (num_digitos - 1 - ib);
            int pos = (result_len - 1) - desloca;
            int result = C[pos] + A[ia] * B[ib] + carry;
            C[pos] = (digit)(result % 10);
            carry = result / 10;
        }
        int pos = (result_len - 1) - ((num_digitos - 1) + (num_digitos - 1 - ib)) - 1;
        while (carry > 0 && pos >= 0) {
            int result = C[pos] + carry;
            C[pos] = (digit)(result % 10);
            carry = result / 10;
            pos--;
        }
    }
}

/* Soma X * 10^shift dentro de C, alinhanum_digitoso pelo LSB */
void somar_com_deslocamento10(digit *C, int len_C, const digit *X, int len_X, int shift) {
    int iC = len_C - 1 - shift, iX = len_X - 1, carry = 0;
    while ((iX >= 0 || carry > 0) && iC >= 0) {
        int result = C[iC] + (iX >= 0 ? X[iX] : 0) + carry;
        C[iC] = (digit)(result % 10);
        carry = result / 10;
        iX--; iC--;
    }
}

/* Karatsuba com caso-base tradicional */
void karatsuba(int num_digitos, const digit *A, const digit *B, int result_len, digit *C) {
    if (num_digitos <= 0) return;
    if (num_digitos <= MIN_CARACTERES_KARATSUBA) {
        mult_trad(num_digitos, A, B, result_len, C);
        return;
    }

    int low_len  = num_digitos / 2;
    int high_len = num_digitos - low_len;

    const digit *A_high = A;
    const digit *A_low = A + high_len;
    const digit *B_high = B;
    const digit *B_low = B + high_len;

    digit *prod_low = calloc(2 * low_len,  sizeof(digit));
    digit *prod_high = calloc(2 * high_len, sizeof(digit));
    int s = (low_len > high_len ? low_len : high_len) + 1;
    digit *a_sum = calloc(s, sizeof(digit));
    digit *b_sum = calloc(s, sizeof(digit));
    digit *sum_prod = calloc(2 * s, sizeof(digit));
    digit *prod_mid = calloc(2 * s, sizeof(digit));
    digit *buf = calloc(2 * s, sizeof(digit));
    if (!prod_low || !prod_high || !a_sum || !b_sum || !sum_prod || !prod_mid || !buf) {
        fprintf(stderr, "memoria insuficiente\n");
        exit(1);
    }

    karatsuba(low_len,  A_low,  B_low,  2 * low_len,  prod_low);
    karatsuba(high_len, A_high,  B_high,  2 * high_len, prod_high);

    soma_vec(low_len, A_low,  high_len, A_high,  s, a_sum);
    soma_vec(low_len, B_low,  high_len, B_high,  s, b_sum);
    karatsuba(s, a_sum, b_sum, 2 * s, sum_prod);

    /* prod_mid = sum_prod - prod_low - prod_high (todos alinhados à direita em 2*s) */
    memset(buf, 0, 2 * s);
    memcpy(buf + (2 * s - 2 * low_len),  prod_low, 2 * low_len);
    sub_vec(2 * s, sum_prod, 2 * s, buf, 2 * s, prod_mid);

    memset(buf, 0, 2 * s);
    memcpy(buf + (2 * s - 2 * high_len), prod_high, 2 * high_len);
    sub_vec(2 * s, prod_mid, 2 * s, buf, 2 * s, prod_mid);

    /* C = prod_high * 10^(2*low_len) + prod_mid * 10^(low_len) + prod_low */
    for (int i = 0; i < result_len; i++) C[i] = 0;
    somar_com_deslocamento10(C, result_len, prod_low, 2 * low_len,   0);
    somar_com_deslocamento10(C, result_len, prod_mid, 2 * s,         low_len);
    somar_com_deslocamento10(C, result_len, prod_high, 2 * high_len,  2 * low_len);

    free(prod_low); free(prod_high); free(a_sum); free(b_sum); free(sum_prod); free(prod_mid); free(buf);
}