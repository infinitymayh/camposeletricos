import numpy as np
import matplotlib.pyplot as plt
import time

def potential(i,j):
	
	if i in range(c_min,c_max+1) and j in range(c_min,c_max+1):
		return 1
	elif i == 0 or i == n-1 or j == 0 or j == n-1 :
		return 0
	else:
		
		a = prism[i+1][j]
		b = prism[i-1][j]
		c = prism[i][j+1]
		d = prism[i][j-1]
		
		return (a+b+c+d)/4

n = 101 #tamanho da matriz n x n
c_min = 40 #indice minimo do condutor
c_max = 60 #indice maximo do condutor

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
im = ax.imshow(prism, cmap='hot', origin='lower', vmin=0, vmax=1)
plt.colorbar(im)

start_time = time.time()
####### CALCULO
for iteration in range(0, 1000):
	for x in range(1,n,2):
		for y in range(1,n,2):
			
			if (x in conductor_x) and (y in conductor_y):
				pass
			else:
				prism2[x][y] = potential(x,y)
				delta = prism2 - prism

				
	for x in range(1,n):
		for y in range(1,n):
			
			if (x in conductor_x) and (y in conductor_y):
				pass
			else:
				prism[x][y] = potential(x,y)
				delta = prism - prism2
	it = time.time()
	it_time = it - start_time
	im.set_data(prism)
	ax.set_title(f"Potêncial V para prisma metálico com um condutor no centro\nIteração {iteration+1}\nTempo de execuçao: {it_time:.2f} segundos")
	plt.pause(0.01)

plt.ioff()
plt.show()
end_time = time.time()
dtime = end_time - start_time
print(f"Máximo de iterações! Tempo de execução: {dtime:.4f} segundos")

