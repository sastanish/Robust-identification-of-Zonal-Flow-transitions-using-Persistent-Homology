import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import scipy.signal as sig

ds = xr.open_dataset('../cut/normed_n_data.nc')
alpha = ds.coords['alpha'].to_numpy()
x = ds.dims['x']

power = np.square(np.abs(np.fft.rfft(ds['n'],axis=2)))
freq = np.fft.rfftfreq(x)
#freq, power = sig.welch(ds['n'],axis=2,scaling='spectrum')

avg_power = np.mean(power,axis=(-1,-2,1))

for a,alf in enumerate(alpha):
    print(a)
    fig, ax = plt.subplots(figsize=(5,5))
    ax.loglog(freq,avg_power[a,:])
    ax.set_title(f'Alpha:{alf} Power Spectrum')
    ax.set_ylabel('$V^2$')
    ax.set_xlabel('$k_x$')
    #ax.set_ylim((10**-10,10**-2))
    plt.savefig(f'figs/{alf}_spec.png')
    plt.close()
