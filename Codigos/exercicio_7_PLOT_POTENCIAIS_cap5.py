import numpy as np
import matplotlib.pyplot as plt

# ===============================
# CONFIGURAÇÕES DO PROBLEMA
# ===============================
L = 60              # tamanho da grade
tol = 1e-6          # tolerância para convergência
omega = 1.9         # fator de relaxação SOR
max_iter = 500    # máximo de iterações
update_plot = 1    # atualiza a cada X iterações

# ===============================
# CONDIÇÕES DE CONTORNO (CAPACITOR)
# ===============================
def inicializar(L):
    V = np.zeros((L, L))
    y1, y2 = L // 3, 2 * L // 3
    xmid = L // 2
    h = 5  # metade da altura da placa
    V[xmid - h:xmid + h, y1] = 1.0   # placa +1
    V[xmid - h:xmid + h, y2] = -1.0  # placa -1
    return V, y1, y2, xmid, h

# ===============================
# CONFIGURAÇÃO INICIAL
# ===============================
V_jacobi, y1, y2, xmid, h = inicializar(L)
V_sor = V_jacobi.copy()

# ===============================
# CONFIGURAÇÃO DO PLOT
# ===============================
plt.ion()
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
im_j = axes[0].imshow(V_jacobi, cmap='plasma', origin='lower', vmin=-1, vmax=1)
im_s = axes[1].imshow(V_sor, cmap='plasma', origin='lower', vmin=-1, vmax=1)
axes[0].set_title("Método de Jacobi")
axes[1].set_title("Método SOR")
for ax in axes:
    ax.set_xticks([]); ax.set_yticks([])

plt.tight_layout()

# ===============================
# ITERAÇÃO E ATUALIZAÇÃO EM TEMPO REAL
# ===============================
for it in range(1, max_iter + 1):

    # Jacobi: usa cópia anterior
    V_old = V_jacobi.copy()
    V_jacobi[1:-1, 1:-1] = 0.25 * (
        V_old[2:, 1:-1] + V_old[:-2, 1:-1] + V_old[1:-1, 2:] + V_old[1:-1, :-2]
    )
    # reaplica as placas
    V_jacobi[xmid - h:xmid + h, y1] = 1.0
    V_jacobi[xmid - h:xmid + h, y2] = -1.0

    # SOR: atualiza in-place
    for i in range(1, L - 1):
        for j in range(1, L - 1):
            if (j == y1 or j == y2) and (xmid - h <= i < xmid + h):
                continue
            oldV = V_sor[i, j]
            V_sor[i, j] = (1 - omega) * oldV + omega * 0.25 * (
                V_sor[i + 1, j] + V_sor[i - 1, j] + V_sor[i, j + 1] + V_sor[i, j - 1]
            )

    # Reaplica as placas
    V_sor[xmid - h:xmid + h, y1] = 1.0
    V_sor[xmid - h:xmid + h, y2] = -1.0

    # Erros
    err_j = np.max(np.abs(V_jacobi - V_old))
    if it % update_plot == 0:
        im_j.set_data(V_jacobi)
        im_s.set_data(V_sor)
        fig.suptitle(f"Iteração {it} — erro Jacobi={err_j:.2e}")
        plt.pause(0.001)

    if err_j < tol:
        break

plt.ioff()
plt.show()
print(f"Convergência atingida em {it} iterações (erro < {tol})")
