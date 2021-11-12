from math import sqrt

def distance(a, b):
    """
    Determine the distance between a and b
    """
    return sqrt((a.location.x - b.location.x)**2 + (a.location.y - b.location.y)**2)
