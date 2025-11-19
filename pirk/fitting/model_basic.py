import numpy as np


def exp_decay(dirk_times, amplitude, tau, y_offset=0.0):
    """
    Exponential decay function with an offset for the y-values (set by default to zero).

    input:
        x: array, x values
        amplitude: float, amplitude of the decay
        tau: float, time constant of the decay
        offset: float, offset of the decay
    output:
        y: array, y values of the decay

        """
    return amplitude * (np.exp(-dirk_times / tau) - 0.0) + y_offset


def exp_decay_with_variable_gH(x, amplitude, gH_start, gH_end, gH_lifetime):  # , y_offset):
    """
    Exponential decay function for ECS (of pmf) where the decay rate constant, gH+ itself is dependent on a firt-order decay of gH+.

    input:
        x: array, x values
        amplitude: float, amplitude of the decay
        gH_start: float, initial gH+ value
        gH_end: float, final gH+ value
        gH_lifetime: float, lifetime of gH+

    output:
        y: array, y values of the decay
        gH: array, gH values of the decay

    """
    gH_amplitude = gH_start - gH_end
    gH = np.array(exp_decay(x, gH_amplitude, gH_lifetime) + gH_end)

    return np.array(amplitude * (np.exp(-x * gH) - 0.0)), gH  # _amplitude #+ y_offset


def pirk_amplitude_recovery(pirk_time, pirk_begin_amplitude, pirk_end_amplitude, recovery_lifetime):  #, y_offset):
    """
    Exponential decay function with an offset. The starting point is the offset and the end point is the offset + amplitude.
    input:
        x: array, x values
        amplitude: float, amplitude of the decay
        tau: float, time constant of the decay
        offset: float, offset of the decay
    output:
        y: array, y values of the decay

        """
    amplitude = pirk_begin_amplitude - pirk_end_amplitude

    return amplitude * (
        np.exp(-pirk_time / recovery_lifetime)) + pirk_end_amplitude  #relative_pirk_amplitude #_amplitude #+ y_offset
