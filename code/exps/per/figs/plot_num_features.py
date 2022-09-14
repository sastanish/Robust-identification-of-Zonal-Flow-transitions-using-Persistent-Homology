import matplotlib.pyplot as plt
import numpy as np
import awkward as awk
from matplotlib import cm

per = awk.from_parquet('../per.parquet')
alpha = [0.001, 0.0016, 0.0027, 0.0046, 0.0077, 0.013, 0.021, 0.036, 0.06, 0.1, 0.17, 0.28, 0.46, 0.0012, 0.0021, 0.0035, 0.0059, 0.01, 0.016, 0.027, 0.046, 0.077, 0.13, 0.22, 0.36]
alpha.sort()
time = len(per[0,:,0,0])

features = np.empty((len(alpha),time))
for a in range(len(alpha)):
    for t in range(time):
        features[a,t] = len(per[a,t,:,0])

features = features/(256*200) #Normalizing by grid size

mean = np.mean(features,axis=-1)
yerr = np.std(features,axis=-1)

fig,axs = plt.subplots(nrows=1,ncols=1,figsize=(10,10))

tab = cm.get_cmap('tab20')
axs.errorbar(alpha,mean,yerr=yerr,fmt='x',label='$<N_f(n)>_t$',color=tab(0))

axs.legend()
axs.set_ylabel('$N_f$')
axs.set_xlabel('alpha')
axs.set_title('Average Number of Generators')

axs.set_xscale('log')


plt.savefig('number_of_features.png')
