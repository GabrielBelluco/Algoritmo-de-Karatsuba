"""
Exemplos e Demonstrações do Algoritmo de Karatsuba
Projeto e Análise de Algoritmos

Este arquivo contém exemplos práticos e demonstrações do algoritmo
de Karatsuba, incluindo análise de complexidade e comparações.
"""

import time
import math
from karatsuba import karatsuba, multiplicacao_tradicional, comparar_algoritmos


def demonstrar_algoritmo_passo_a_passo(x, y):
    """
    Demonstra o algoritmo de Karatsuba passo a passo para fins educacionais.
    
    Args:
        x (int): Primeiro número
        y (int): Segundo número
    """
    print(f"\n=== Demonstração Passo a Passo: {x} × {y} ===")
    
    if x < 10 or y < 10:
        resultado = x * y
        print(f"Caso base: {x} × {y} = {resultado}")
        return resultado
    
    # Calcula o número de dígitos
    n = max(len(str(abs(x))), len(str(abs(y))))
    m = n // 2
    divisor = 10 ** m
    
    print(f"Número de dígitos: {n}")
    print(f"Ponto de divisão: {m}")
    print(f"Divisor: {divisor}")
    
    # Divide os números
    a = x // divisor
    b = x % divisor
    c = y // divisor
    d = y % divisor
    
    print(f"\nDivisão dos números:")
    print(f"x = {x} = {a} × {divisor} + {b}")
    print(f"y = {y} = {c} × {divisor} + {d}")
    
    # Calcula as três multiplicações recursivas
    print(f"\nCálculos recursivos:")
    print(f"ac = {a} × {c}")
    ac = karatsuba(a, c)
    print(f"ac = {ac}")
    
    print(f"bd = {b} × {d}")
    bd = karatsuba(b, d)
    print(f"bd = {bd}")
    
    print(f"(a+b)(c+d) = ({a}+{b}) × ({c}+{d}) = {a+b} × {c+d}")
    soma_produto = karatsuba(a + b, c + d)
    print(f"(a+b)(c+d) = {soma_produto}")
    
    ad_bc = soma_produto - ac - bd
    print(f"ad+bc = {soma_produto} - {ac} - {bd} = {ad_bc}")
    
    # Resultado final
    resultado = ac * (10 ** (2 * m)) + ad_bc * (10 ** m) + bd
    print(f"\nResultado final:")
    print(f"{ac} × {10**(2*m)} + {ad_bc} × {10**m} + {bd}")
    print(f"= {ac * (10**(2*m))} + {ad_bc * (10**m)} + {bd}")
    print(f"= {resultado}")
    
    # Verificação
    verificacao = x * y
    print(f"\nVerificação: {x} × {y} = {verificacao}")
    print(f"Correto: {'✓' if resultado == verificacao else '✗'}")
    
    return resultado


def analise_complexidade():
    """Analisa a complexidade do algoritmo com diferentes tamanhos de entrada."""
    print("\n=== Análise de Complexidade ===")
    
    # Usa números pré-definidos para evitar problemas de conversão
    casos = [
        (10, 1234567890, 9876543210),
        (100, 12345678901234567890123456789012345678901234567890, 98765432109876543210987654321098765432109876543210),
    ]
    
    print(f"{'Dígitos':<10} {'Karatsuba (s)':<15} {'Tradicional (s)':<17} {'Speedup':<10}")
    print("-" * 55)
    
    for digitos, x, y in casos:
        # Mede tempo do Karatsuba
        start = time.time()
        resultado_k = karatsuba(x, y)
        tempo_k = time.time() - start
        
        # Mede tempo da multiplicação tradicional
        start = time.time()
        resultado_t = x * y
        tempo_t = time.time() - start
        
        # Calcula speedup
        speedup = tempo_t / tempo_k if tempo_k > 0 else float('inf')
        
        print(f"{digitos:<10} {tempo_k:<15.6f} {tempo_t:<17.6f} {speedup:<10.2f}")
        
        # Verifica se os resultados são iguais
        if resultado_k != resultado_t:
            print(f"ERRO: Resultados diferentes para {digitos} dígitos!")


