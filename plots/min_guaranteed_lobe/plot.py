import numpy as np
from numpy import pi
from matplotlib import pyplot as plt

from aux_funcs import *


''''""""""""""""""""""""""""""""""""""""""""""""""""""""""
 SOME IMPORTANT DEFINITIONS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""'''

# Conversion from radians to degrees, and viceversa. 
rad_2_deg 	= 180/pi
deg_2_rad	= pi/180


max_dist_m 	= 5 	# Max measured distance at which the device was able to WU!
min_dist_m	= 0.1	# The minimum distance from which the simulation can be approximated to a power series of the form A.1/x^3 	
dists_n 	= 7		# Number of distances used during measurements.
angles_n 	= 7		# Number of angles used during measurements.

lines_n 	= 100 	# Number of lines to be used from the simulated values (each corresponding to a distance r)

# The used angles between the reader's axis and tag position, in degrees. 
thetas_d 	= [ 0, 15, 30, 45, 60, 75, 90 ]
thetas_r	= 	np.array(thetas_d) * deg_2_rad
# The used distances between the reader's coil's center and the tag position, in meters.
dists_m 	= [ 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.40]

# The orientation angles for the tag, in degrees
phis_d 		= [0, 10, 20, 30, 40, 50, 60, 70, 80, 90 ]
#phis_d 		= [0, 15, 30, 60, 90 ]


''''""""""""""""""""""""""""""""""""""""""""""""""""""""""
 DECLARATION OF GLOBAL VARS 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""'''


B 			= {}	# Magnetic field (B) module (in Tesla)
B_er 		= {}	# Magnetic field (B) on versor e_r (in Tesla)  	
B_et 		= {}	# Magnetic field (B) on versor e_theta (in Tesla)
B_rot 		= {}	# Magnetic field resulting from the rotation of the reader (in Tesla)



gamma_r 	= {}	# Angle gamma of B wrt e_r (in radians)
gamma_d 	= {}	# Angle gamma of B wrt e_r (in degrees)
gamma_abs_r = {}	# Anlge gamma of B with respect to the horizontal (in radians)
gamma_abs_d = {}	# Angle gamma of B with respect to the horizontal (in degrees)
gamma_rot_r = {}	# Angle gamma of B wrt e_r resulting from the rotation of the reader (in radians)  

r_m			= []	# Distances over e_r in which the simulation obtained values, in meters.



''''""""""""""""""""""""""""""""""""""""""""""""""""""""""
 USEFUL LOCAL FUNCTIONS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""'''

def plot_lobe( ax, lobe ):
	( x_lobe, y_lobe ) = get_lobe_polar( r_m, thetas_r, lobe )
	ax.plot(x_lobe,y_lobe,'k:')
	ax.fill_between(x_lobe,0,y_lobe, alpha=0.075, zorder=1,color='k')


def setup_plot( ax ):

	ax.set_ylim( 0,  max( r_m ) + min( r_m ) )
	ax.set_rmax( round(max( r_m )*10)/10  )


	ax.set_thetamax( max( thetas_d ) )
	ax.set_xticks( deg_2_rad * np.linspace(0,  max( thetas_d ) , angles_n, endpoint=True) )
	ax.set_rticks( dists_m )
	return ax


''''""""""""""""""""""""""""""""""""""""""""""""""""""""""
 SET UP OF PLOT WINDOW 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""'''

plt.close('all')


# Dimensions of the figure to be generated
#figLength = 7
#figHeight = figLength*0.85
#figLength = 20
#figHeight = figLength*0.85

#plt.rcParams["figure.figsize"] = [figLength, figHeight]
#plt.rcParams["figure.autolayout"] = True
plt.rcParams["font.family"] = "serif"
#plt.rc('xtick',labelsize=13)
#plt.rc('ytick',labelsize=13)
plt.rc('xtick',labelsize=5)
plt.rc('ytick',labelsize=5)


''''""""""""""""""""""""""""""""""""""""""""""""""""""""""
 GETTING THE SIMULATED FIELD VALUES 

The FEMM42 program can offer the components of the magnetic field in a point, both normal and
tangential to the traced line. In our case, the line is the versor e_r, so the normal  component is the component e_theta and the tangential one is the component on e_r. 
 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""'''

