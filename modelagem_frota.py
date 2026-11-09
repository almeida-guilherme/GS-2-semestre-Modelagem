import os
import numpy as np
import matplotlib.pyplot as plt

regioes = ["Norte", "Sul", "Leste", "Oeste"]


# ETAPA 1
# x = [N, S, L, O] -> quantidade de ônibus em cada região
def etapa1():
    print("\n--- ETAPA 1: distribuição atual da frota ---\n")

    # cada linha é um registro do Relatório I
    A = np.array([[1, 1, 1, 1],    # N + S + L + O = 72
                  [1, 2, 0, 1],    # N + 2S + O = 76
                  [0, 1, 2, 0],    # S + 2L = 52
                  [1, 0, 1, 2]])   # N + L + 2O = 76
    b = np.array([72, 76, 52, 76])

    print("Matriz A:")
    print(A)
    print("Vetor b:", b)

    # verificando se a solução é única
    det = np.linalg.det(A)
    posto_A = np.linalg.matrix_rank(A)
    posto_Ab = np.linalg.matrix_rank(np.column_stack((A, b)))
    print("\ndet(A) =", round(det, 4))
    print("posto(A) =", posto_A)
    print("posto([A|b]) =", posto_Ab)

    if round(det) != 0 and posto_A == posto_Ab == 4:
        print("Sistema possível e determinado, então a solução é única")
    else:
        print("O sistema não tem solução única")

    x = np.linalg.solve(A, b)

    # conferindo com a inversa
    inversa = np.linalg.inv(A)
    print("\nInversa de A:")
    print(np.round(inversa, 4))
    print("A^-1 . b =", np.round(inversa @ b, 4))

    atual = np.round(x).astype(int)
    print("\nDistribuição encontrada:")
    for i in range(4):
        print(regioes[i], "=", atual[i], "ônibus")

    print("\nTodos inteiros?", np.allclose(x, atual))
    print("Todos >= 0?", np.all(atual >= 0))

    # substituindo a solução nos registros
    print("\nVerificação dos registros:")
    nomes = ["N + S + L + O", "N + 2S + O", "S + 2L", "N + L + 2O"]
    obtido = A @ atual
    for i in range(4):
        if obtido[i] == b[i]:
            status = "OK"
        else:
            status = "ERRO"
        print(nomes[i], "=", obtido[i], "| esperado:", b[i], "->", status)

    return atual


# ETAPA 2
def etapa2(atual):
    print("\n--- ETAPA 2: política de redistribuição ---\n")

    passageiros = np.array([560, 760, 720, 840])
    capacidade = 40

    # a) arredonda pra cima pra nenhum passageiro ficar sem vaga
    necessidade = np.ceil(passageiros / capacidade).astype(int)
    print("a) Ônibus necessários (passageiros / 40):")
    for i in range(4):
        print(regioes[i], ":", passageiros[i], "/ 40 =", necessidade[i])
    print("Total necessário:", necessidade.sum(), "| Frota:", atual.sum())

    # b) saldo positivo = sobra, negativo = falta
    saldo = atual - necessidade
    print("\nb) Desequilíbrio (atual - necessário):")
    for i in range(4):
        if saldo[i] > 0:
            situacao = "sobra"
        elif saldo[i] < 0:
            situacao = "falta"
        else:
            situacao = "ok"
        print(regioes[i], ": atual", atual[i], "| necessário", necessidade[i],
              "| saldo", saldo[i], "(" + situacao + ")")

    # c) transferências (origem, destino, quantidade)
    # Oeste->Norte e Sul->Leste são vizinhas
    # o Leste ainda precisa de 1 e só o Oeste tem sobra
    transferencias = [("Oeste", "Norte", 2),
                      ("Sul", "Leste", 1),
                      ("Oeste", "Leste", 1)]
    print("\nc) Transferências propostas:")
    total_movido = 0
    for origem, destino, qtd in transferencias:
        print(origem, "->", destino, ":", qtd, "ônibus")
        total_movido += qtd
    print("Total de ônibus movidos:", total_movido)

    # d/e) matriz da transformação T(x) = M.x
    # M[i][j] = fração dos ônibus da região j que vai para a região i
    M = np.zeros((4, 4))
    for origem, destino, qtd in transferencias:
        j = regioes.index(origem)
        i = regioes.index(destino)
        M[i][j] = M[i][j] + qtd / atual[j]
    # o que não foi transferido fica na própria região
    for j in range(4):
        M[j][j] = 1 - M[:, j].sum()

    print("\nd/e) Matriz M:")
    print(np.round(M, 4))

    nova = M @ atual
    print("\nNova distribuição T(x) = M.x:")
    for i in range(4):
        print(regioes[i], "=", round(nova[i], 2))

    # restrições: inteiro e não negativo (confere antes de arredondar)
    print("Todos inteiros?", np.allclose(nova, np.round(nova)))
    print("Todos >= 0?", np.all(nova >= 0))
    nova = np.round(nova).astype(int)

    # f) verificações
    print("\nf) Verificações:")
    print("Soma das colunas de M:", np.round(M.sum(axis=0), 4))
    print("Todas as colunas somam 1?", np.allclose(M.sum(axis=0), 1))
    print("Todos os elementos >= 0?", np.all(M >= 0))
    print("Total antes:", atual.sum(), "| Total depois:", nova.sum())
    print("Nova distribuição = necessidade?", np.array_equal(nova, necessidade))

    # testando com outras frotas pra ver que vale pra qualquer x >= 0
    print("\nTeste com outras frotas:")
    testes = [np.array([10, 30, 20, 12]),
              np.array([0, 40, 5, 27]),
              np.array([50, 10, 10, 2])]
    for x_teste in testes:
        y = M @ x_teste
        print("x =", x_teste, "soma =", x_teste.sum(), "| T(x) =", np.round(y, 2),
              "soma =", round(y.sum(), 2), "| menor valor =", round(y.min(), 2))

    # linearidade: T(3u + 2v) = 3T(u) + 2T(v)
    u = np.array([10, 5, 8, 3])
    v = np.array([2, 7, 1, 9])
    print("T(3u + 2v) = 3T(u) + 2T(v)?", np.allclose(M @ (3*u + 2*v), 3*(M @ u) + 2*(M @ v)))

    print("\ndet(M) =", round(np.linalg.det(M), 4), "(diferente de 0, então M é inversível)")

    return passageiros, necessidade, nova


