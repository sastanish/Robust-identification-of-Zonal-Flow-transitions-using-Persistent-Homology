import awkward as awk

per = awk.from_parquet('per.parquet')
awk.to_parquet(per[per[:,:,:,0]==0],'b0_per.parquet')
awk.to_parquet(per[per[:,:,:,0]==1],'b1_per.parquet')