# theta_d will have the angle value in degrees.
# theta is the string version of it to be used to access dictionaries.
for theta_d in thetas_d:
	theta = str(theta_d)
	
	# Getting the component from e_theta and the position values
	values 		= getValuesFromFile( "/norm_" + theta )
	r_m 		= values[0][:lines_n] 
	B_et[theta] = values[1][:lines_n]
	
	# Getting the component over e_r. The position values are the same as before.
	values 		= getValuesFromFile( "/tan_" + theta )
	B_er[theta] = values[1][:lines_n]

	# The field module is computed. 
	B[theta] 	= np.sqrt( B_et[theta]**2 + B_er[theta]**2 )
	
	# The field angle wrt e_r (gamma) is computed. 
	gamma_r[theta] 		= np.arctan( B_et[theta] / B_er[theta] )
	gamma_d[theta] 		= gamma_r[theta] * rad_2_deg 
	gamma_abs_r[theta] 	= gamma_r[theta] + theta_d * deg_2_rad
	gamma_abs_d[theta]	= gamma_d[theta] + theta_d

if 0:	
	print("B_et", B_et)
	print("B_er",B_er)	 
	print("B", B)
	print("gamma_d", gamma_d)
	print("gamma_abs_d", gamma_abs_d)
	

''''""""""""""""""""""""""""""""""""""""""""""""""""""""""
 QUIVER  
 
In case we want to, we could plot the obtained magnetic field vector for each point of the cuadrant.  
"""""""""""""""""""""""""""""""""""""""""""""""""""""""'''
if 0:
	# The 4 variables needed to plot (_pl) a quiver
	t_pl = [] # The angle (theta)
	r_pl = [] # The radius (r)
	u_pl = [] # The component over the horizontal (u)
	v_pl = [] # The component over the vertical (v)

	for i in range(angles_n):
		t_pl = np.append(t_pl, np.full( lines_n, gamma_r[i]), axis=0)
		r_pl = np.append(r_pl, r_m , axis=0)
		
		
	scale = 0.15 # This scale factor is arbitrary and only used to scale the size of the arrows.
	
	for theta in angles_d:
		theta = str(theta)
		u_pl = np.append( u_pl, scale*np.sin(gamma_abs_r[theta] ) )
		v_pl = np.append( v_pl, scale*np.cos(gamma_abs_r[theta] ) )

	ax.quiver(t_pl, r_pl, v_pl , u_pl, scale=1/scale, width=scale/100, clip_on = False, zorder=100 )

	plt.show()
	

''''""""""""""""""""""""""""""""""""""""""""""""""""""""""
 ROTATING theta READER 
 
We already have the vector B(r, theta) for each point of space.
Now we need to rotate the reader to simulate the hand movement. 
This is done because there is a chance that a tag is positioned in a way it cannot get enough field through it, but that the magnetic field intesity would be enough to wake it up had it been oriented somehow differently. 
To simulate the movement of the arm, the reader is rotated 90 degrees. 
Each time step is represented by a different rotation angle alpha. 
To avoid interpolating data, the same set of angles theta are used.
Symmetry is assumed in both for the readers rotation axis and its ortogonal plane. 
Therefore, by rotating the reader 15 deg, the values on the 0 deg vector are copied to the new 15 deg vector. The same happens with 15 deg and 30 deg, and so on. 
Thanks to the assumed symmetry, the 0 deg vector is filled with the 15 deg one. On the next step it will be filled with the 30 deg and so on. 
e.g. 
					 rotation
0 deg 	: AAAAAAAAA	---------> 	BBBBBBBBB	--------->	CCCCCCCCC 	
15 deg	: BBBBBBBBB				AAAAAAAAA				BBBBBBBBB
30 deg	: CCCCCCCCC				BBBBBBBBB				AAAAAAAAA
45 deg	: EEEEEEEEE   			CCCCCCCCC				BBBBBBBBB

Note that this is only valid because the vector B(r,theta) has its angle expressed as relative to the versor e_r. 


@ToDo: To replicate a more natural rotation, it should not be done along the reader's coil's center, but rather ~0.5 m behind, simulating the rotation of the arm. 
This requires a far more complex computation.   
"""""""""""""""""""""""""""""""""""""""""""""""""""""""'''

alphas_d = thetas_d # Set of angles that represent each time step of the rotation. 

