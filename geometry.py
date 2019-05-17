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



def line(p1, p2):
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0]*p2[1] - p2[0]*p1[1])
    return A, B, -C
@jit
def intersection(L1, L2):
    D  = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        return x,y
    else:
        return False
@jit
def boolIntersect(segment, R):
    hit = True
    minX = min(segment[0][0], segment[0][1])
    maxX = max(segment[0][0], segment[0][1])
    minY = min(segment[1][0], segment[1][1])
    maxY = max(segment[1][0], segment[1][1])
    if R[0] > maxX or R[0] < minX:
        hit = False
    if R[1] > maxY or R[1] < minY:
        hit = False
    return hit

'''@jit
def intersectAndHit(segment1, segment2):
    p1 = [segment1[0][0],segment1[1][0]]
    p2 = [segment1[0][1],segment1[1][1]]
    L1 = line(p1, p2)
    p1 = [segment2[0][0],segment2[1][0]]
    p2 = [segment2[0][1],segment2[1][1]]
    L2 = line(p1, p2)
    R = intersection(L1, L2)
    #did it hit the detector
    hit = False
    if R:
        if boolIntersect(segment1, R) and boolIntersect(segment2, R):
            hit = True

    return R, hit, '''


@jit
def intersectAndHit(segment1, segment2):
    p1 = [segment1[0][0],segment1[1][0]]
    p2 = [segment1[0][1],segment1[1][1]]
    L1 = line(p1, p2)
    p1 = [segment2[0][0],segment2[1][0]]
    p2 = [segment2[0][1],segment2[1][1]]
    L2 = line(p1, p2)
    R = intersection(L1, L2)

    return R

@jit
def returnRotation(cordRotation, x,y):
    newX = math.cos(cordRotation)*x - math.sin(cordRotation)*y
    newY = math.sin(cordRotation)*x + math.cos(cordRotation)*y
    return newX, newY   
@jit
def returnLocalDxDy(cordRotation, segment):

    cordRotation = -(cordRotation - math.pi/2)
    x0, y0 = segment[0][0],segment[1][0]
    newX0, newY0 =  returnRotation(cordRotation, x0,y0)
    x1, y1 = segment[0][1],segment[1][1]
    newX1, newY1 =  returnRotation(cordRotation, x1,y1)
    if newX1 == newX0:
        return float('nan')
    newSlope = (newY1-newY0)/(newX1 -newX0)
    return newSlope

@jit
def transformCord(cordX, cordY, cordRotation, point):
    cordRotation = -(cordRotation - math.pi/2)
    x, y = point[0]-cordX, point[1]-cordY
    newX, newY =  returnRotation(cordRotation, x,y)
    return [newX, newY]

