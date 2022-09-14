import awkward as awk
import numpy as np
import matplotlib.pyplot as plt

midlife = awk.from_parquet('../midlife.parquet')
alpha = [0.001, 0.0016, 0.0027, 0.0046, 0.0077, 0.013, 0.021, 0.036, 0.06, 0.1, 0.17, 0.28, 0.46, 0.0012, 0.0021, 0.0035, 0.0059, 0.01, 0.016, 0.027, 0.046, 0.077, 0.13, 0.22, 0.36]
midlife = midlife[midlife!=np.inf]

for i in range(len(alpha)):
    print(i)
    fig,axs = plt.subplots(tight_layout=True,figsize=(5,5))
    axs.hist(awk.flatten(midlife[i]),bins=30, color='tab:blue')
    axs.set_title('n')
    plt.yscale('log')
    axs.set_xlim((-1,1))
    fig.suptitle(f'alpha:{alpha[i]}')
    plt.savefig(f'dists/midlife_{alpha[i]}.png')
    plt.close()