# alpha_d will have the angle value in degrees.
# alpha is the string version of it to be used to access dictionaries.
for alpha_d in alphas_d:
	alpha = str(alpha_d)
	
	B_rot[alpha] 		= {} 	# For each time step (angle alpha), we will have a dictionary representing the magnetic field intesity in the whole space.  
	gamma_rot_r[alpha] 	= {} 	# Equivalently, for each time step we will have a dictionary for the magnetic field angle wrt e_r. 
	
	# theta_d will have the angle value in degrees.
	# theta is the string version of it to be used to access dictionaries.
	for theta_d in thetas_d:
		theta = str(theta_d)
		
		# In the initial scenario, for each angle theta there is a set of magnetic field intensity and angle gamma. The swype angle is which of those sets from the original scenario will be loaded into the new set alpha. 
		# e.g. If we have rotated the reader 30 deg, in the place of theta = 45 deg we will have to place the original values for theta = 45 - 30 deg = 15 deg.   
		swypeAng = str( abs( theta_d - alpha_d ) )
		B_rot		[alpha][theta] = B		[ swypeAng ]
		gamma_rot_r	[alpha][theta] = gamma_r[ swypeAng ]

if 0:		
	print(B_rot)	
	print( gamma_rot_r['0']['0'] )

''''""""""""""""""""""""""""""""""""""""""""""""""""""""""
 GETTING Bth @ 5m  for theta=0, phi=0 
 
Knowing that in the best possible position and orientation (theta = 0, phi = 0), the tag could be woke up at r = 5 m, we find the magnetic field that was going through it and call it Bth (threshold magnetic field). 

For simplicity and to avoid being unnecessarily demanding with the simulation, the values were obtianed only until 40 cm, so they have to be scaled. 

This is still useful to obtain the shape of the lobe, and then it can be scaled up again. 

"""""""""""""""""""""""""""""""""""""""""""""""""""""""'''	

# A first set of values are skipped to because the magentic field decay can be approximated to A.1/r^3 only after a considerable distance from the coil.

'''
@ToDo: Compute this skip from the min_dist_m, and not arbitrarily. 
'''
skip = 10

# The intesity values are approximated to obtain the coefficient A. 
opot, pcov = curve_fit( decay, r_m[skip:], B['0'][skip:] )
A = opot[0]

# The approximation is used (with the coefficient A) to obtain the magnetic field intensity that the tag let thorugh at the max distance. 
Bth_real = decay( max_dist_m, A )

# The previous value is disregarded momentarily to use a scaled down version. 
# Once the lobe has been computed, it should be scaled up using the Bth_real/Bth ratio.
Bth = B['0'][lines_n -1]

if 1:
	print("Bth: ", Bth)

''''""""""""""""""""""""""""""""""""""""""""""""""""""""""
 ROTATING THE TAG 

The minimium guaranteed area will be that in which:
* For every possible tag orientation phi
* At least for one time step alpha
* The B through the tag is greater than Bth

That being said, the lobe boundary (r_max) for each angle theta is given by the maximum distance r in which B(r,theta) satisfies the aforementioned conditions. 

Therefore, it will be computed as: 

for each phi:
	
	Para cada tiempo debo hallar un lobulo. 
	Luego estos son los que superpongo. 
	Me quedo con el lobulo MAXIMO. 


	for each alpha:
		for each theta: 
			compute the B thorugh the tag considering that the orientation phi affects merely with the (co)sine of the angle between phi and the B direction gamma. 
			

"""""""""""""""""""""""""""""""""""""""""""""""""""""""'''	


### @ToDo: Phis_d should be more granular!!
#phis_d = thetas_d	

B_rot_tag 		= {}
B_max_rot_tag 	= {}
r_max_rot_tag 	= {}

B_tgt = np.full( lines_n, Bth )

for phi_d in phis_d:
	phi = str(phi_d)
	
	B_rot_tag[phi] 		= {}
	B_max_rot_tag[phi] 	= {}
	r_max_rot_tag[phi] 	= {}
	
	for alpha_d in alphas_d:
		alpha = str(alpha_d)
		
		B_max = 0
		index_max = 0
		diff = []
		B_thr_tag_diff = []
		
		thisPhi = np.full( lines_n, phi_d )
		
		B_rot_tag[phi][alpha] 		= {}
		B_max_rot_tag[phi][alpha] 	= {}
		r_max_rot_tag[phi][alpha] 	= {}
		
		for theta_d in thetas_d:
			theta = str(theta_d)
				
			diff = abs( thisPhi - gamma_rot_r[alpha][theta]*rad_2_deg )*deg_2_rad
			
			factor = np.sin( diff )
			B_rot_tag[phi][alpha][theta] = B_rot[alpha][theta]*factor
				
			B_thr_tag_diff = B_rot_tag[phi][alpha][theta] - B_tgt
			
			for i in range(len(B_thr_tag_diff)):
				if B_thr_tag_diff[i] > 0:
					index_max = i
			if 0:
				print( "phi: ", phi, "\talpha: ", alpha, "\ttheta: ", theta, "\tB: ", B_rot_tag[phi][alpha][theta] ) 
				print("Diffs: ", B_thr_tag_diff )			
				print(index_max)
			
			r_max_rot_tag[phi][alpha][theta] = r_m[index_max] 

