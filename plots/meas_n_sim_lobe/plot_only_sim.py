import numpy as np
from numpy import pi
from matplotlib import pyplot as plt
from scipy.interpolate import make_interp_spline

figLength = 7
figHeight = figLength*0.85

plt.rcParams["figure.figsize"] = [figLength, figHeight]
plt.rcParams["figure.autolayout"] = True
plt.rcParams["font.family"] = "serif"
plt.rc('xtick',labelsize=13)
plt.rc('ytick',labelsize=13)



with open('replicaMeas.csv') as data:
    values = np.empty((0,3),int)
    for line in data:
        newLine = line.strip().split(',')
        miArray = np.array(newLine)
        values = np.append(values,[miArray],axis=0)
        values = np.asfarray(values,dtype=float)

values = values.transpose()


## GETTING AXIS AND X,Y PAIRS
r = values[0]*0.01
t = values[1]*pi/180
m = values[2]

#para los colores
mc = m*((r/0.01)**3)

f = plt.figure()
ax = f.add_subplot(polar=True)

for i in range(7):
	print("Thetha=" + str(t[i*8]))
	for j in range(8):
		k = i*8 + j
		print( "r=" + str(r[k]) + "\tm=" + str(m[k]) + "\tmc=" + str(mc[k]))


ax.scatter(t, r, c = mc)


ax.set_rmax(max(r)+min(r))
ax.set_thetamax(90)

maxAngle = 90
ax.set_xticks(pi/180 * np.linspace(0,  maxAngle, 7, endpoint=True))
ax.set_rticks([ 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.40])

f.text(0.5, 0.01, "Distance (m)", ha='center', fontsize=14)
f.text(0.72, 0.62, "Reader-tag angle", ha='center',fontsize=14, rotation = -45)

plt.tight_layout(pad = 0.8)



xls = np.array([0, 15, 30, 45, 60, 75, 90])*pi/180
yls = np.array([0.40, 0.39, 0.37, 0.34, 0.31, 0.29, 0.28 ])
X_Y_Spline = make_interp_spline(xls, yls)
X_ = np.linspace(xls.min(), xls.max(), 500)
Y_ = X_Y_Spline(X_)


#scatter = ax.scatter(xls,yls, cmap="RdYlGn", s=75, edgecolor="black", clip_on=False, zorder=1000)
ax.plot(X_,Y_,'k--')
ax.fill_between(X_,0,Y_, alpha=0.075, zorder=0,color='k')
f.text(0.51, 0.13, "40 μV @ 5.0 m →", ha='center', fontsize=14)
f.text(0.45, 0.47, "40 μV @ 6.9 m →", ha='center', fontsize=14, rotation = 60)



plt.show()
f.savefig("replicaMeas.svg",format = 'svg',transparent=True)

