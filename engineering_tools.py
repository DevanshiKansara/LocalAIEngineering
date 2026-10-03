import math 

def spindle_speed(cutting_speed, diameter):
    return(1000 * cutting_speed) / (math.pi * diameter)