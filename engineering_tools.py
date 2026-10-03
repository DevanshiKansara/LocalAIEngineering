import math


def spindle_speed(cutting_speed, diameter):
    if cutting_speed <= 0:
        raise ValueError("Cutting speed must be greater than zero.")

    if diameter <= 0:
        raise ValueError("Tool diameter must be greater than zero.")

    return (1000 * cutting_speed) / (math.pi * diameter)


def feed_rate(spindle_speed, teeth, feed_per_tooth):
    if spindle_speed <= 0:
        raise ValueError("Spindle speed must be greater than zero.")

    if teeth <= 0:
        raise ValueError("Number of teeth must be greater than zero.")

    if feed_per_tooth <= 0:
        raise ValueError("Feed per tooth must be greater than zero.")

    return spindle_speed * teeth * feed_per_tooth