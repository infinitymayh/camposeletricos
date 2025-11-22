import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time

def potential(i,j):
	
	if i == 2 and j == n//2:
		return 1
	elif i == 0 or j == 0 or i == n or j == n:
		return 0
	else:
		a = field[i+1][j]
		b = field[i-1][j]
		c = field[i][j+1]
		d = field[i][j-1]
		e = (rho[i][j]*delta_x**2)/4
		
		return (a+b+c+d)/4 + e


n = 21 #tamanho da matriz n x n

rho = np.zeros((n,n))
rho[2][n//2]=1
field=rho.copy()
delta_x = 0.001 # = delta y = delta z

delta_max = 1e9
tolerance = 1e-6

######### GRÁFICO

plt.ion()  # modo interativo ligado
fig = plt.figure(figsize=(14,14))
gs = fig.add_gridspec(2, 2)

x = np.arange(rho.shape[0])
y = np.arange(rho.shape[1])
X, Y = np.meshgrid(x, y)


ax1 = fig.add_subplot(gs[0, 0])
im = ax1.imshow(field, cmap='plasma', origin='lower', vmin=0, vmax=1)
plt.colorbar(im)
ax1.set_title('Potencial 2D')

ax2 = fig.add_subplot(gs[0,1])
dVy, dVx = np.gradient(field)
Ex = -dVx
Ey = -dVy
step = 1  # amostragem das setas
Q = ax2.quiver(X[::step,::step], Y[::step,::step],
               Ex[::step,::step], Ey[::step,::step], scale=0.2, color='r')
ax2.set_title("Campo eletrico E")
ax2.set_aspect('equal') 

## 3D
ax3 = fig.add_subplot(gs[1,0], projection='3d')
ax3.plot_surface(X, Y, field.T, cmap='plasma')
ax3.set_title('Potencial 3D')

start_time = time.time()

iteration = 0
####### CALCULO
while delta_max > tolerance:
	delta_max = 0
	iteration +=1
	for x in range(0,n-1):
		for y in range(0,n-1):
			new_val = potential(x,y)
			delta_max = max(delta_max, abs(new_val - field[x][y]))
			field[x][y]=new_val
				
	
	dVy, dVx = np.gradient(field, y, x)
	Ex = -dVx
	Ey = -dVy
	
	
	it = time.time()
	it_time = it - start_time
	
	step = 1
	im.set_data(field)
	Q.set_UVC(Ex[::step,::step], Ey[::step,::step])
	ax3.collections.clear()
	ax3.plot_surface(X, Y, field.T, cmap='plasma')
	fig.suptitle(f"Iteraçoes:{iteration}\nErro de convergência: {delta_max:.6f}\nCriterio de convergencia: {tolerance}", fontsize=14)
	plt.pause(0.01)

plt.ioff()
plt.show()
end_time = time.time()
dtime = end_time - start_time
print(f"Tempo de execução: {dtime:.4f} segundos")


