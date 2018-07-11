import math
import random
from numba import jit
from constants import pi, typicalScatteringDistance, angleConstant, speedDecreaseConstant, massOverCharge, magneticField
from geometry import *

@jit
def iterateMuon(angleInitial, speed, charge, xInitial, yInitial):
    #radiusOfCurvature = massOverCharge*speed/magneticField #negative means curve the other way
    radiusOfCurvature = returnRadiusOfCurvature(massOverCharge, speed, magneticField)

    #flip y by charge, then flip back
    yInitial = yInitial*charge

    x0, y0 = circleFromPointAndRadius(xInitial, yInitial, radiusOfCurvature, angleInitial)

    #calculate scattering distance:
    distance = scatteringDistance()

    circumference = 2*pi*abs(radiusOfCurvature)

    if distance > circumference:
        distance = -999
        xFinal, yFinal, angleFinal = xInitial, yInitial, angleInitial
        angleAfterScatter = angleInitial
    else:
        angleCovered = distance/circumference*2*pi #angles are radians
        angleFinal = angleInitial + angleCovered

        xFinal, yFinal = circleFromPointAndRadius(x0,y0, -radiusOfCurvature, angleFinal)

        scatAngle = scatteringAngle(speed)
        angleAfterScatter =  angleFinal + scatAngle

        speed = scatteringSpeed(speed,scatAngle)

    if xFinal < xInitial:
        distance = -999

    #flip y by charge, then flip back
    yFinal = yFinal*charge

    return xFinal, yFinal, angleAfterScatter, speed, distance, x0, y0, radiusOfCurvature