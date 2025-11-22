import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time

def potential(r,V):
	idx = np.where(np.isclose(r_list, r))[0][0]
	if r <= r_min:
		return 1000
	elif np.isclose(r, r_far):
		return 0
	else:
		a = (grid_size**2)
		b = V[idx+1]*(1+(grid_size/r))
		c = V[idx-1]*(1-(grid_size/r))
		return 0.5*(a+b+c)

r_min = 0.2
r_far = 5
grid_size = 0.025

delta_max = 1e9
tolerance = 1e-6

r_list = np.arange(0,r_far+grid_size,grid_size)
V = np.zeros_like(r_list)
V[r_list <= r_min] = 1000
V[np.isclose(r_list, r_far)] = 0

######### GRÁFICO
plt.ion()  # modo interativo
fig, ax = plt.subplots(figsize=(8, 5))
line, = ax.plot(r_list, V, color='royalblue', lw=2)
ax.set_xlabel("r")
ax.set_ylabel("Potencial V(r)")
ax.set_title("Convergência iterativa do potencial radial")
ax.grid(True)
plt.tight_layout()

iteration = 0
####### CALCULO
while delta_max > tolerance:
	delta_max = 0
	iteration +=1
	for i, r in enumerate(r_list[1:-1], start=1):  # evita bordas
		new_val = potential(r, V)
		delta_max = max(delta_max, abs(new_val - V[i]))
		V[i] = new_val
	
	line.set_ydata(V)
	ax.set_title(f"Convergência do potencial — iteração {iteration}")
	plt.pause(0.01)
	
plt.ioff()
line.set_ydata(V)
ax.set_title(f"Solução final após {iteration} iterações")
plt.draw()
plt.show()

print("Convergiu em", iteration, "iterações")
	
