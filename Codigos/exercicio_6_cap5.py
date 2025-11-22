import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time

def potential(i,j):
	
	if i == c_x and j in range(c_min,c_max+1):
		return 0
	elif j == n-1 :
		return 0
	elif j == 0 or i == 0 or i == n-1:
		return 1
	else:
		a = prism[i+1][j]
		b = prism[i-1][j]
		c = prism[i][j+1]
		d = prism[i][j-1]
		
		return (a+b+c+d)/4
		
####### CALCULOS PARA APENAS 1/4 DO PRISMA

n = 101 #tamanho da matriz n x n
c_min = 30 #indice minimo do condutor
c_max = 100 #indice maximo do condutor

prism = np.zeros((n,n))

#metade superior da placa direita
c_x = 50 #posição da placa no eixo x
'''
for j in range(c_min,c_max+1):
		prism[c_x,j] = 0
'''

rod = np.arange(c_min,c_max+1)


delta_max = 1e9
tolerance = 1e-6

######### GRÁFICO

plt.ion()  # modo interativo ligado
fig = plt.figure(figsize=(14,6))
'''
full = np.block([
		[np.flipud(np.fliplr(prism[1:,1:])), np.flipud(prism[1:,:])],
		[np.fliplr(prism[:,1:]), prism] 
	])
'''
x = np.arange(prism.shape[0])
y = np.arange(prism.shape[1])
X, Y = np.meshgrid(x, y)


ax1 = fig.add_subplot(1, 2, 1)
im = ax1.imshow(prism, cmap='hot', origin='upper', vmin=0, vmax=1)
plt.colorbar(im)
ax1.set_title('Potencial 2D')

ax2 = fig.add_subplot(1, 2, 2)
dVy, dVx = np.gradient(prism)
Ex = -dVx
Ey = -dVy
step = 3  # amostragem das setas
Q = ax2.quiver(X[::step,::step], Y[::step,::step],
               Ex[::step,::step], Ey[::step,::step], scale=0.01, color='r')
ax2.set_title("Campo eletrico E")
start_time = time.time()

iteration = 0
####### CALCULO
while delta_max > tolerance:
	delta_max = 0
	iteration +=1
	for x in range(0,n):
		for y in range(0,n):
			
			if (x == c_x) and (y in rod):
				pass
			else:
				new_val = potential(x,y)
				delta_max = max(delta_max, abs(new_val - prism[x][y]))
				prism[x][y]=new_val
				
	####### MONTANDO O PRISMA INTEIRO
	'''
	full = np.rot90(np.block([
		[np.flipud(np.fliplr(np.abs(prism[1:,1:]))), np.flipud(np.abs(prism[1:,:]))],
		[np.fliplr(prism[:,1:]), prism]
	]))
	'''

	dVy, dVx = np.gradient(prism, y, x)
	Ex = -dVx
	Ey = -dVy
	
	
	it = time.time()
	it_time = it - start_time
	
	step = 3
	im.set_data(prism)
	Q.set_UVC(Ex[::step,::step], Ey[::step,::step])
	fig.suptitle(f"Iteraçoes:{iteration}\nErro de convergência: {delta_max:.6f}\nCriterio de convergencia: {tolerance}", fontsize=14)
	plt.pause(0.0001)

plt.ioff()
plt.show()
end_time = time.time()
dtime = end_time - start_time
print(f"Tempo de execução: {dtime:.4f} segundos")

