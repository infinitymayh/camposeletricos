import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time

def potential(i,j):
	
	if i == c_x and j in range(c_min,c_max+1):
		return -1
	elif i == 0 or i == n-1 or j == n-1 :
		return 0
	elif i == 0:
		return prism[1,j]
	elif j == 0:
		return prism[i,1]
	else:
		
		a = prism[i+1][j]
		b = prism[i-1][j]
		c = prism[i][j+1]
		d = prism[i][j-1]
		
		return (a+b+c+d)/4

####### CALCULOS PARA APENAS 1/4 DO PRISMA

n = 51 #tamanho da matriz n x n
c_min = 0 #indice minimo do condutor
c_max = 10 #indice maximo do condutor

prism = np.zeros((n,n))

#metade superior da placa direita
c_x = 10 #posição da placa no eixo x
for j in range(c_min,c_max+1):
		prism[c_x,j] = -1

plate_right_y = np.arange(c_min,c_max+1)


prism2 = np.ones((n,n))
delta = prism2-prism
tolerance = np.full((n,n), 0.001)



######### GRÁFICO

plt.ion()  # modo interativo ligado
fig = plt.figure(figsize=(6,6))

full = np.block([
		[np.flipud(np.fliplr(prism[1:,1:])), np.flipud(prism[1:,:])],
		[np.fliplr(prism[:,1:]), prism] 
	])
	


x = np.arange(full.shape[0])
y = np.arange(full.shape[1])
X, Y = np.meshgrid(x, y)

start_time = time.time()
####### CALCULO
for iteration in range(0, 1000):
	for x in range(0,n,2):
		for y in range(0,n,2):
			
			if (x == c_x) and (y in plate_right_y):
				pass
			else:
				prism2[x][y] = potential(x,y)
				delta = prism2 - prism

				
	for x in range(0,n):
		for y in range(0,n):
			
			if (x == c_x) and (y in plate_right_y):
				pass
			else:
				prism[x][y] = potential(x,y)
				delta = prism - prism2
	
	####### MONTANDO O PRISMA INTEIRO
	full = np.rot90(np.block([
		[np.flipud(np.fliplr(np.abs(prism[1:,1:]))), np.flipud(np.abs(prism[1:,:]))],
		[np.fliplr(prism[:,1:]), prism]
	]))
	
	dVy, dVx = np.gradient(full, y, x)
	Ex = -dVx
	Ey = -dVy
	
	
	it = time.time()
	it_time = it - start_time
	
	step = 3
	plt.clf()
	plt.quiver(X[::step,::step], Y[::step,::step], Ex[::step,::step], Ey[::step,::step],scale=0.1, color='r')
	plt.title(f"Campo elétrico para prisma metálico com duas placas capacitoras\nIteração {iteration+1}\nTempo de execuçao: {it_time:.2f} segundos", fontsize=16)
	plt.pause(0.01)

plt.ioff()
plt.show()
end_time = time.time()
dtime = end_time - start_time
print(f"Máximo de iterações! Tempo de execução: {dtime:.4f} segundos")

