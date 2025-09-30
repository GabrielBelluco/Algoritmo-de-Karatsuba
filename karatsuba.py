"""
Implementação do Algoritmo de Karatsuba
Projeto e Análise de Algoritmos

O algoritmo de Karatsuba é um método de divisão e conquista para multiplicação 
de números inteiros grandes de forma mais eficiente que o método tradicional.

Complexidade: O(n^log2(3)) ≈ O(n^1.585) ao invés de O(n^2)
"""

import math


def karatsuba(x, y):
    """
    Multiplica dois números inteiros usando o algoritmo de Karatsuba.
    
    Args:
        x (int): Primeiro número
        y (int): Segundo número
    
    Returns:
        int: Produto de x e y
    """
    # Caso base: números pequenos
    if x < 10 or y < 10:
        return x * y
    
    # Calcula o número de dígitos dos números
    n = max(len(str(abs(x))), len(str(abs(y))))
    
    # Se n é ímpar, arredonda para cima
    m = n // 2
    
    # Divide os números em duas partes
    # x = a * 10^m + b
    # y = c * 10^m + d
    divisor = 10 ** m
    
    a = x // divisor
    b = x % divisor
    c = y // divisor
    d = y % divisor
    
    # Recursivamente calcula:
    # ac = a * c
    # bd = b * d
    # ad_bc = (a + b) * (c + d) - ac - bd = a*d + b*c
    ac = karatsuba(a, c)
    bd = karatsuba(b, d)
    ad_bc = karatsuba(a + b, c + d) - ac - bd
    
    # Resultado final: ac * 10^(2m) + ad_bc * 10^m + bd
    return ac * (10 ** (2 * m)) + ad_bc * (10 ** m) + bd


def karatsuba_string(x_str, y_str):
    """
    Versão do algoritmo que trabalha com strings para números muito grandes.
    
    Args:
        x_str (str): Primeiro número como string
        y_str (str): Segundo número como string
    
    Returns:
        str: Produto como string
    """
    # Converte para inteiros e usa a função principal
    x = int(x_str)
    y = int(y_str)
    result = karatsuba(x, y)
    return str(result)


def multiplicacao_tradicional(x, y):
    """
    Multiplicação tradicional para comparação de performance.
    
    Args:
        x (int): Primeiro número
        y (int): Segundo número
    
    Returns:
        int: Produto de x e y
    """
    return x * y


def comparar_algoritmos(x, y):
    """
    Compara o resultado do algoritmo de Karatsuba com a multiplicação tradicional.
    
    Args:
        x (int): Primeiro número
        y (int): Segundo número
    
    Returns:
        dict: Dicionário com os resultados e comparação
    """
    resultado_karatsuba = karatsuba(x, y)
    resultado_tradicional = multiplicacao_tradicional(x, y)
    
    return {
        'x': x,
        'y': y,
        'karatsuba': resultado_karatsuba,
        'tradicional': resultado_tradicional,
        'correto': resultado_karatsuba == resultado_tradicional
    }


if __name__ == "__main__":
    # Teste básico
    print("=== Teste do Algoritmo de Karatsuba ===")
    
    # Casos de teste
    casos_teste = [
        (12, 34),
        (123, 456),
        (1234, 5678),
        (12345, 67890),
        (999999, 999999)
    ]
    
    for x, y in casos_teste:
        resultado = comparar_algoritmos(x, y)
        print(f"{x} × {y} = {resultado['karatsuba']} (Correto: {resultado['correto']})")
    
    print("\n=== Teste finalizado ===")