from numba import jit
from geometry import *
from constants import *
from iterateMuon import iterateMuon
from circleIntersectLine import circleIntersectLine


#@jit
def propagateMuon(angleInitial, speed, charge, xInitial, yInitial):
    for i in range(100):

        if i == 0:
            radiusOfCurvature = returnRadiusOfCurvature(massOverCharge, speed, magneticField)
            x0 , y0 = circleFromPointAndRadius(xInitial, yInitial, radiusOfCurvature, angleInitial)
            yTrackOut = circleIntersectLine(100, 0, 100, 100, x0, y0, radiusOfCurvature, charge)

        xInitial, yInitial, angleInitial, speed, distance, x0, y0, radiusOfCurvature = iterateMuon(angleInitial, speed, charge, xInitial, yInitial)

        #if verbose > 9: print angleInitial, "\t", speed, "\t", charge, "\t", xInitial, "\t", yInitial, "\t",  x0, "\t", y0, "\t", radiusOfCurvature
        if verbose > 5: print "angle {} speed {} charge {} x {} y {} radius {}".format(angleInitial, speed, charge, xInitial, yInitial,  x0, y0, radiusOfCurvature)

        yHitOut = circleIntersectLine(100, 0, 100, 100, x0, y0, radiusOfCurvature, charge)

        if distance == -999:
            break

        if xBound[0] > xInitial or xBound[1] < xInitial:
            break

        if yBound[0] > yInitial or yBound[1] < yInitial:
            break
        
    if verbose > 5: 
        print "end loop yhitOut {}, yTrackOut {}".format(yHitOut, yTrackOut)



    residualLeavingBounds = yTrackOut -  yHitOut
    if verbose > 5: print "residual leaving bounds ", residualLeavingBounds

    return residualLeavingBounds