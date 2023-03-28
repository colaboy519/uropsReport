import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import special
import numpy as np
import pandas as pd
import math
import csv

# open data file 
#-------------------------------------------------------------------
fileLocation = input('Key in csv file path\n')
data = pd.read_csv(fileLocation)
x = data.position[2:].to_numpy()
y = data.voltage[2:].to_numpy()

x = [float(i) for i in x] # make it a list of float 
y = [float(i) for i in y] # make it a list of float


# curve fitting
#-------------------------------------------------------------------
def power(hi,po,p,w,h0): 
    pi = po + p/2 * special.erfc((h0-hi)/(w/math.sqrt(2)))
    return pi
#make sure hi-h0>0

# guessed parameters p0 = [po,p,w,h0]
# po = background power reading, 
# p = maximum power reading, 
# w = guessed beam width, here it's set to 0.5mm
# h0 = position of half maximum power reading -> center of beam position
po = float(data.voltage[1])
p = float(max(y))
w = float(0.0005)
h0 = float(input('What is the position of half maximum in unit (m): guess base on data (remember to consider background power)\n'))
# print(po,p,w,h0)
# print(type(po),type(p),type(w),type(h0))
# here h0 is eyeballed, can write a code for it instead in the future

popt,pcov = curve_fit(power,x,y,p0 =[po,p,w,h0])
# last used p0 values: 0.288,21.5,0.0005,0.0092

print('finished fitting, plotting graph')

# plot graphs
#-------------------------------------------------------------------
plt.plot(x,y, 'o', label='data')

xdata = np.linspace(min(x),max(x),num=1000)
plt.plot(xdata, power(xdata, *popt), 'r-', label='Fitting')
plt.legend()
plt.title('Fitting')
plt.xlabel('knife position (m)')
plt.ylabel('voltage (V)')

print(popt,pcov)
print("beam width =",popt[2],"(m)") # beam fitted w value 
beamStdev = np.sqrt(np.diag(pcov))[2]
print("stdev =",'%.20f' % beamStdev,"(m)") # print one standard deviation in decimal format

print('all done')

#this line blocks the script from proceeding, hence it's moved to the end
plt.show()