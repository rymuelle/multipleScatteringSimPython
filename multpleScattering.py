from numba import jit
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import math
import random


random.seed(1.0)

nEvents = 100000

xDistance = 100

yRange = [-100, 100]

typicalScatteringDistance = 10

angleConstant = 1.0

speedDecreaseConstant = .95

magneticField = 1.0

massOverCharge = 1.0

@jit
def shootParticle(angle, speed, charge):

    sigma = angleConstant/(speed*100)
    x = 0
    y = 0
    while(True): 
        currentX = x

        scatteringDistance =  typicalScatteringDistance/(10*random.random() )

        x = x + scatteringDistance*math.cos(angle)
        y = y + scatteringDistance*math.sin(angle)

        #print x, y

        if x > xDistance:
            scatteringDistance =  (xDistance - currentX)/math.cos(angle)
            x = 100
            y = y + scatteringDistance*math.sin(angle)

            #print y

            return y

        if y > yRange[1] or y < yRange[0]:
            return -999

        deltaAngle = sigma*2*(.5-random.random())
        angle = angle + deltaAngle
        speed = speed*speedDecreaseConstant
        sigma = angleConstant/(speed*100)

    return -999


y = []
for i in range(nEvents):
    hitLocation = shootParticle(0,1, 1)
    if hitLocation != -999: y.append(hitLocation)


n, bins, patches = plt.hist(y, 50, density=True, facecolor='g', alpha=0.75,range=[-10, 10])


plt.xlabel('y position')
plt.ylabel('Probability')
plt.title('Histogram of hit locations')
#plt.show()
plt.savefig("output/hit_position_hist.png")