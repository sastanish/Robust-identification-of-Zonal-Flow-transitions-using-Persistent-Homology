import awkward as awk
import numpy as np
import matplotlib.pyplot as plt

lifespans = awk.from_parquet('../lifespans.parquet')
alpha = [0.001, 0.0016, 0.0027, 0.0046, 0.0077, 0.013, 0.021, 0.036, 0.06, 0.1, 0.17, 0.28, 0.46, 0.0012, 0.0021, 0.0035, 0.0059, 0.01, 0.016, 0.027, 0.046, 0.077, 0.13, 0.22, 0.36]
alpha.sort()
lifespans = lifespans[lifespans!=np.inf]
bins = np.logspace(-3, 0, 50)

for i in range(len(alpha)):
    print(i)
    fig,axs = plt.subplots(tight_layout=True,figsize=(5,5))
    axs.barh(bins[:-1],np.histogram(awk.flatten(lifespans[i]),bins=bins, density=True)[0], align='edge', height=np.diff(bins), color='tab:blue')
    axs.set_title('n')
    plt.xscale('log')
    plt.yscale('log')
    #axs.set_xlim((10**-5,10**3))
    fig.suptitle(f'alpha:{alpha[i]}')
    plt.savefig(f'dists/lifespan_{alpha[i]}.png')
    plt.close()
