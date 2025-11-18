import numpy as np


def exp_decay(dirk_times, amplitude, tau, y_offset):
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
