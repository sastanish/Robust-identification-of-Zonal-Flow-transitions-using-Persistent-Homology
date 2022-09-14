import numpy as np
import matplotlib.pyplot as plt
alpha = [0.001, 0.0016, 0.0027, 0.0046, 0.0077, 0.013, 0.021, 0.036, 0.06, 0.1, 0.17, 0.28, 0.46, 0.0012, 0.0021, 0.0035, 0.0059, 0.01, 0.016, 0.027, 0.046, 0.077, 0.13, 0.22, 0.36]
alpha.sort()

Ze = np.load('Ze.npy')
Ke = np.load('Ke.npy')

fig,ax = plt.subplots(figsize=(10,10))
ax.errorbar(alpha,np.mean(Ze/Ke,axis=(1,2)),yerr=np.std(Ze/Ke,axis=(1,2)),linestyle='',marker='.',color='tab:red')
ax.set_xlabel('alpha')
ax.set_ylabel('Z_e/K_e')
ax.set_xscale('log')
ax.set_title('Ratio of Zonal to Total Kinetic Energy')
plt.savefig('energy_ratio.png')