if 0:
	print(r_max_rot_tag)


''''""""""""""""""""""""""""""""""""""""""""""""""""""""""
 TIME FLATTENING: The max lobe over time
 
Now that we have for each phi and alpha what is the area where the tag would WU! at some point, we can superpose them to obtain the lobe (for each phi) where the tag  would WU! at least at one given time. 
 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""'''

r_max_flat_time = {}

for phi_d in phis_d:
	phi = str(phi_d)
	
	r_max_flat_time[phi] = {}

	for theta_d in thetas_d:
		theta = str(theta_d)

		r_maxs_list = []
		
		for alpha_d, i in zip( alphas_d, range( len(alphas_d) ) ): 
			alpha = str(alpha_d)	
			r_maxs_list.append(r_max_rot_tag[phi][alpha][theta])
			
		r_max_flat_time[phi][theta] = max( r_maxs_list )	
		
		if 0: 
			print("r_max_rot_tag[",phi,"][",alpha,"][",theta,"] \t", r_max_rot_tag[phi][alpha][theta])
			print("r_max_flat_time[",phi,"][",theta,"]\t", r_max_flat_time[phi][theta] )	 
			print("list: ", r_maxs_list )
			print("max: ",max( r_maxs_list ) ) 
			
		
if 0:			
	print( r_max_flat_time )



''''""""""""""""""""""""""""""""""""""""""""""""""""""""""
 MINIMUM LOBE
 
Now that we have the lobes inside which the tag would WU at least at some given time, we must guarantee that it will WU! no matter which orientation it has. 

That is done by taking the minimum lobe edge among the len(phis_d) options for each angle theta.  
 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""'''

guar_lobe = np.zeros( angles_n )


for theta_d, i_theta in zip( thetas_d, range( angles_n )):
	theta = str(theta_d)
	
	r_mins_list = []
	
	for phi_d, i_phi in zip( phis_d, range( len( phis_d ) ) ):
		phi = str(phi_d)
		
		r_mins_list.append(r_max_flat_time[phi][theta])
		
	guar_lobe[i_theta] = ( min( r_mins_list ) ) 

if 1:
	print( "Minimum Guaranteed Lobe: ", guar_lobe )


''''""""""""""""""""""""""""""""""""""""""""""""""""""""""
GENERATING THE LOBE
 
Once we have some basic values we can prepare the plot. 
This will be a cuadrant going from 0 to 90deg. 
 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""'''

rows_specific_phi	= len( alphas_d )
row_each_phi 		= rows_specific_phi
row_final 			= row_each_phi + 1

if 0: 
	f, axs = plt.subplots(1, 2, subplot_kw=dict(projection="polar"))
	setup_plot	( axs[0] )
	plot_lobe	( axs[0],  guar_lobe )
	setup_plot	( axs[1] )
	plot_lobe	( axs[1],  guar_lobe )
	plt.show()
	

if 1: 
	f, axs = plt.subplots(rows_specific_phi + 2, len(phis_d), subplot_kw=dict(projection="polar"))

	for phi_d, i_col in zip( phis_d, range( len( phis_d ) ) ):
		phi = str(phi_d)
				
		for alpha_d, i_row in zip( alphas_d, range( len( alphas_d ) ) ) :
			alpha = str(alpha_d)

			values = np.array( list ( r_max_rot_tag[ phi ][alpha].values() ))			
			
			setup_plot	( axs[ i_row ][ i_col ] )
			plot_lobe	( axs[ i_row ][ i_col ], values )	


#### Plot each time-flattened lobe	
	for phi_d, i_ax in zip( phis_d, range( len(phis_d) ) ):
		phi = str( phi_d ) 
			
		values = np.array( list ( r_max_flat_time[ phi ].values() ))

		setup_plot 	( axs[row_each_phi][i_ax] )
		plot_lobe	( axs[row_each_phi][i_ax], values )
	
### Plot the minimal lobe
	setup_plot	( axs[row_final][0] )
	plot_lobe	( axs[row_final][0],  guar_lobe )

	plt.show()

##############################################
############# TEXT FOR theta LOBE ##############
##############################################
if 0:
	f.text(0.68, 0.13, "%02d μV @ %d m →" % (B_max_dist, 	max_dist_m ), ha='center', fontsize=14)


##############################################
#############  SAVE IMG ##############
##############################################
if 0:
	f.savefig("imgs/"+meas+".svg",format = 'svg',transparent=True)






