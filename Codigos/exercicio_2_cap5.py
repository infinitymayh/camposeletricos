import numpy as np
import matplotlib.pyplot as plt
import time

def potential(i,j):
	
	if i in range(c_min,c_max+1) and j in range(c_min,c_max+1):
		return 1
	elif i == n-1 or j == n-1 :
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

# condutor metalico com 20% da área total do prisma
prism = np.zeros((n,n))

for i in range(c_min,c_max+1):
	for j in range(c_min,c_max+1):
		prism[i,j] = 1

conductor_x = np.arange(c_min,c_max+1)
conductor_y = np.arange(c_min,c_max+1)

prism2 = np.ones((n,n))
delta = prism2-prism
tolerance = np.full((n,n), 0.001)

######### GRÁFICO
plt.ion()  # modo interativo ligado
fig, ax = plt.subplots()
full = np.block([
		[np.flipud(np.fliplr(prism[1:,1:])), np.flipud(prism[1:,:])],
		[np.fliplr(prism[:,1:]), prism] 
	])
im = ax.imshow(full, cmap='hot', origin='lower', vmin=0, vmax=1)
plt.colorbar(im)

start_time = time.time()
####### CALCULO
for iteration in range(0, 1000):
	for x in range(0,n,2):
		for y in range(0,n,2):
			
			if (x in conductor_x) and (y in conductor_y):
				pass
			else:
				prism2[x][y] = potential(x,y)
				delta = prism2 - prism

				
	for x in range(0,n):
		for y in range(0,n):
			
			if (x in conductor_x) and (y in conductor_y):
				pass
			else:
				prism[x][y] = potential(x,y)
				delta = prism - prism2
	
	####### MONTANDO O PRISMA INTEIRO
	full = np.block([
		[np.flipud(np.fliplr(prism[1:,1:])), np.flipud(prism[1:,:])],
		[np.fliplr(prism[:,1:]), prism] 
	])
	it = time.time()
	it_time = it - start_time
	im.set_data(full)
	ax.set_title(f"Potêncial V para prisma metálico com um condutor no centro\nIteração {iteration+1}\nTempo de execuçao: {it_time:.2f} segundos")
	plt.pause(0.01)

plt.ioff()
plt.show()
end_time = time.time()
dtime = end_time - start_time
print(f"Máximo de iterações! Tempo de execução: {dtime:.4f} segundos")

