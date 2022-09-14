#!/bin/bash
for k in 0.1
do
	for a in 0.001 0.0012 0.0016 0.0027 0.0035 0.0046 0.0059 0.0077 0.01 0.013 0.016 0.021 0.027 0.036 0.046 0.06 0.077 0.1 0.13 0.17 0.22 0.28 0.36 0.46
	do
		mvp2run -v -m cyclic -c 8 -a -e OMP_NUM_THREADS=2 /sciclone/home20/sastanish/install/BOUT-dev/examples/hasegawa-wakatani/hw restart nout=200 TIMESTEP=100.0 SOLVER:type=rk4 SOLVER:timestep=0.1 hw:alpha=$a hw:kappa=$k -d /sciclone/pscr/sastanish/hw/data/$k/$a >& /sciclone/pscr/sastanish/hw/data/$k/$a/OUT_ext
	done
done
