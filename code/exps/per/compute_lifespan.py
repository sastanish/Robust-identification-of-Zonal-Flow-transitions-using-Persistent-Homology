import matplotlib.pyplot as plt
import numpy as np
import awkward as awk

per = awk.from_parquet('per.parquet')
awk.to_parquet(per[:,:,:,2]-per[:,:,:,1],'lifespans.parquet')
