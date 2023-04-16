import numpy as np
from matplotlib import pyplot as plt

import code

''''""""""""""""""""""""""""""""""""""""""""""""""""""""""
 SOME IMPORTANT DEFINITIONS 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""'''

lines_n     = 2500 # Number of lines to take from the data

local = locals()

''''""""""""""""""""""""""""""""""""""""""""""""""""""""""
 GLOBAL VARIABLES 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""'''

time_ms     = []    # The time axis, in ms
dt_ms       = 0     # The time increment, in ms
i_mA        = []    # The current axis, in mA

 # Array containing each interval of interest
intvs       = []


class Interval:
    def __init__(self, name, ti, tf, factor, yscale, label):
        self.name = name  
        self.ti = ti
        self.tf = tf
        self.factor = factor
        self.yscale = yscale
        self.label = label

''''""""""""""""""""""""""""""""""""""""""""""""""""""""""
 USEFUL LOCAL FUNCTIONS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""'''

def getValuesFromFile( file_name ):
    with open( file_name ) as f_data:
        values = np.empty((0,4),int)
        for line, i in zip(f_data, range(lines_n) ):
            if i >= lines_n: break
            newLine = line.strip().split(',')
            miArray = np.array(newLine)
            values 	= np.append(values,[miArray],axis=0)
            values 	= np.asfarray(values,dtype=float)
    return values.transpose()

def time2Index( t ):
    return (np.floor(t)/dt_ms).astype(int)

def debug():
    code.interact(local=local)
    # Resume    Ctrl+D
    # Exit      Ctrl+Z



''''""""""""""""""""""""""""""""""""""""""""""""""""""""""
 Getting the values
"""""""""""""""""""""""""""""""""""""""""""""""""""""""'''

values 		= getValuesFromFile( "ConsumptionCSV.csv" )
time_ms 	= values[2][:lines_n] 
dt_ms       = time_ms[1] - time_ms[0]
i_mA        = values[3][:lines_n]
i_mA        = abs(i_mA)


''''""""""""""""""""""""""""""""""""""""""""""""""""""""""
 Interval information
"""""""""""""""""""""""""""""""""""""""""""""""""""""""'''
intvs.append( Interval(\
                        name    = "Whole Sequence",\
                        ti      = time2Index(2),\
                        tf      = time2Index(624),\
                        factor  = 1,\
                        yscale  = 'log',\
                        label   = "Current (mA)") )

intvs.append( Interval(\
                        name    = "Initialization",\
                        ti      = time2Index(94),\
                        tf      = time2Index(103),\
                        factor  = 1,\
                        yscale  = 'lin',\
                        label   = "Current (mA)") )

intvs.append( Interval(\
                        name    = "First Advertisement",\
                        ti      = time2Index(400),\
                        tf      = time2Index(435),\
                        factor  = 1,\
                        yscale  = 'lin',\
                        label   = "Current (mA)") )

intvs.append( Interval(\
                        name    = "i-th Advertisement",\
                        ti      = time2Index(510),\
                        tf      = time2Index(520),\
                        factor  = 1,\
                        yscale  = 'lin',\
                        label   = "Current (mA)") )

intvs.append( Interval(\
                        name    = "System off",\
                        ti      = time2Index(550),\
                        tf      = time2Index(560),\
                        factor  = 1000,\
                        yscale  = 'lin',\
                        label   = "Current (µA)") )

''''""""""""""""""""""""""""""""""""""""""""""""""""""""""
 SET UP OF PLOT WINDOW 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""'''

intvs_n = len(intvs)

individualSize = 3
figLength = individualSize*intvs_n
figHeight = individualSize
plt.rcParams["figure.figsize"] = [figLength, figHeight]

plt.rcParams["figure.autolayout"] = True
plt.rcParams["font.family"] = "serif"
plt.rc('xtick',labelsize=13)
plt.rc('ytick',labelsize=13)

#plt.tight_layout(pad = 0.8)



''''""""""""""""""""""""""""""""""""""""""""""""""""""""""
 SETTING UP THE PLOTS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""'''


f, axs = plt.subplots(1,intvs_n)


for intv, i in zip(intvs, range(intvs_n)):
    ax = axs[i]
    ax.plot(time_ms [ intv.ti : intv.tf ],\
            i_mA    [ intv.ti : intv.tf ]*intv.factor )

    ax.set_title(intv.name)
    ax.set_xlabel("Time (ms)")
    ax.set_ylabel(intv.label)
    if intv.yscale == 'log':
        ax.set_yscale("log")


plt.show()
