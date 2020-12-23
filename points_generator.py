from math import cos, sin, pi
from random import uniform, random


def generatePointsOnVertial(amount, x, y1, y2):
    pointsList = []
    for i in range(amount):
        pointsList.append((x, uniform(y1,y2)))
    return pointsList

def generatePoinsOnSegment(amount, p1, p2):
    if p1[0] == p2[0]:
        return generatePointsOnVertial(amount, p1[0], min(p1[1], p2[1]), max(p1[1], p2[1]))
    pointsList = []
    a = (p2[1] - p1[1])/(p2[0] - p1[0]);
    b = p1[1] - a*p1[0];
    for i in range(amount):
        x = uniform(min(p1[0],p2[0]),max(p1[0],p2[0]))
        pointsList.append(( x, a*x + b))
    return pointsList

def generatePointsOnAxisAndDiagonals(amountAxis, amountDiagonal, x, y):
    pointsList = [(0,0), (x,0), (0,y), (x,y)]
    pointsList = pointsList + generatePoinsOnSegment(amountAxis, (0,0), (0,y))
    pointsList = pointsList + generatePoinsOnSegment(amountAxis, (0,0), (x,0))
    pointsList = pointsList + generatePoinsOnSegment(amountDiagonal, (0,y), (x,0))
    pointsList = pointsList + generatePoinsOnSegment(amountDiagonal, (0,0), (x,y))
    return pointsList


def generatePointsOnCirdcle(amount, radius, center):
    pointsList = []
    for i in range(amount):
        t = random()
        pt = ( radius * cos(2 * pi * t) + center[0], radius * sin(2 * pi * t) + center[1])
        pointsList.append(pt)
    return pointsList
