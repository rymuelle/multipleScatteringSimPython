import math
import random
from numba import jit
from constants import typicalScatteringDistance, angleConstant, speedDecreaseConstant, massOverCharge, magneticField

@jit
def scatteringDistance():
    scatteringDistance =  typicalScatteringDistance/(10*random.random() )
    return scatteringDistance

@jit
def scatteringAngle(speed):
    sigma = angleConstant/(speed)
    deltaAngle = sigma*2*(.5-random.random())
    return deltaAngle

@jit
def scatteringSpeed(speed,angle):
    speed = speedDecreaseConstant*speed*math.cos(angle)
    return speed

@jit
def circleFromPointAndRadius(xInitial, yInitial, radiusOfCurvature, angleInitial):
    x0 = xInitial - radiusOfCurvature*math.sin(angleInitial)
    y0 = yInitial + radiusOfCurvature*math.cos(angleInitial)
    return x0, y0

@jit
def returnRadiusOfCurvature(massOverCharge, speed, magneticField):
    radiusOfCurvature = massOverCharge*speed/magneticField
    return radiusOfCurvature