# AVALIAÇÃO
def avaliacao(atual, nova, passageiros):
    print("\n--- AVALIAÇÃO: antes x depois ---")

    ocupacoes = []
    for nome, frota in [("Antes", atual), ("Depois", nova)]:
        vagas = frota * 40
        sem_vaga = passageiros - vagas
        sem_vaga[sem_vaga < 0] = 0
        sobrando = vagas - passageiros
        sobrando[sobrando < 0] = 0
        ocupacao = passageiros / vagas * 100
        ocupacoes.append(ocupacao)

        print("\n" + nome + ":")
        for i in range(4):
            print(regioes[i], ":", frota[i], "ônibus |", vagas[i], "vagas |",
                  sem_vaga[i], "sem vaga |", sobrando[i], "vagas sobrando |",
                  "ocupação", round(ocupacao[i], 1), "%")
        print("Total sem vaga:", sem_vaga.sum(), "| Total de vagas sobrando:", sobrando.sum())

    return ocupacoes


def graficos(atual, necessidade, nova, ocupacoes):
    os.makedirs("graficos", exist_ok=True)
    pos = np.arange(4)

    # gráfico 1 - ônibus por região
    plt.figure(figsize=(8, 4))
    plt.bar(pos - 0.27, atual, 0.25, label="Atual")
    plt.bar(pos, necessidade, 0.25, label="Necessária")
    plt.bar(pos + 0.27, nova, 0.25, label="Após redistribuição")
    for i in range(4):
        plt.text(pos[i] - 0.27, atual[i] + 0.3, atual[i], ha="center")
        plt.text(pos[i], necessidade[i] + 0.3, necessidade[i], ha="center")
        plt.text(pos[i] + 0.27, nova[i] + 0.3, nova[i], ha="center")
    plt.xticks(pos, regioes)
    plt.ylabel("Ônibus")
    plt.ylim(0, 29)
    plt.title("Ônibus por região")
    plt.legend(ncol=3, loc="upper left")
    plt.tight_layout()
    plt.savefig("graficos/onibus_por_regiao.png", dpi=200)
    plt.close()

    # gráfico 2 - ocupação antes e depois
    plt.figure(figsize=(8, 4))
    plt.bar(pos - 0.2, ocupacoes[0], 0.38, label="Antes")
    plt.bar(pos + 0.2, ocupacoes[1], 0.38, label="Depois")
    for i in range(4):
        plt.text(pos[i] - 0.2, ocupacoes[0][i] - 8, str(round(ocupacoes[0][i], 1)) + "%", ha="center", color="white")
        plt.text(pos[i] + 0.2, ocupacoes[1][i] - 8, str(round(ocupacoes[1][i], 1)) + "%", ha="center", color="white")
    plt.axhline(100, color="black", linestyle="--", linewidth=1)
    plt.xticks(pos, regioes)
    plt.ylabel("Ocupação (%)")
    plt.ylim(0, 140)
    plt.title("Ocupação dos ônibus no pico (linha = 100%)")
    plt.legend(ncol=2, loc="upper right")
    plt.tight_layout()
    plt.savefig("graficos/ocupacao_antes_depois.png", dpi=200)
    plt.close()

    print("\nGráficos salvos na pasta graficos/")


atual = etapa1()
passageiros, necessidade, nova = etapa2(atual)
ocupacoes = avaliacao(atual, nova, passageiros)
graficos(atual, necessidade, nova, ocupacoes)
