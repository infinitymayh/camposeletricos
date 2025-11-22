import numpy as np
import matplotlib.pyplot as plt
import time

def sor_2d(N, alpha, max_iter=5000, tol=1e-6):
    """Resolve a equação de Laplace 2D via SOR."""
    V = np.zeros((N, N))
    V_new = V.copy()

    # Carga pontual no centro
    cx, cy = N//2, N//2
    V[cx, cy] = 1.0

    start = time.time()
    for it in range(max_iter):
        V_old = V.copy()
        for i in range(1, N-1):
            for j in range(1, N-1):
                if (i, j) != (cx, cy):
                    V_star = 0.25 * (V[i+1,j] + V[i-1,j] + V[i,j+1] + V[i,j-1])
                    V[i,j] = (1 - alpha)*V[i,j] + alpha*V_star
        delta = np.max(np.abs(V - V_old))
        if delta < tol:
            break
    end = time.time()
    return V, it, end - start

def sor_3d(N, alpha, max_iter=3000, tol=1e-6):
    """Resolve a equação de Laplace 3D via SOR."""
    V = np.zeros((N, N, N))
    V_new = V.copy()

    cx, cy, cz = N//2, N//2, N//2
    V[cx, cy, cz] = 1.0

    start = time.time()
    for it in range(max_iter):
        V_old = V.copy()
        for i in range(1, N-1):
            for j in range(1, N-1):
                for k in range(1, N-1):
                    if (i,j,k) != (cx,cy,cz):
                        V_star = (V[i+1,j,k] + V[i-1,j,k] + V[i,j+1,k] + V[i,j-1,k] + V[i,j,k+1] + V[i,j,k-1]) / 6
                        V[i,j,k] = (1 - alpha)*V[i,j,k] + alpha*V_star
        delta = np.max(np.abs(V - V_old))
        if delta < tol:
            break
    end = time.time()
    return V, it, end - start

# -------------------------------------------------------------
# Testando desempenho
alphas = np.linspace(1.0, 1.95, 10)
N = 50

iters_2d, times_2d = [], []
for a in alphas:
    V, it, t = sor_2d(N, a)
    iters_2d.append(it)
    times_2d.append(t)
    print(f"2D: α={a:.2f}, iter={it}, tempo={t:.2f}s")

iters_3d, times_3d = [], []
for a in alphas:
    V, it, t = sor_3d(30, a)
    iters_3d.append(it)
    times_3d.append(t)
    print(f"3D: α={a:.2f}, iter={it}, tempo={t:.2f}s")

# -------------------------------------------------------------
# Plotando resultados
plt.figure(figsize=(8,5))
plt.plot(alphas, iters_2d, 'o-', label='2D - Iterações')
plt.plot(alphas, iters_3d, 's-', label='3D - Iterações')
plt.xlabel('α')
plt.ylabel('Número de iterações até convergência')
plt.legend()
plt.grid(True)
plt.show()

