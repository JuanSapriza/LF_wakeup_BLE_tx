


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



with open('measured.csv') as data:
    values = np.empty((0,4),int)
    for line in data:
        newLine = line.strip().split(',')
        miArray = np.array(newLine)
        values = np.append(values,[miArray],axis=0)
        values = np.asfarray(values,dtype=float)

values = values.transpose()


## GETTING AXIS AND X,Y PAIRS

r = values[0]*0.01
t = values[1]*pi/180
v = values[2]
u = values[3]

## POLAR COORDINATES
m = np.sqrt(u**2 + v**2)
a = np.arctan(u/v)


#para los colores
mc = m*r**(2.7)
#mc = (1/m)**3

# CORRECTION!!!!
#for i in range(len(a)):
#   a[i] = t[i]+(t[i]-a[i]) if t[i] > a[i] else a[i]


## NORMALIZATION
for i in range(len(u)):
    u[i] = np.cos(a[i]) if t[i] <= a[i] else -np.cos(a[i]) 
v = np.sin(a)

f = plt.figure()

ax = f.add_subplot(polar=True)
ax.quiver(t, r, u , v, mc, scale = 12, width=0.008, clip_on = False, zorder=100 )


ax.set_rmax(max(r)+min(r))
ax.set_thetamax(90)

maxAngle = 90
ax.set_xticks(pi/180 * np.linspace(0,  maxAngle, 7, endpoint=True))
ax.set_rticks([ 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.40])

f.text(0.5, 0.01, "Distance (m)", ha='center', fontsize=14)
f.text(0.72, 0.62, "Reader-tag angle", ha='center',fontsize=14, rotation = -45)

plt.tight_layout(pad = 0.8)






xls = np.array([0, 15, 30, 45, 60, 75, 90])*pi/180
yls = np.array([0.40, 0.35, 0.37, 0.38, 0.38, 0.39, 0.36 ])
# Lineal sin 5cm
#0.39, 0.40, 0.38, 0.36, 0.34, 0.31, 0.31

# Lineal con 5cm (mas lindo)
# 0.40, 0.39, 0.36, 0.33, 0.31,	0.28, 0.29

# Log sin 5cm
#0.40, 0.35, 0.37, 0.38, 0.38, 0.39, 0.36

# Log con 5cm (original)
# 0.29, 0.30, 0.32, 0.36, 0.40, 0.39, 0.34

# Log sin 10cm
# 0.40, 0.32, 0.34, 0.38, 0.34, 0.39, 0.32

X_Y_Spline = make_interp_spline(xls, yls)
X_ = np.linspace(xls.min(), xls.max(), 500)
Y_ = X_Y_Spline(X_)

#scatter = ax.scatter(xls,yls, cmap="RdYlGn", s=75, edgecolor="black", clip_on=False, zorder=1000)
ax.plot(X_,Y_,'k--')
ax.fill_between(X_,0,Y_, alpha=0.075, zorder=0,color='k')
f.text(0.51, 0.13, "40 μV @ 5.0 m →", ha='center', fontsize=14)
f.text(0.45, 0.47, "40 μV @ 6.9 m →", ha='center', fontsize=14, rotation = 60)








plt.show()
f.savefig("imgs/measured.svg",format = 'svg',transparent=True)



