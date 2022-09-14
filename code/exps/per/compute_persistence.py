import numpy as np
import awkward as awk
import xarray as xr
import gudhi

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
	percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
	filledLength = int(length * iteration // total)
	bar = fill * filledLength + '-' * (length - filledLength)
	print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
	if iteration == total:
		print()

ds = xr.open_dataset(f'../cut/normed_n_data.nc')
dims = ds.dims
dim_names = [dim for dim in ds.dims]

form = """
{
  "class": "ListOffsetArray64",
  "offsets": "i64",
  "content": {
              "class": "ListOffsetArray64",
              "offsets": "i64",
              "content": {
                  "class": "ListOffsetArray64",
                  "offsets": "i64",
                  "content": {
                      "class": "NumpyArray",
                      "primitive": "float64",
                      "form_key": "node3"
                  },
              "form_key": "node2"
              },
          "form_key": "node1"
          },
  "form_key": "node0"
}
"""

builder = awk.layout.LayoutBuilder32(form)

total = 2*dims['alpha']*dims['t']
i=0

printProgressBar(i,total)
for var in ['n']:
    for a in range(dims['alpha']):
        builder.begin_list()
        for t in range(dims['t']):
            builder.begin_list()
            cc = gudhi.PeriodicCubicalComplex(top_dimensional_cells=ds[var][a,t,:,0,:].values,periodic_dimensions=[False, True])
            printProgressBar(i,total)
            i+=1
            for (f,(b,d)) in cc.persistence():
                builder.begin_list()
                builder.float64(f)
                builder.float64(b)
                builder.float64(d)
                builder.end_list()
            builder.end_list()
        builder.end_list()
    layout = builder.snapshot()
    array = awk.Array(layout)
awk.to_parquet(array,f'./per.parquet')
