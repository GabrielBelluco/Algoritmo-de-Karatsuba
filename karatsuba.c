#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* Representamos cada número como vetor de dígitos decimais (0..9),
   com o dígito mais significativo (MSB) em A[0] e o menos significativo (LSB) em A[n-1]. */

typedef signed char digit;

/* ----------------------- Assinaturas ----------------------- */
static void read_number(int n, digit *A);
static void print_number_trim(const digit *C, int m);

static void add_vec(int a, const digit *A, int b, const digit *B, int c, digit *C);
static void sub_vec(int a, const digit *A, int b, const digit *B, int c, digit *C); /* supõe A >= B */

static void tradicional_multi(int n, const digit *A, const digit *B, int m, digit *C);
static void karatsuba(int n, const digit *A, const digit *B, int m, digit *C);

static void add_into_shift10(digit *C, int m, const digit *X, int len, int shift);

/* ----------------------- Config ----------------------- */
/* Abaixo desse tamanho, usa multiplicação tradicional (O(n^2)).
   Ajuste se quiser, mas 32 é um corte seguro. */
#define KARATSUBA_CUTOFF 32

int main(void) {
    int n;
    if (scanf("%d", &n) != 1) return 0;
    getchar(); /* consome '\n' após o n */

    digit *X = (digit*) malloc(n * sizeof(digit));
    digit *Y = (digit*) malloc(n * sizeof(digit));
    digit *Z = (digit*) calloc(2*n, sizeof(digit)); /* resultado até 2n dígitos */

    if (!X || !Y || !Z) {
        fprintf(stderr, "Erro de memória\n");
        return 1;
    }

    read_number(n, X);
    read_number(n, Y);

    karatsuba(n, X, Y, 2*n, Z);

    print_number_trim(Z, 2*n);

    free(X); free(Y); free(Z);
    return 0;
}

/* -------------------- Leitura e Impressão -------------------- */
static void read_number(int n, digit *A) {
    /* Lê exatamente n caracteres '0'..'9' e guarda como 0..9 */
    for (int i = 0; i < n; i++) {
        int ch = getchar();
        while (ch == '\r' || ch == '\n') ch = getchar(); /* pula quebras de linha inesperadas */
        A[i] = (digit)(ch - '0');
    }
    int ch;
    /* consome até o fim da linha */
    while ((ch = getchar()) != EOF && ch != '\n');
}

static void print_number_trim(const digit *C, int m) {
    int i = 0;
    while (i < m && C[i] == 0) i++;
    if (i == m) { puts("0"); return; }
    for (; i < m; i++) printf("%d", (int)C[i]);
    printf("\n");
}

/* -------------------- Aritmética básica -------------------- */
/* Soma A (a dígitos) + B (b dígitos) -> C (c dígitos).
   Vetores MSB->LSB. c deve ser >= max(a,b)+1. */
static void add_vec(int a, const digit *A, int b, const digit *B, int c, digit *C) {
    int ia = a - 1, ib = b - 1, ic = c - 1;
    int carry = 0;
    while (ic >= 0) {
        int va = (ia >= 0) ? A[ia--] : 0;
        int vb = (ib >= 0) ? B[ib--] : 0;
        int r = va + vb + carry;
        C[ic--] = (digit)(r % 10);
        carry = r / 10;
    }
}

/* Subtração A - B -> C, assumindo A >= B (sem sinal).
   Tamanhos a, b e c informados; saída em C com c dígitos (MSB->LSB). */
static void sub_vec(int a, const digit *A, int b, const digit *B, int c, digit *C) {
    int ia = a - 1, ib = b - 1, ic = c - 1;
    int borrow = 0;
    while (ic >= 0) {
        int va = (ia >= 0) ? A[ia--] : 0;
        int vb = (ib >= 0) ? B[ib--] : 0;
        int r = va - vb - borrow;
        if (r < 0) { r += 10; borrow = 1; } else { borrow = 0; }
        C[ic--] = (digit)r;
    }
}

/* Multiplicação tradicional O(n^2): A(n) * B(n) -> C(m=2n), MSB->LSB. */
static void tradicional_multi(int n, const digit *A, const digit *B, int m, digit *C) {
    /* zera C */
    for (int i = 0; i < m; i++) C[i] = 0;

    /* Acumula de trás pra frente (alinhando LSBs) */
    for (int ib = n - 1; ib >= 0; ib--) {
        int carry = 0;
        for (int ia = n - 1; ia >= 0; ia--) {
            int off_a = (n - 1 - ia);
            int off_b = (n - 1 - ib);
            int pos = (m - 1) - (off_a + off_b);
            int r = C[pos] + A[ia] * B[ib] + carry;
            C[pos] = (digit)(r % 10);
            carry = r / 10;
        }
        int pos = (m - 1) - ((n - 1) + (n - 1 - ib)) - 1; /* posição à esquerda */
        while (carry > 0 && pos >= 0) {
            int r = C[pos] + carry;
            C[pos] = (digit)(r % 10);
            carry = r / 10;
            pos--;
        }
    }
}

