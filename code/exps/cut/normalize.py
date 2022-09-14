import xarray as xr

ds = xr.open_dataset('eq_data.nc')
ds = ds.drop_vars(['vort', 'phi'])
norm = ds-ds.mean(dim='z')
norm.to_netcdf('normed_n_data.nc')
