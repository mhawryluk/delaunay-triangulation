from math import cos, sin, pi
from random import uniform, random


def generate_points_on_vertical(amount, x, y1, y2):
    points_list = []
    for i in range(amount):
        points_list.append((x, uniform(y1,y2)))
    return points_list

def generate_points_on_segment(amount, p1, p2):
    if p1[0] == p2[0]:
        return generate_points_on_vertical(amount, p1[0], min(p1[1], p2[1]), max(p1[1], p2[1]))
    points_list = []
    a = (p2[1] - p1[1])/(p2[0] - p1[0]);
    b = p1[1] - a*p1[0];
    for i in range(amount):
        x = uniform(min(p1[0],p2[0]),max(p1[0],p2[0]))
        points_list.append(( x, a*x + b))
    return points_list

def generate_points_on_axis_and_diagonals(amountAxis, amountDiagonal, x, y):
    points_list = [(0,0), (x,0), (0,y), (x,y)]
    points_list = points_list + generate_points_on_segment(amountAxis, (0,0), (0,y))
    points_list = points_list + generate_points_on_segment(amountAxis, (0,0), (x,0))
    points_list = points_list + generate_points_on_segment(amountDiagonal, (0,y), (x,0))
    points_list = points_list + generate_points_on_segment(amountDiagonal, (0,0), (x,y))
    return points_list

def generate_points_on_circle(amount):
    center = (0,0)
    radius = amount/6
    points_list = []
    for i in range(amount):
        t = random()
        pt = (radius * cos(2 * pi * t) + center[0], radius * sin(2 * pi * t) + center[1])
        points_list.append(pt)
    return points_list


def generate_random_points(amount, range_from, range_to):
    return [(uniform(range_from, range_to), uniform(range_from, range_to)) for _ in range(amount)]


def generate_multiple_rectangles(amount, max_value, tan_of_angle_to_OX):
    points = []
    for i in range(amount):
        x = uniform(0, max_value)
        points = points + [(x, tan_of_angle_to_OX*x), (x, -tan_of_angle_to_OX*x), (-x, -tan_of_angle_to_OX*x), (-x, tan_of_angle_to_OX*x)]
    return points
