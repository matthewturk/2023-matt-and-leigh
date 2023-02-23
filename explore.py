import hdf5plugin
import yt

ds = yt.load("for_Matt_Turk/mkow075-ens-db620.00790000.nc")
ds.parameters
s = ds.r[:,:,10.0].plot("vortmag")
s.save()
