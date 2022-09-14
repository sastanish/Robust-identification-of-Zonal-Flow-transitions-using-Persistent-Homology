import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

alpha = [0.001, 0.0016, 0.0027, 0.0046, 0.0077, 0.013, 0.021, 0.036, 0.06, 0.1, 0.17, 0.28, 0.46, 0.0012, 0.0021, 0.0035, 0.0059, 0.01, 0.016, 0.027, 0.046, 0.077, 0.13, 0.22, 0.36]
alpha.sort()

def energy(arr):
    grad = np.square(arr.differentiate('x'))+np.square(arr.differentiate('z'))
    print('ke grad')
    return 0.5*grad.integrate(coord=('x','z'))

ds = xr.open_dataset('../cut/eq_data.nc')
zone = ds['phi'].mean('z')

Ze = np.square(zone.differentiate('x')).integrate(coord='x')*128
np.save('Ze',Ze)
Ke = energy(ds['phi'])
np.save('Ke',Ke)
