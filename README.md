# Mobilidade Urbana Inteligente - Modelagem da Frota

Global Solution 2026.2 (CitizenTech) - Modelagem Matemática e Computacional - FIAP

| Integrante | RM |
|---|---|
| André Santos de Azevedo | RM572236 |
| Guilherme Henrique de Almeida | RM568708 |
| Renan de Castro Albuquerque | RM570532 |

## O que o projeto faz

- **Etapa 1:** recupera quantos ônibus cada região (Norte, Sul, Leste e Oeste) tem a partir dos registros que sobraram, montando um sistema linear `A·x = b`. O determinante de A é 3, então a solução é única.
- **Etapa 2:** calcula quantos ônibus cada região precisa no horário de pico e propõe uma redistribuição na forma de transformação linear `T(x) = M·x`, com uma matriz estocástica por colunas.
- **Avaliação:** compara passageiros sem vaga e ocupação antes e depois.

## Resultados

| Região | Atual | Necessário | Depois |
|---|---|---|---|
| Norte | 12 | 14 | 14 |
| Sul | 20 | 19 | 19 |
| Leste | 16 | 18 | 18 |
| Oeste | 24 | 21 | 21 |
| **Total** | **72** | **72** | **72** |

Transferências: Oeste → Norte (2), Sul → Leste (1), Oeste → Leste (1).
Os passageiros sem vaga caem de 160 para 0.

## Como rodar

```bash
pip install -r requirements.txt
python modelagem_frota.py
```

A saída vai para o terminal e os gráficos são salvos em `graficos/`.

## Arquivos

- `modelagem_frota.py` - código das duas etapas e da avaliação
- `graficos/` - gráficos usados no relatório
- `relatorio/` - relatório (HTML e PDF)
