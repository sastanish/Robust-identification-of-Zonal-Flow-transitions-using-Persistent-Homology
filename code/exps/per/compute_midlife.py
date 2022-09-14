import matplotlib.pyplot as plt
import numpy as np
import awkward as awk

per = awk.from_parquet('per.parquet')
midlife = (per[:,:,:,1]+per[:,:,:,2])/2
awk.to_parquet(midlife,'midlife.parquet')
