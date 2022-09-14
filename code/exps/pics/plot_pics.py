import matplotlib.pyplot as plt
import xarray as xr

ds = xr.open_dataset('../cut/normed_n_data.nc')
a = 
t = 
alpha = ds.coords['alpha']
print(alpha)

fig, ax = plt.subplots()
ax.imshow(ds[f][a,t,:,0,:])
plt.savefig(f'alpha{alpha[a]}_t{t}.png')
plt.close()
