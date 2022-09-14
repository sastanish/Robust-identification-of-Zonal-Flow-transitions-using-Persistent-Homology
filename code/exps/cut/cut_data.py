import numpy as np
import time as tc
import xarray as xr
import pandas as pd

def load_boutdataset(dirs,chunks={'t':10},num_files=8,**kwargs):
    ds = xr.open_mfdataset(dirs,parallel=True,chunks=chunks,concat_dim="x", combine="nested",data_vars='minimal', coords='minimal', compat='override')
    ends = [34+36*i for i in range(7)]
    drops = [i for i in range(30)]+[int(0+i) for i in ends]+[int(1+i) for i in ends]+[int(2+i) for i in ends]+[int(3+i) for i in ends]+[287-i for i in range(30)]
    ds = ds.drop_sel(x=drops)
    return ds.isel(t=slice(-200,-1))

## Target dimensions ##
alpha = [0.001, 0.0016, 0.0027, 0.0046, 0.0077, 0.013, 0.021, 0.036, 0.06, 0.1, 0.17, 0.28, 0.46, 0.0012, 0.0021, 0.0035, 0.0059, 0.01, 0.016, 0.027, 0.046, 0.077, 0.13, 0.22, 0.36]
alpha.sort()
kappa = '0.1'

removable_data = ['BOUT_VERSION', 't_array', 'iteration', 'zperiod', 'MXSUB', 'MYSUB', 'MZSUB', 'PE_XIND', 'PE_YIND', 'MYPE', 'MXG', 'MYG', 'MZG', 'nx', 'ny', 'nz', 'MZ', 'NXPE', 'NYPE', 'NZPE', 'ZMAX', 'ZMIN', 'ixseps1', 'ixseps2', 'jyseps1_1', 'jyseps1_2', 'jyseps2_1', 'jyseps2_2', 'ny_inner', 'dx', 'dy', 'dz', 'g11', 'g22', 'g33', 'g12', 'g13', 'g23', 'g_11', 'g_22', 'g_33', 'g_12', 'g_13', 'g_23', 'J', 'Bxy', 'G1', 'G2', 'G3', 'wall_time', 'wtime', 'ncalls', 'ncalls_e', 'ncalls_i', 'wtime_rhs', 'wtime_invert', 'wtime_comms', 'wtime_io', 'wtime_per_rhs', 'wtime_per_rhs_e', 'wtime_per_rhs_i', 'tt', 'hist_hi', 'run_id', 'run_restart_from']

## Transform Data ##
data_sets = [load_boutdataset(f'/sciclone/pscr/sastanish/hw/data/{kappa}/{alp}/BOUT.dmp.*.nc').drop_vars(removable_data) for alp in alpha]
new_data = xr.concat(data_sets, pd.Index(data=alpha,name="alpha"))

new_data.to_netcdf(f"eq_data.nc")
