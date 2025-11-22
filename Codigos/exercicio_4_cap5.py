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

def eletric_field(i,j):
	return - (potential(i+1,j)-potential(i-1,j))/2,  - (potential(i,j+1)-potential(i,j-1))/2
	
####### CALCULOS PARA APENAS 1/4 DO PRISMA

n = 51 #tamanho da matriz n x n
c_min = 0 #indice minimo do condutor (altura)
c_max = 10 #indice maximo do condutor (altura)

prism = np.zeros((n,n))

#metade superior da placa direita
c_list = [1,5,10,15,20,25,30,35,40,45,50] #lista de diferentes separações
distances = [d*2 for d in c_list]

fringe_campos = []

for d in c_list:
	print(f"Calculando fringe para d = {d}")
	c_x = d #posição da placa no eixo x
	for j in range(c_min,c_max+1):
			prism[c_x,j] = -1

	plate_right_y = np.arange(c_min,c_max+1)


	prism2 = np.ones((n,n))
	delta = prism2-prism
	tolerance = np.full((n,n), 0.001)



	start_time = time.time()
	####### CALCULO
	for iteration in range(0, 100):
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
		
	E_abs = np.sqrt(Ex**2 + Ey**2)
	region = E_abs[0:10,0:10]
	fringe_mean = np.mean(region)
	fringe_campos.append(fringe_mean)
		
	it = time.time()
	it_time = it - start_time
		
		
plt.plot(distances, fringe_campos, "o-")
plt.xlabel("Distancia entre as placas")
plt.ylabel("Campo de fringing")
plt.title(f"Fringing field vs separação entre placas\nTempo de execuçao: {it_time:.2f} segundos", fontsize=16)
end_time = time.time()
dtime = end_time - start_time
print(f"Máximo de iterações! Tempo de execução: {dtime:.4f} segundos")
plt.show()


