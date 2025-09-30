"""
Testes para o Algoritmo de Karatsuba
Projeto e Análise de Algoritmos

Este arquivo contém testes unitários e casos de teste para validar
a implementação do algoritmo de Karatsuba.
"""

import unittest
import time
import random
from karatsuba import karatsuba, karatsuba_string, multiplicacao_tradicional, comparar_algoritmos


class TestKaratsuba(unittest.TestCase):
    """Classe de testes unitários para o algoritmo de Karatsuba."""
    
    def test_casos_basicos(self):
        """Testa casos básicos de multiplicação."""
        casos = [
            (0, 0, 0),
            (0, 5, 0),
            (1, 1, 1),
            (2, 3, 6),
            (9, 9, 81),
            (10, 10, 100)
        ]
        
        for x, y, esperado in casos:
            with self.subTest(x=x, y=y):
                resultado = karatsuba(x, y)
                self.assertEqual(resultado, esperado,
                               f"karatsuba({x}, {y}) deveria ser {esperado}, mas foi {resultado}")
    
    def test_numeros_grandes(self):
        """Testa multiplicação de números grandes."""
        casos = [
            (123, 456),
            (1234, 5678),
            (12345, 67890),
            (999999, 999999),
            (123456789, 987654321)
        ]
        
        for x, y in casos:
            with self.subTest(x=x, y=y):
                resultado_karatsuba = karatsuba(x, y)
                resultado_esperado = x * y
                self.assertEqual(resultado_karatsuba, resultado_esperado,
                               f"karatsuba({x}, {y}) falhou")
    
    def test_numeros_negativos(self):
        """Testa multiplicação com números negativos."""
        casos = [
            (-5, 3, -15),
            (5, -3, -15),
            (-5, -3, 15),
            (-123, 456, -56088),
            (123, -456, -56088),
            (-123, -456, 56088)
        ]
        
        for x, y, esperado in casos:
            with self.subTest(x=x, y=y):
                resultado = karatsuba(x, y)
                self.assertEqual(resultado, esperado,
                               f"karatsuba({x}, {y}) deveria ser {esperado}, mas foi {resultado}")
    
    def test_comparacao_com_tradicional(self):
        """Testa se o resultado do Karatsuba é igual à multiplicação tradicional."""
        casos = [
            (12, 34),
            (123, 456),
            (1234, 5678),
            (12345, 67890),
            (999, 999),
            (10000, 20000)
        ]
        
        for x, y in casos:
            with self.subTest(x=x, y=y):
                resultado = comparar_algoritmos(x, y)
                self.assertTrue(resultado['correto'],
                              f"Algoritmos divergem para {x} × {y}")
    
    def test_karatsuba_string(self):
        """Testa a versão string do algoritmo."""
        casos = [
            ("123", "456", "56088"),
            ("1234", "5678", "7006652"),
            ("999", "999", "998001")
        ]
        
        for x_str, y_str, esperado in casos:
            with self.subTest(x=x_str, y=y_str):
                resultado = karatsuba_string(x_str, y_str)
                self.assertEqual(resultado, esperado,
                               f"karatsuba_string({x_str}, {y_str}) falhou")
    
    def test_numeros_aleatorios(self):
        """Testa com números gerados aleatoriamente."""
        random.seed(42)  # Para reprodutibilidade
        
        for _ in range(10):
            x = random.randint(1, 999999)
            y = random.randint(1, 999999)
            
            with self.subTest(x=x, y=y):
                resultado_karatsuba = karatsuba(x, y)
                resultado_esperado = x * y
                self.assertEqual(resultado_karatsuba, resultado_esperado,
                               f"Falha com números aleatórios: {x} × {y}")


class TestPerformance(unittest.TestCase):
    """Testes de performance para comparar Karatsuba com multiplicação tradicional."""
    
    def test_performance_numeros_grandes(self):
        """Compara performance entre Karatsuba e multiplicação tradicional."""
        # Números grandes para teste de performance
        x = 12345678901234567890
        y = 98765432109876543210
        
        # Teste Karatsuba
        start_time = time.time()
        resultado_karatsuba = karatsuba(x, y)
        tempo_karatsuba = time.time() - start_time
        
        # Teste multiplicação tradicional (Python built-in)
        start_time = time.time()
        resultado_tradicional = x * y
        tempo_tradicional = time.time() - start_time
        
        # Verifica se os resultados são iguais
        self.assertEqual(resultado_karatsuba, resultado_tradicional,
                        "Resultados diferentes entre algoritmos")
        
        print(f"\nTeste de Performance:")
        print(f"Karatsuba: {tempo_karatsuba:.6f}s")
        print(f"Tradicional: {tempo_tradicional:.6f}s")
        print(f"Números testados: {x} × {y}")


def executar_testes_manuais():
    """Executa testes manuais adicionais para demonstração."""
    print("=== Testes Manuais do Algoritmo de Karatsuba ===\n")
    
    # Teste 1: Casos básicos
    print("1. Casos Básicos:")
    casos_basicos = [(12, 34), (123, 456), (1234, 5678)]
    for x, y in casos_basicos:
        resultado = karatsuba(x, y)
        esperado = x * y
        status = "✓" if resultado == esperado else "✗"
        print(f"   {x} × {y} = {resultado} {status}")
    
    # Teste 2: Números grandes
    print("\n2. Números Grandes:")
    x, y = 999999999, 888888888
    resultado = karatsuba(x, y)
    esperado = x * y
    status = "✓" if resultado == esperado else "✗"
    print(f"   {x} × {y} = {resultado} {status}")
    
    # Teste 3: Comparação de performance
    print("\n3. Teste de Performance:")
    x, y = 123456789012345, 987654321098765
    
    start = time.time()
    resultado_k = karatsuba(x, y)
    tempo_k = time.time() - start
    
    start = time.time()
    resultado_t = x * y
    tempo_t = time.time() - start
    
    print(f"   Karatsuba: {tempo_k:.6f}s")
    print(f"   Tradicional: {tempo_t:.6f}s")
    print(f"   Resultado correto: {'✓' if resultado_k == resultado_t else '✗'}")
    
    print("\n=== Testes Manuais Finalizados ===")


if __name__ == "__main__":
    # Executa testes unitários
    print("Executando testes unitários...")
    unittest.main(verbosity=2, exit=False)
    
    print("\n" + "="*50)
    
    # Executa testes manuais
    executar_testes_manuais()