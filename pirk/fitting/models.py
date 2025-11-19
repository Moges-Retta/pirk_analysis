import numpy as np

from pirk.fitting.model_basic import pirk_amplitude_recovery, exp_decay, exp_decay_with_variable_gH
from pirk.parsing.helpers import find_closest_index

def construct_dirk_pirk (x_total, pirk_points, dirk_amplitude,
                         gH_start, gH_end, gH_lifetime,
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
        gH_start: float, initial gH+ value
        gH_end: float, final gH+ value
        gH_lifetime: float, lifetime of gH+
        pirk_begin_amplitude: float, initial amplitude of the pirk signal
        pirk_end_amplitude: float, final amplitude of the pirk signal
        pirk_amplitude_recovery_lifetime: float, lifetime of the pirk signal
        offset_amplitude: float, amplitude of the slow component not associated with gh+ changes
        offset_lifetime: float, lifetime of the slow component not associated with gh+ changes

    output:
        y_total: array, the total decay of the protocol

        y_test, gH_test = exp_decay_with_variable_gH ( x_total, amplitude, gH_start, gH_end, gH_lifetime)


    """

    y_total = np.zeros(len(x_total))
    gH_values_total = np.zeros(len(x_total))
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
        # print(pirk_begin, pirk_end, pirk_begin_index, pirk_end_index)

        # x = np.linspace(pirk_begin, pirk_end, pirk_end_index - pirk_begin_index)
        # x = np.linspace(pirk_begin, pirk_end, pirk_end_index - pirk_begin_index)
        x = np.linspace(x_total[pirk_begin_index], x_total[pirk_end_index], pirk_end_index - pirk_begin_index)

        # print('i',i,"len(x) =", len(x),'pirk_points',pirk_points)

        # print(x[0], pirk_begin_amplitude, pirk_end_amplitude, pirk_amplitude_recovery_lifetime)
        relative_pirk_amplitude =  pirk_amplitude_recovery(x[0], pirk_begin_amplitude, pirk_end_amplitude, pirk_amplitude_recovery_lifetime)

        # plt.scatter(x[0], relative_pirk_amplitude)

        if i > 0:
            amplitude = y[-1] + relative_pirk_amplitude #pirk_amplitudes[i]
            gH_start_use = gH_values[-1]
            relative_pirk_amplitudes.append(relative_pirk_amplitude)
            pirk_times.append(x[0])
        else:
            gH_start_use = gH_start
            amplitude  = dirk_amplitude

        # PS_recovery(pirk_begin,   )


        y, gH_values = exp_decay_with_variable_gH ( x - pirk_begin, amplitude, gH_start_use, gH_end, gH_lifetime)
        # y_total = y_total + y

        y_total[pirk_begin_index:pirk_begin_index + len(y)] = y
        gH_values_total[pirk_begin_index:pirk_begin_index + len(y)] = gH_values
        dirk_pirk_x[pirk_begin_index:pirk_begin_index + len(y)] = x


    slow_phase = exp_decay(dirk_pirk_x, offset_amplitude, offset_lifetime)

    y_total = y_total + slow_phase
    y_total[-1] = y_total[-2]

    gH_values_total[-1] = gH_values_total[-2]
    dirk_pirk_x[-1] = dirk_pirk_x[-2]

    return dirk_pirk_x, y_total, gH_values_total, pirk_times, relative_pirk_amplitudes

def dirk_pirk (x_total, amplitude, gH_start, gH_end, gH_lifetime,
               pirk_begin_amplitude, pirk_end_amplitude,
               pirk_amplitude_recovery_lifetime, offset_amplitude, offset_lifetime,pirk_points):
       """
       Wrapper function for the construct_dirk_pirk function that returns the ECS signal for a given set of parameters.
       THis function is used to fit the parameters to the data using curve_fit.

       """

       _, dirk_pirk_y, _, _, _ = construct_dirk_pirk (x_total, pirk_points,
                                                               amplitude,
                                                                      gH_start, gH_end, gH_lifetime,
                                                                      pirk_begin_amplitude, pirk_end_amplitude,
                                                                      pirk_amplitude_recovery_lifetime,
                                                                      offset_amplitude, offset_lifetime)

       return dirk_pirk_y