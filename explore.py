import hdf5plugin
import yt

ds = yt.load("for_Matt_Turk/mkow075-ens-db620.00790000.nc")
ds.parameters

#s = ds.r[:,:,0.0376].plot("vortmag")
s = ds.r[:,0.0,:].plot("vortmag")
s.set_cmap(("vortmag"),"nipy_spectral")
s.set_log(("vortmag"),False)
s.set_zlim(("vortmag"),zmin=(4e-3,"1/s"),zmax=(0.2,"1/s"))
s.set_buff_size(2000)
s.set_figure_size(10)
print(list(s.plots)[0])
plot = s.plots[list(s.plots)[0]]
print(plot)
ax=plot.axes
img=ax.images[0]
print(img)
#following does nothing to smooth plot (seems to be pixel based, no interpolation)
img.set_interpolation("bicubic")
s.save("full.png",mpl_kwargs=dict(dpi=300))
