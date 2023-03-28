import numpy as np
from numpy import pi
from matplotlib import pyplot as plt
from scipy.interpolate import make_interp_spline
from scipy.optimize import curve_fit

max_dist_m 	= 5
dists_n 	= 7
angles_n 	= 7

plt.close('all')

figLength = 7
figHeight = figLength*0.85

plt.rcParams["figure.figsize"] = [figLength, figHeight]
plt.rcParams["figure.autolayout"] = True
plt.rcParams["font.family"] = "serif"
plt.rc('xtick',labelsize=13)
plt.rc('ytick',labelsize=13)

sim = 'simulated'
meas = 'measured'


##############################################
#### FUNCTIONS TO APPROXIMATE ################
##############################################
def decay(x, a):
	return a*(x**(-3))

def decay_inv(v, a):
	return (a/v)**(1/3)


def get_lobe(distances_m, module_T):
	A=np.zeros(dists_n)

	skip = 1
	for i in range(dists_n):
		start = i*8 + skip
		end = start + 7 - skip
		opot, pcov = curve_fit( decay, distances_m[start:end],module_T[start:end])
		perr = np.sqrt(np.diag(pcov))
		print(perr)
		A[i] = opot[0]
	# The Vth that would have been measured at the maximum 
	# reported Wake-Up-distance.
	# It was measured with 0 degrees.	
	Vth_max_dist_vpp = decay( max_dist_m, A[0] )
	# The distance at which in each direction that voltage is obtained	
	Vth_dist_m = np.zeros(dists_n)
	for i in range(dists_n):
		Vth_dist_m[i] = decay_inv( Vth_max_dist_vpp, A[i] )
	# Normalize those values for representation
	norm_Vth_dist_m = Vth_dist_m * max(r_m) / max_dist_m
	return (norm_Vth_dist_m, Vth_max_dist_vpp)

def get_lobe_polar( distances_m, modules_T,  ):

	xls = np.array([0, 15, 30, 45, 60, 75, 90])*pi/180
	X_ = np.linspace(xls.min(), xls.max(), 500)
	
	(norm_Vth_dist_m, Vth_max_dist_vpp) = get_lobe( distances_m, modules_T )
	yls = np.array(norm_Vth_dist_m)
	
	X_Y_Spline = make_interp_spline(xls, yls)
	Y_ = X_Y_Spline(X_)
	return (X_, Y_, Vth_max_dist_vpp)


##############################################
#### GETTING MEASURED VALUES ################
##############################################

with open(meas + '.csv') as data:
    values = np.empty((0,4),int)
    for line in data:
        newLine = line.strip().split(',')
        miArray = np.array(newLine)
        values = np.append(values,[miArray],axis=0)
        values = np.asfarray(values,dtype=float)

values = values.transpose()

## GETTING AXIS AND X,Y PAIRS
r_m = values[0]*0.01
t = values[1]*pi/180
v = values[2]
u = values[3]
## POLAR COORDINATES
m = np.sqrt(u**2 + v**2)
a = np.arctan(u/v)
## NORMALIZATION
for i in range(len(u)):
    u[i] = np.cos(a[i]) if t[i] <= a[i] else -np.cos(a[i]) 
v = np.sin(a)


##############################################
######### GETTING SIMULATED VALUES ###########
##############################################

with open( sim + '.csv') as data:
    values = np.empty((0,3),int)
    for line in data:
        newLine = line.strip().split(',')
        miArray = np.array(newLine)
        values = np.append(values,[miArray],axis=0)
        values = np.asfarray(values,dtype=float)

values = values.transpose()
## GETTING AXIS AND X,Y PAIRS
r_sim = values[0]*0.01
t_sim = values[1]*pi/180
m_sim = values[2]


##############################################
############# PLOTTING QUIVER  ###############
##############################################

color_scheme = np.log(m)

f = plt.figure()

ax = f.add_subplot(polar=True)

ax.quiver(t, r_m, u , v, color_scheme, scale = 12, width=0.008, clip_on = False, zorder=100 )
ax.set_rmax(max(r_m)+min(r_m))
ax.set_thetamax(90)
maxAngle = 90
ax.set_xticks(pi/180 * np.linspace(0,  maxAngle, 7, endpoint=True))
ax.set_rticks([ 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.40])
# Adding some text labels
f.text(0.5, 0.01, "Distance (m)", ha='center', fontsize=14)
f.text(0.72, 0.62, "Reader-tag angle", ha='center',fontsize=14, rotation = -45)
plt.tight_layout(pad = 0.8)


##############################################
########### GENERATING THE LOBE ##############
##############################################


(x_lobe, y_lobe_meas, Vth_max_dist_vpp) = get_lobe_polar( r_m, m )
( _, y_lobe_sim, _ ) 					= get_lobe_polar( r_m, m_sim )


# Adding the measured plot
ax.plot(x_lobe,y_lobe_meas,'k:')
# Adding the simulated plot and its shadow
ax.plot(x_lobe, y_lobe_sim, 'k--')
ax.fill_between(x_lobe,0,y_lobe_sim, alpha=0.075, zorder=0,color='k')

##############################################
############# TEXT FOR THE LOBE ##############
##############################################

f.text(0.68, 0.13, "%02d μV @ %d m →" % (Vth_max_dist_vpp*1e6, max_dist_m ), ha='center', fontsize=14)


##############################################
############# PLOT AND SAVE IMG ##############
##############################################

plt.show()
f.savefig("imgs/"+meas+".svg",format = 'svg',transparent=True)



