import numpy as np
import hdf5plugin
import yt
from yt.visualization.volume_rendering.api import (Camera, Scene, create_volume_source)
from yt.visualization.volume_rendering.transfer_function_helper import (
    TransferFunctionHelper,
)
from yt.visualization.volume_rendering.transfer_functions import (
    MultiVariateTransferFunction, ColorTransferFunction,
)

print("yt.load:")
ds = yt.load("for_Matt_Turk/mkow075-ens-db620.00790000.nc")
print("ds.parameters:")
ds.parameters #ORF note: This displays nothing
print("ds.print_stats():")
ds.print_stats()
#print_stats is good except we should get rid of all Mpc, AU etc and do it in MKS/weather units
print("ds.field_list:") #This shows nothing! Bad! Should we not get all the vars?
ds.field_list
print("ds.derived_field_list:")#Also shows nothing!!
#Would it not be spectacular to have some useful derived fields?
#Perhaps we can recode LOFS/LOFT stuff.
#I mean, stuff like vorticity and velocity, already there...
ds.derived_field_list

# First, a 2D plot

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
s.save("full-xzplot.png",mpl_kwargs=dict(dpi=300))

# VOLUME RENDERING

# normal_vector points from camera to the center of the final projection.
# yt is [x,y,z] FYI.
normal_vector = [0.0, 1.0, 0.0]
# north_vector defines the "top" direction of the projection, which is positive z direction here.
north_vector = [0.0, 0.0, 1.0]

sc=yt.create_scene(ds, lens_type="perspective",field="winterp")
print("sc:")
print (sc)
source=sc[0]
print("source:")
print(source)
source.tfh.set_log(False)
#ORF BUG: If I make the small bound negative, it blows up
#even though we are set_log (False) above
source.tfh.set_bounds((1,70.0))
source.tfh.grey_opacity=True
source.tfh.plot("transfer_function.png",profile_field="winterp")

cam=sc.add_camera(ds,lens_type="perspective")
cam.resolution=(3840,2160)
cam.position=ds.domain_center+np.array([20,-80,23.0])*yt.units.kilometer
cam.switch_orientation(normal_vector=normal_vector, north_vector=north_vector)
cam.focus=ds.domain_center +np.array([0,0,0.0])*yt.units.kilometer
sc.annotate_axes()
sc.annotate_domain(ds,color=[1,1,1,0.5])
sc.camera.set_width(ds.quan(60,"km"))
im=sc.render()
sc.save("full-volume-dbz.png",sigma_clip=2.0)

'''
#sc.camera.set_width(ds.quan(20,"km"))
#source=sc.sources["dbz"]
#tf=yt.ColorTransferFunction((-65,65))
#tf.add_layers(4, w=0.01)
#source.set_transfer_function(tf)


tf=ColorTransferFunction((0,65))
tfh.tf.add_layers(8,colormap="cmyt.algae")
sc=Scene()
source=create_volume_source(ds.all_data(),"dbz")
tf=ColorTransferFunction((0,65))

tfh.tf.add_layers(8,colormap="cmyt.algae")
#mv=MultiVariateTransferFunction()
#tf.add_gaussian(0.0 ,0.01,[1.0,0.0,0.0,0.1])
#tf.add_gaussian(20.0,0.01,[0.0,1.0,0.0,0.2])
#tf.add_gaussian(40.0,0.01,[0.0,0.0,1.0,0.5])
#tf.map_to_colormap(0, 60, scale=40.0, colormap="cmyt.algae")

tfh = TransferFunctionHelper(ds)
tfh.set_field("dbz")
tfh.set_bounds((-40,60))
tfh.set_log(False)
tfh.build_transfer_function()
tfh.tf.add_layers(
    8,
    w=0.01,
    mi=-60.0,
    ma=70.0,
    col_bounds=[-60.0, 70.0],
    alpha=np.linspace(0.0,1.0,num=100),
    colormap="RdBu_r",
)
tfh.tf.map_to_colormap(0.0,70, colormap="Reds")
tfh.tf.map_to_colormap(-60, 0.0, colormap="Blues_r")
#tfh.plot(profile_field=("dbz"))
'''