def exemplos_praticos():
    """Executa exemplos práticos do algoritmo."""
    print("\n=== Exemplos Práticos ===")
    
    exemplos = [
        ("Multiplicação simples", 123, 456),
        ("Números iguais", 999, 999),
        ("Número grande", 123456789, 987654321),
        ("Potências de 10", 1000, 2000),
        ("Números primos", 97, 101)
    ]
    
    for descricao, x, y in exemplos:
        print(f"\n{descricao}:")
        resultado = comparar_algoritmos(x, y)
        print(f"  {x} × {y} = {resultado['karatsuba']}")
        print(f"  Verificação: {'✓' if resultado['correto'] else '✗'}")


def comparacao_visual():
    """Cria uma comparação visual entre os algoritmos."""
    print("\n=== Comparação Visual ===")
    
    casos = [
        (12, 34),
        (123, 456),
        (1234, 5678),
        (12345, 67890)
    ]
    
    print(f"{'X':<8} {'Y':<8} {'Karatsuba':<12} {'Tradicional':<12} {'Match':<6}")
    print("-" * 50)
    
    for x, y in casos:
        resultado_k = karatsuba(x, y)
        resultado_t = x * y
        match = "✓" if resultado_k == resultado_t else "✗"
        
        print(f"{x:<8} {y:<8} {resultado_k:<12} {resultado_t:<12} {match:<6}")


def benchmark_detalhado():
    """Executa um benchmark detalhado dos algoritmos."""
    print("\n=== Benchmark Detalhado ===")
    
    print("Testando diferentes cenários de multiplicação...\n")
    
    cenarios = [
        ("Números pequenos (2 dígitos)", [(12, 34), (56, 78), (91, 23)]),
        ("Números médios (4 dígitos)", [(1234, 5678), (9999, 1111), (4567, 8901)]),
        ("Números grandes (8 dígitos)", [(12345678, 87654321), (99999999, 11111111)])
    ]
    
    for nome_cenario, casos in cenarios:
        print(f"{nome_cenario}:")
        
        tempo_total_k = 0
        tempo_total_t = 0
        
        for x, y in casos:
            # Karatsuba
            start = time.time()
            resultado_k = karatsuba(x, y)
            tempo_k = time.time() - start
            tempo_total_k += tempo_k
            
            # Tradicional
            start = time.time()
            resultado_t = x * y
            tempo_t = time.time() - start
            tempo_total_t += tempo_t
            
            print(f"  {x} × {y}: Karatsuba={tempo_k:.6f}s, Tradicional={tempo_t:.6f}s")
        
        print(f"  Tempo total - Karatsuba: {tempo_total_k:.6f}s")
        print(f"  Tempo total - Tradicional: {tempo_total_t:.6f}s")
        print(f"  Speedup médio: {tempo_total_t/tempo_total_k:.2f}x\n")


def main():
    """Função principal que executa todas as demonstrações."""
    print("🔢 ALGORITMO DE KARATSUBA - DEMONSTRAÇÕES")
    print("=" * 50)
    
    # Demonstração passo a passo
    demonstrar_algoritmo_passo_a_passo(1234, 5678)
    
    # Exemplos práticos
    exemplos_praticos()
    
    # Comparação visual
    comparacao_visual()
    
    # Análise de complexidade
    analise_complexidade()
    
    # Benchmark detalhado
    benchmark_detalhado()
    
    print("\n" + "=" * 50)
    print("✅ Demonstrações concluídas!")
    print("\nO algoritmo de Karatsuba demonstra sua eficiência")
    print("especialmente para números muito grandes, com")
    print("complexidade O(n^1.585) vs O(n^2) do método tradicional.")


if __name__ == "__main__":
    main()