/* Soma um bloco X (len dígitos, MSB->LSB) em C (m dígitos, MSB->LSB),
   deslocando X por 'shift' casas decimais (multiplica por 10^shift).
   Alinhamento pelo LSB: X[len-1] cai em C[m-1-shift]. */
static void add_into_shift10(digit *C, int m, const digit *X, int len, int shift) {
    int iC = m - 1 - shift;  /* onde cai o LSB de X */
    int iX = len - 1;
    int carry = 0;

    while ((iX >= 0 || carry > 0) && iC >= 0) {
        int vC = C[iC];
        int vX = (iX >= 0) ? X[iX] : 0;
        int r = vC + vX + carry;
        C[iC] = (digit)(r % 10);
        carry = r / 10;
        iX--; iC--;
    }
    /* Se m for suficiente (é: m=2n), não deve sobrar carry significativo aqui. */
}

/* -------------------- Karatsuba -------------------- */
static void karatsuba(int n, const digit *A, const digit *B, int m, digit *C) {
    if (n <= 0) return;

    /* Caso base: usa tradicional */
    if (n <= KARATSUBA_CUTOFF) {
        tradicional_multi(n, A, B, m, C);
        return;
    }

    /* Divide em metades */
    int mlow = n / 2;       /* parte baixa (menos significativa) */
    int mhigh = n - mlow;   /* parte alta (mais significativa)   */

    const digit *A_high = A;             /* A[0 .. mhigh-1]   */
    const digit *A_low  = A + mhigh;     /* A[mhigh .. n-1]   */
    const digit *B_high = B;             /* B[0 .. mhigh-1]   */
    const digit *B_low  = B + mhigh;     /* B[mhigh .. n-1]   */

    /* Buffers */
    digit *z0 = (digit*) calloc(2*mlow, sizeof(digit));
    digit *z2 = (digit*) calloc(2*mhigh, sizeof(digit));

    int s = (mlow > mhigh ? mlow : mhigh) + 1; /* para somas com possível carry */
    digit *A_sum = (digit*) calloc(s, sizeof(digit));
    digit *B_sum = (digit*) calloc(s, sizeof(digit));
    digit *t1    = (digit*) calloc(2*s, sizeof(digit));
    digit *z1    = (digit*) calloc(2*s, sizeof(digit));
    digit *tmp   = (digit*) calloc(2*s, sizeof(digit));

    if (!z0 || !z2 || !A_sum || !B_sum || !t1 || !z1 || !tmp) {
        fprintf(stderr, "Erro de memória\n");
        exit(1);
    }

    /* z0 = A_low * B_low */
    karatsuba(mlow, A_low, B_low, 2*mlow, z0);

    /* z2 = A_high * B_high */
    karatsuba(mhigh, A_high, B_high, 2*mhigh, z2);

    /* A_sum = A_low + A_high ; B_sum = B_low + B_high (com s dígitos) */
    add_vec(mlow, A_low,  mhigh, A_high, s, A_sum);
    add_vec(mlow, B_low,  mhigh, B_high, s, B_sum);

    /* t1 = (A_low + A_high) * (B_low + B_high) (tamanho 2*s) */
    karatsuba(s, A_sum, B_sum, 2*s, t1);

    /* z1 = t1 - z0 - z2  (todos alinhados à direita em 2*s) */
    /* z1 = t1 - z0 */
    memset(tmp, 0, 2*s);
    memcpy(tmp + (2*s - 2*mlow), z0, 2*mlow);
    sub_vec(2*s, t1, 2*s, tmp, 2*s, z1);

    /* z1 = z1 - z2 */
    memset(tmp, 0, 2*s);
    memcpy(tmp + (2*s - 2*mhigh), z2, 2*mhigh);
    sub_vec(2*s, z1, 2*s, tmp, 2*s, z1);

    /* Montagem do resultado:
       C (2n) = z2 * 10^(2*mlow) + z1 * 10^(mlow) + z0
       Usamos somador que alinha pelo LSB e aplica shift em casas decimais. */
    for (int i = 0; i < m; i++) C[i] = 0;
    add_into_shift10(C, m, z0, 2*mlow, 0);
    add_into_shift10(C, m, z1, 2*s,   mlow);
    add_into_shift10(C, m, z2, 2*mhigh, 2*mlow);

    /* Libera temporários */
    free(z0); free(z2); free(A_sum); free(B_sum); free(t1); free(z1); free(tmp);
}
