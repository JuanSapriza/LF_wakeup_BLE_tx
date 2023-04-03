import numpy as np
from scipy.interpolate import make_interp_spline
from scipy.optimize import curve_fit

sim = 'simulated'
meas = 'measured'
data_dir = 'data'



##############################################
#### FUNCTIONS TO APPROXIMATE ################
##############################################
def decay(x, a):
	return a*(x**(-3))

def decay_inv(y, a):
	return (a/y)**(1/3)


##############################################
#### FUNCTIONS TO GET THE LOBE ###############
##############################################

def get_lobe(distances_m, module):
	A=np.zeros(dists_n)

	skip = 1
	for i in range(dists_n):
		start = i*8 + skip
		end = start + 7 - skip
		opot, pcov = curve_fit( decay, distances_m[start:end],module[start:end])
		perr = np.sqrt(np.diag(pcov))
		A[i] = opot[0]
	# The Vth that would have been measured at the maximum 
	# reported Wake-Up-distance.
	# It was measured with 0 degrees.	
	th_max_dist = decay( max_dist_m, A[0] )
	# The distance at which in each direction that voltage is obtained	
	th_dist_m = np.zeros(dists_n)
	for i in range(dists_n):
		th_dist_m[i] = decay_inv( th_max_dist, A[i] )
	# Normalize those values for representation
	norm_th_dist_m = th_dist_m * max(r_m) / max_dist_m
	return (norm_th_dist_m, th_max_dist)

def get_lobe_polar( distances_m, angles_r, maxs ):

	xls = angles_r
	yls = np.array( maxs )
	
	X_ = np.linspace(xls.min(), xls.max(), 500)
	X_Y_Spline = make_interp_spline(xls, yls)
	Y_ = X_Y_Spline(X_)
	return (X_, Y_)
	
	

def getValuesFromFile( file_name ):
	with open( data_dir + file_name + 'deg.txt' ) as f_data:
		values = np.empty((0,4),int)
		for line in f_data:
		    newLine = line.strip().split('\t')
		    miArray = np.array(newLine)
		    values 	= np.append(values,[miArray],axis=0)
		    values 	= np.asfarray(values,dtype=float)
	return values.transpose()
