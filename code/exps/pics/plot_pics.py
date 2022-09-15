import matplotlib.pyplot as plt
import xarray as xr

ds = xr.open_dataset('../cut/normed_n_data.nc')
a = 0
t = -1
alpha = ds.coords['alpha'].to_numpy()
print(alpha)

fig, ax = plt.subplots()
ax.imshow(ds['n'][a,t,:,0,:])
plt.savefig(f'alpha{alpha[a]}_t{t}.svg')
plt.close()
