from numba import jit
from geometry import *
from constants import *
from iterateMuon import iterateMuon
from circleIntersectLine import circleIntersectLine


#@jit
def propagateMuon(angleInitial, speed, charge, xInitial, yInitial):
    #massOverCharge = 99999999999
    radiusOfCurvature = returnRadiusOfCurvature(massOverCharge, speed, magneticField)

    radiusOfCurvature = 1000
    xCircle0 , yCircle0 = circleFromPointAndRadius(xInitial, yInitial, radiusOfCurvature, angleInitial) # center of circle
    xLine0, yLine0, xLine1, yLine1 = 100, -2, 120, 100 
    xTrackOut, yTrackOut, angleTrack, trackLine, angleChamberOut = circleIntersectLine(xLine0, yLine0, xLine1, yLine1, xCircle0 , yCircle0, radiusOfCurvature, charge)

    #print xTrackOut, yTrackOut, angleTrack, trackLine
    angleIterate, xIterate, yIterate = angleInitial, xInitial, yInitial 
#
#    for i in range(100):
#
#
#
#
#        xIterate, yIterate, angleIterate, speed, distance, x0, y0, radiusOfCurvature = iterateMuon(angleIterate, speed, charge, xIterate, yIterate)
#
#        #if verbose > 9: print angleInitial, "\t", speed, "\t", charge, "\t", xInitial, "\t", yInitial, "\t",  x0, "\t", y0, "\t", radiusOfCurvature
#        if verbose > 5: print "angle {} speed {} charge {} x {} y {} radius {}".format(angleInitial, speed, charge, xInitial, yInitial,  x0, y0, radiusOfCurvature)
#
#        xHitOut, yHitOut, angle, hitLine = circleIntersectLine(100, 0, 100, 100, x0, y0, radiusOfCurvature, charge)
#
#        if distance == -999:
#            break
#
#        if xBound[0] > xInitial or xBound[1] < xInitial:
#            break
#
#        if yBound[0] > yInitial or yBound[1] < yInitial:
#            break
#        
#    if verbose > 5: 
#        print "end loop yHitOut {}, yTrackOut {} angle {}, hitline {}".format(yHitOut, yTrackOut, angle, hitLine )
#
#
#
#    residualLeavingBounds = yTrackOut -  yHitOut
#    if verbose > 5: print "residual leaving bounds ", residualLeavingBounds

    yHitOut = yTrackOut
    #print yTrackOut, yHitOut, angleTrack, angleInitial
    return yTrackOut, yHitOut, angleTrack