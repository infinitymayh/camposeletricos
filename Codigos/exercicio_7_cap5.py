import numpy as np
import matplotlib.pyplot as plt

def capacitor_jacobi(L, tol=1e-5, max_iter=10000):
    V = np.zeros((L, L))
    V_new = np.zeros_like(V)
    
    # Placas
    y1, y2 = L//3, 2*L//3
    V[L//2 - 5:L//2 + 5, y1] = 1.0
    V[L//2 - 5:L//2 + 5, y2] = -1.0
    
    for it in range(max_iter):
        V_new[1:-1, 1:-1] = 0.25 * (V[2:, 1:-1] + V[:-2, 1:-1] + V[1:-1, 2:] + V[1:-1, :-2])
        
        # Reaplica as condições das placas
        V_new[L//2 - 5:L//2 + 5, y1] = 1.0
        V_new[L//2 - 5:L//2 + 5, y2] = -1.0
        
        error = np.max(np.abs(V_new - V))
        if error < tol:
            return V_new, it
        
        V[:] = V_new[:]
    
    return V, max_iter


def capacitor_SOR(L, omega=1.9, tol=1e-5, max_iter=10000):
    V = np.zeros((L, L))
    y1, y2 = L//3, 2*L//3
    V[L//2 - 5:L//2 + 5, y1] = 1.0
    V[L//2 - 5:L//2 + 5, y2] = -1.0
    
    for it in range(max_iter):
        max_diff = 0
        for i in range(1, L-1):
            for j in range(1, L-1):
                if (j == y1 or j == y2) and (L//2 - 5 <= i < L//2 + 5):
                    continue  # placas fixas
                oldV = V[i, j]
                V[i, j] = (1 - omega) * oldV + omega * 0.25 * (V[i+1, j] + V[i-1, j] + V[i, j+1] + V[i, j-1])
                max_diff = max(max_diff, abs(V[i, j] - oldV))
        if max_diff < tol:
            return V, it
    return V, max_iter


# Teste e comparação
sizes = [20, 40, 80, 160]
jacobi_iters, sor_iters = [], []

for L in sizes:
    _, it_j = capacitor_jacobi(L)
    _, it_s = capacitor_SOR(L)
    jacobi_iters.append(it_j)
    sor_iters.append(it_s)

plt.loglog(sizes, jacobi_iters, 'o-', label='Jacobi')
plt.loglog(sizes, sor_iters, 's-', label='SOR')
plt.xlabel('L (número de pontos por dimensão)')
plt.ylabel('N_iter')
plt.legend()
plt.show()
