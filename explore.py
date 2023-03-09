import hdf5plugin
import yt

print("yt.load:")
ds = yt.load("for_Matt_Turk/mkow075-ens-db620.00790000.nc")
print("ds.parameters:")
ds.parameters #ORF note: This displays nothing
print("ds.print_stats():")
ds.print_stats()
#print_stats is good except we should get rid of all Mpc, AU etc and do it in MKS/weather units
print("ds.field_list:") #This shows nothing! Bad! Should we not get all the vars?
ds.field_list
print("ds.derived_field_list:")#Also shows nothing
ds.derived_field_list

#s = ds.r[:,:,0.0376].plot("vortmag")
s = ds.r[:,0.0,:].plot("vortmag")
s.set_cmap(("vortmag"),"nipy_spectral")
s.set_log(("vortmag"),False)
s.set_zlim(("vortmag"),zmin=(4e-3,"1/s"),zmax=(0.2,"1/s"))
#ORF not sure making this bigger helps us?
s.set_buff_size(2000)
s.set_figure_size(10)
print(list(s.plots)[0])
plot = s.plots[list(s.plots)[0]]
print(plot)
ax=plot.axes
img=ax.images[0]
print(img)
#following does nothing to smooth plot (seems to be pixel based, no interpolation)
#This is because yt does its own buffering and some ofthe matplotlib stuff is NOT
#available. This has to do with the typical highly irregular grid/mesh layout of astrophysics data 
#img.set_interpolation("bicubic")
#ORF so there is this mpl_kwargs dpi way to do what we expect, but there is no current way
#to do nice smooth interpolation. Worry about that later!
s.save("full.png",mpl_kwargs=dict(dpi=300))
