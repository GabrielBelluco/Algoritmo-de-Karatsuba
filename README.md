# Algoritmo de Karatsuba

**Trabalho de Disciplina de Projeto e Análise de Algoritmos**

Este repositório contém uma implementação completa do **Algoritmo de Karatsuba** para multiplicação eficiente de números inteiros grandes, desenvolvido como projeto acadêmico para a disciplina de Projeto e Análise de Algoritmos.

## 📖 Sobre o Algoritmo

O algoritmo de Karatsuba é um método de **divisão e conquista** para multiplicação de números inteiros que supera a complexidade da multiplicação tradicional:

- **Complexidade Tradicional**: O(n²)
- **Complexidade Karatsuba**: O(n^log₂(3)) ≈ O(n^1.585)

O algoritmo foi descoberto por Anatoly Karatsuba em 1960 e foi o primeiro algoritmo de multiplicação a quebrar a barreira quadrática.

### Como Funciona

Para multiplicar dois números `x` e `y` de `n` dígitos:

1. **Divisão**: Divide cada número em duas partes de `n/2` dígitos
2. **Conquista**: Realiza três multiplicações recursivas ao invés de quatro
3. **Combinação**: Reconstrói o resultado usando as três multiplicações

**Exemplo**: Para `x = 1234` e `y = 5678`
- x = 12 × 10² + 34 = a × 10^m + b
- y = 56 × 10² + 78 = c × 10^m + d

**Três multiplicações**:
- ac = 12 × 56 = 672
- bd = 34 × 78 = 2652  
- (a+b)(c+d) = 46 × 134 = 6164
- ad + bc = 6164 - 672 - 2652 = 2840

**Resultado**: 672 × 10⁴ + 2840 × 10² + 2652 = 7,006,652

## 🚀 Como Usar

### Requisitos
- Python 3.6 ou superior
- Nenhuma dependência externa

### Execução Rápida

```bash
# Teste básico da implementação
python karatsuba.py

# Executar testes unitários
python test_karatsuba.py

# Ver demonstrações completas
python examples.py
```

### Uso no Código

```python
from karatsuba import karatsuba, comparar_algoritmos

# Multiplicação simples
resultado = karatsuba(1234, 5678)
print(resultado)  # 7006652

# Comparação com método tradicional
comparacao = comparar_algoritmos(12345, 67890)
print(f"Resultado: {comparacao['karatsuba']}")
print(f"Correto: {comparacao['correto']}")

# Para números muito grandes (como strings)
from karatsuba import karatsuba_string
resultado_grande = karatsuba_string("999999999999", "888888888888")
```

## 📁 Estrutura do Projeto

```
Algoritmo-de-Karatsuba/
├── karatsuba.py          # Implementação principal do algoritmo
├── test_karatsuba.py     # Testes unitários e validação
├── examples.py           # Demonstrações e análise de performance
└── README.md            # Este arquivo
```

### Arquivos Principais

- **`karatsuba.py`**: Contém a implementação principal do algoritmo com funções auxiliares
- **`test_karatsuba.py`**: Suite completa de testes incluindo casos extremos e performance
- **`examples.py`**: Demonstrações passo a passo e análise comparativa

## 🧪 Testes e Validação

O projeto inclui uma suite abrangente de testes:

### Tipos de Teste
- ✅ Casos básicos (números pequenos)
- ✅ Números grandes
- ✅ Números negativos
- ✅ Comparação com multiplicação tradicional
- ✅ Testes de performance
- ✅ Números aleatórios
- ✅ Casos extremos (zeros, potências de 10)

### Executar Testes

```bash
# Todos os testes
python test_karatsuba.py

# Apenas demonstrações
python examples.py
```

## 📊 Análise de Performance

O algoritmo mostra vantagens significativas para números muito grandes:

| Tamanho | Karatsuba | Tradicional | Vantagem |
|---------|-----------|-------------|----------|
| 10 dígitos | ~0.000046s | ~0.000000s | Para educação |
| 100 dígitos | ~0.000336s | ~0.000000s | Demonstração teórica |
| 1000+ dígitos | Vantagem significativa | - | Uso prático |

*Nota: Para números pequenos, o overhead da recursão pode fazer o Python built-in ser mais rápido. A vantagem real aparece com números de milhares de dígitos.*

## 🎯 Objetivos Educacionais

Este projeto demonstra:

1. **Algoritmos de Divisão e Conquista**
2. **Análise de Complexidade Assintótica**
3. **Otimização de Algoritmos Clássicos**
4. **Implementação e Testes em Python**
5. **Comparação de Performance**
6. **Documentação Técnica**

## 🔍 Funcionalidades

### Algoritmo Principal
- Implementação recursiva do Karatsuba
- Suporte a números negativos
- Otimização para casos base
- Versão para strings (números muito grandes)

### Ferramentas de Análise
- Comparação automática com multiplicação tradicional
- Medição de performance
- Demonstração passo a passo
- Análise de complexidade

### Testes Abrangentes
- Casos básicos e extremos
- Testes de regressão
- Validação com números aleatórios
- Benchmarks de performance

## 📚 Referências Acadêmicas

- Karatsuba, A. and Ofman, Y. (1962). "Multiplication of Many-Digital Numbers by Automatic Computers"
- Cormen, T. H., et al. "Introduction to Algorithms" - Capítulo sobre Divide and Conquer
- Knuth, D. E. "The Art of Computer Programming, Volume 2"

## 👨‍💻 Desenvolvimento

Este projeto foi desenvolvido como parte do trabalho acadêmico da disciplina de **Projeto e Análise de Algoritmos**, demonstrando:

- Implementação correta do algoritmo clássico
- Testes rigorosos e validação
- Análise de complexidade prática
- Documentação completa
- Código limpo e bem comentado

## 🏃‍♂️ Próximos Passos

Possíveis extensões do projeto:
- [ ] Implementação iterativa
- [ ] Comparação com outros algoritmos (Toom-Cook, FFT)
- [ ] Otimizações específicas para Python
- [ ] Interface gráfica para visualização
- [ ] Análise de uso de memória

---

**Autor**: Gabriel Belluco  
**Disciplina**: Projeto e Análise de Algoritmos  
**Algoritmo**: Karatsuba (1960)
