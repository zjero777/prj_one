import numpy as np
matrix = np.zeros((500, 500))
x = 240 
y = 280 
radius = 10 
mask = np.ogrid[x-radius:x+radius+1, y-radius:y+radius+1]
matrix[mask]=1
print(matrix)
