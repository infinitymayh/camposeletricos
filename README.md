# Simulações Computacionais de Potenciais e Campos Elétricos

Este repositório reúne simulações numéricas voltadas ao cálculo de potenciais e campos elétricos em diferentes configurações físicas. Os problemas implementados correspondem aos exercícios **5.1 a 5.10** do livro *Computational Physics* (Giordano & Nakanishi), utilizando métodos iterativos para resolver numericamente as equações de **Laplace** e **Poisson**.

As simulações incluem sistemas como:
- prismas metálicos com condutor interno;
- capacitores planos e estudo do campo de franja;
- cargas pontuais próximas a superfícies aterradas;
- distribuições de potencial em diferentes geometrias;
- análise de convergência e eficiência dos métodos Jacobi, Gauss–Seidel e SOR.

---

## 📁 Estrutura do Repositório

```bash
main/
│
├── codigos/        # Scripts Python com as implementações numéricas
│
├── resultados/     # Imagens, gráficos e mapas de potencial/campo gerados
│
└── relatorio/      # PDF contendo o relatório completo do trabalho
```
---

## 🧠 Conteúdos Principais

- **Métodos numéricos**
  - Jacobi  
  - Gauss–Seidel  
  - Successive Over-Relaxation (SOR)

- **Equações resolvidas**
  - Laplace (∇²V = 0)
  - Poisson (∇²V = –ρ/ε₀)

- **Fenômenos simulados**
  - Potenciais e campos em cavidades metálicas
  - Capacitores planos e efeitos de borda
  - Intensificação de campo em para-raios
  - Cargas pontuais próximas a superfícies condutoras
  - Comparações de desempenho entre métodos iterativos

---

## ▶️ Como Executar

1. Certifique-se de possuir **Python 3.8+** instalado.
2. Instale dependências básicas:

```bash
pip install numpy matplotlib
```

3. Execute qualquer código:

```bash
python codigos/nome_do_arquivo.py
```

---

## Relatório

O PDF completo com a fundamentação teórica, metodologia, resultados e discussões está disponível na pasta ```relatorio/```.
