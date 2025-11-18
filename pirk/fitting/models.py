import numpy as np

from pirk.fitting.model_basic import pirk_amplitude_recovery, exp_decay
from pirk.utils.helpers import find_closest_index

def construct_dirk_pirk(x_total, pirk_points, dirk_amplitude, lifetime, y_offset,
                        pirk_begin_amplitude, pirk_end_amplitude,
                        pirk_amplitude_recovery_lifetime,
                        offset_amplitude, offset_lifetime):
    """
    Construct a Dirk Pirk protocol with a set of pirk points and amplitudes.
    The protocol is constructed by generating exponential decays with variable tau values.
    The tau values are calculated using the calculate_gproton_values function.
    The protocol is constructed by generating the exponential decays for each pirk point and amplitude.
    The decay is generated using the exp_decay_with_variable_tau function.
    The decay is then added to the total decay.

    input:
        x_total: array, x values for the total decay time
        pirk_points: array, x values for the pirk points
        amplitude: float, amplitude of the decay
        tau: time constant of the decay
        y_offset : offset of the decay
        pirk_begin_amplitude: float, initial amplitude of the pirk signal
        pirk_end_amplitude: float, final amplitude of the pirk signal
        pirk_amplitude_recovery_lifetime: float, lifetime of the pirk signal
        offset_amplitude: float, amplitude of the slow component not associated with gh+ changes
        offset_lifetime: float, lifetime of the slow component not associated with gh+ changes

    output:
        y_total: array, the total decay of the protocol


    """

    y_total = np.zeros(len(x_total))
    dirk_pirk_x = np.zeros(len(x_total))
    relative_pirk_amplitudes = []
    pirk_times = []

    for i, pirk_begin in enumerate(pirk_points):
        if i == len(pirk_points) - 1:
            pirk_end = x_total[-1]
        else:
            pirk_end = pirk_points[i + 1]
        pirk_begin_index = find_closest_index(x_total, pirk_begin)
        pirk_end_index = find_closest_index(x_total, pirk_end)

        x = np.linspace(x_total[pirk_begin_index], x_total[pirk_end_index], pirk_end_index - pirk_begin_index)

        relative_pirk_amplitude = pirk_amplitude_recovery(x[0], pirk_begin_amplitude, pirk_end_amplitude,
                                                          pirk_amplitude_recovery_lifetime)

        if i > 0:
            amplitude = y[-1] + relative_pirk_amplitude  # pirk_amplitudes[i]
            relative_pirk_amplitudes.append(relative_pirk_amplitude)
            pirk_times.append(x[0])
        else:
            amplitude = dirk_amplitude

        y = exp_decay(x - pirk_begin, amplitude, lifetime, y_offset)

        y_total[pirk_begin_index:pirk_begin_index + len(y)] = y
        dirk_pirk_x[pirk_begin_index:pirk_begin_index + len(y)] = x

    slow_phase = exp_decay(dirk_pirk_x, offset_amplitude, offset_lifetime, y_offset=0)

    y_total = y_total + slow_phase


    return dirk_pirk_x, y_total, pirk_times, relative_pirk_amplitudes


def dirk_pirk(x_total, amplitude, tau, y_offset,
              pirk_begin_amplitude, pirk_end_amplitude,
              pirk_amplitude_recovery_lifetime, offset_amplitude, offset_lifetime):
    """
    Wrapper function for the construct_dirk_pirk function that returns the ECS signal for a given set of parameters.
    THis function is used to fit the parameters to the data using curve_fit.

    """
    global pirk_points


    _, dirk_pirk_y, _, _ = construct_dirk_pirk(x_total, pirk_points,
                                               amplitude,
                                               tau, y_offset,
                                               pirk_begin_amplitude, pirk_end_amplitude,
                                               pirk_amplitude_recovery_lifetime,
                                               offset_amplitude, offset_lifetime)

    return dirk_pirk_y