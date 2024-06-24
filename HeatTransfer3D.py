import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

#parameters
a = 2346   # thermal diffusivity air 40C (mm2/s)
length = 5000  # room length (mm)
time = 60  # seconds
nodes = 50  # grid nodes 

#spatial steps
dx = length / nodes
dy = length / nodes
dz = length / nodes

#time step
dt = dx**2 / (5 * a) 

#temperature grid
u = np.zeros((nodes, nodes, nodes)) + 40  # initial temperature 40°C

#boundary conditions
u[0, :, :] = 20
u[-1, :, :] = 20
u[:, 0, :] = 20
u[:, -1, :] = 20
u[:, :, 0] = 20
u[:, :, -1] = 20

#visualization setup
fig = plt.figure()
axis = fig.add_subplot(111, projection='3d')

#heat distribution
counter = 0

while counter < time:
    w = u.copy()
    
    for i in range(1, nodes - 1):
        for j in range(1, nodes - 1):
            for k in range(1, nodes - 1):
                dd_ux = (w[i-1, j, k] - 2*w[i, j, k] + w[i+1, j, k]) / dx**2 #finite difference method
                dd_uy = (w[i, j-1, k] - 2*w[i, j, k] + w[i, j+1, k]) / dy**2
                dd_uz = (w[i, j, k-1] - 2*w[i, j, k] + w[i, j, k+1]) / dz**2

                u[i, j, k] = dt * a * (dd_ux + dd_uy + dd_uz) + w[i, j, k]
    

    counter += dt

    print(f"t = {counter:.3f} s, Average temperature = {np.average(u):.2f} °C")

    # Plotting a slice of the temperature distribution
    axis.clear()
    x, y = np.meshgrid(np.linspace(0, length, nodes), np.linspace(0, length, nodes))
    z = u[:, :, nodes // 2]

    axis.plot_surface(x, y, z, cmap='jet', vmin=0, vmax=100)
    axis.set_title(f" Avg Temp: {np.average(u):.2f} °C, Temperature distribution at t: {counter:.3f} s")
    plt.pause(0.01)



plt.show()
