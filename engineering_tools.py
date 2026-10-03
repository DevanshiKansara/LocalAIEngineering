import math 

def spindle_speed(cutting_speed, diameter):
    return(1000 * cutting_speed) / (math.pi * diameter)

def feed_rate(spindle_speed, teeth, feed_per_tooth):
    return spindle_speed * teeth * feed_per_tooth