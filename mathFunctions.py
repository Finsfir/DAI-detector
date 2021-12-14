#This custom package contains Math\Geometry Functions

import cv2 as cv
import numpy as np

def orientation(x1, x2, x3, y1, y2, y3): # Orientation of point x3,y3 relative to vector starts in x1,y1 and ends in x2,y2
    x3 -= x1
    y3 -= y1
    a = ((x2 - x1)**2 + (y2- y1)**2)**0.5
    b = x2 - x1
    c = y2 - y1
    if b == 0 or c == 0:
        return 0
    alpha = (b*b + c*c - a*a)/(2*b*c)    
    M = np.array([[alpha, -np.sin(np.arccos(alpha))], [np.sin(np.arccos(alpha)), alpha]]) # Transformation matrix Oxy -> vector's basis    
    #X3 = M[0,0] * x3 + M[0,1] * y3
    Y3 = M[1,0] * x3 + M[1,1] * y3    
    if Y3 > 0:
        return 1
    else:
        return 0
    
def cosTh(x3, x2, x1, y3, y2, y1): # Angle between vectors c = (x3 - x1, y3 - y1) and b = (x3 - x2, y3 - y2)
    a = ((x2 - x1)**2 + (y2- y1)**2)**0.5
    b = ((x3 - x1)**2 + (y3- y1)**2)**0.5
    c = ((x3 - x2)**2 + (y3- y2)**2)**0.5
    
    if b == 0 or c == 0:
        return 0
    alpha = (b*b + c*c - a*a)/(2*b*c)
    if orientation(x1, x3, x2, y1, y3, y2):
        alpha = 180 - np.arccos(alpha)*180/np.pi
    else:
        alpha = 180 + np.arccos(alpha)*180/np.pi
    return alpha


def scale(x, y, w, h, scaleKoef = 0.1):
    hh = round(scaleKoef * (h - y))
    ww = round(scaleKoef * (w - x))
    if y - hh > 0 and x - ww > 0:
        y -= hh
        x -= ww
        h += hh
        w += ww
    return x, y, w, h

def drawLine(image, x1, x2, y1, y2, koef = 2.5, line_thickness = 2, approx = 0):
    cv.line(image, (x2, y2), (x1, y1), (0, 255, 0), thickness=line_thickness)
    if approx:
        dX = x2 - x1
        dY = y2 - y1
        dX = round(x1 - dX * koef)
        dY = round(y1 - dY * koef)
        cv.line(image, (dX, dY), (x1, y1), (0, 0, 255), thickness=line_thickness)
    return image
    