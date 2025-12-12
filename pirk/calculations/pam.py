import pandas as pd

from pirk.fitting.fitters import fit_fm_values
from pirk.parsing.loader import parse_array, extract_Fluro_paras
from pirk.names import *


import numpy as np

from pirk.plotting.fits import plot_PAM

def calculate_indices(pulses, ramp_lights):
    indices = {'fs_begin': 0, 'fs_end': pulses[0] - 1}
    start = indices['fs_end'] + 1

    for i in range(1, len(ramp_lights)  + 1):
        indices[f'Fm_{i}_begin'] = start
        indices[f'Fm_{i}_end'] = start + pulses[i] - 1
        start = indices[f'Fm_{i}_end'] + 1

    # FoPrime
    FoPrime_begin = indices[f'Fm_{len(ramp_lights) }_end'] + pulses[len(ramp_lights)  + 1]
    FoPrime_end = FoPrime_begin + pulses[len(ramp_lights)  + 1]
    indices.update({'FoPrime_begin': FoPrime_begin, 'FoPrime_end': FoPrime_end})

    return indices

def calculate_fluorescence_params ( f_values: dict , FmPrime_corr: float = None ) -> dict :
    """
    Calculate fluorescence parameters with and without MPF correction.

    Parameters
    ----------
    f_values : dict
        Dictionary containing:
        - Fs: Steady-state fluorescence
        - FoPrime: Minimal fluorescence in light-adapted state
        - AFmP: Maximal fluorescence in light-adapted state
    FmPrime_corr : float, optional
        Corrected Fm' for MPF. If provided, MPF-corrected parameters are also calculated.

    Returns
    -------
    params : dict
        Dictionary containing:
        - fvfm_noMPF, npqt_noMPF, qL_noMPF, PhiNO_noMPF, PhiNPQ_noMPF, qP_noMPF, FvP_FmP_noMPF
        - fvfm_MPF, npqt_MPF, qL_MPF, PhiNO_MPF, PhiNPQ_MPF, qP_MPF, FvP_FmP_MPF (if FmPrime_corr is provided)
        - Fs, FoPrime, AFmP, FmPrime (if MPF is used)
    """
    Fs = f_values [ "Fs" ]
    FoPrime = f_values [ "FoPrime" ]
    AFmP = f_values [ "AFmP" ]

    # --- No MPF parameters ---
    fvfm_noMPF = (AFmP - Fs) / AFmP
    npqt_noMPF = 4.88 / ((AFmP / FoPrime) - 1) - 1
    qL_noMPF = ((AFmP - Fs) * FoPrime) / ((AFmP - FoPrime) * Fs)
    PhiNO_noMPF = 1 / (npqt_noMPF + 1 + qL_noMPF * 4.88)
    PhiNPQ_noMPF = 1 - fvfm_noMPF - PhiNO_noMPF
    qP_noMPF = (AFmP - Fs) / (AFmP - FoPrime)
    FvP_FmP_noMPF = (AFmP - FoPrime) / AFmP

    params = {
        'fvfm_noMPF' : fvfm_noMPF ,
        'npqt_noMPF' : npqt_noMPF ,
        'qL_noMPF' : qL_noMPF ,
        'PhiNO_noMPF' : PhiNO_noMPF ,
        'PhiNPQ_noMPF' : PhiNPQ_noMPF ,
        'qP_noMPF' : qP_noMPF ,
        'FvP_FmP_noMPF' : FvP_FmP_noMPF
    }

    # --- MPF-corrected parameters if FmPrime_corr is provided ---
    if FmPrime_corr is not None :
        fvfm_MPF = (FmPrime_corr - Fs) / FmPrime_corr
        npqt_MPF = 4.88 / ((FmPrime_corr / FoPrime) - 1) - 1
        qL_MPF = ((FmPrime_corr - Fs) * FoPrime) / ((FmPrime_corr - FoPrime) * Fs)
        PhiNO_MPF = 1 / (npqt_MPF + 1 + qL_MPF * 4.88)
        PhiNPQ_MPF = 1 - fvfm_MPF - PhiNO_MPF
        qP_MPF = (FmPrime_corr - Fs) / (FmPrime_corr - FoPrime)
        FvP_FmP_MPF = (FmPrime_corr - FoPrime) / FmPrime_corr

        params= {
            'Fs' : Fs ,
            'FoPrime' : FoPrime ,
            'FmPrime' : FmPrime_corr ,
            'fvfm_MPF' : fvfm_MPF ,
            'npqt_MPF' : npqt_MPF ,
            'qL_MPF' : qL_MPF ,
            'PhiNO_MPF' : PhiNO_MPF ,
            'PhiNPQ_MPF' : PhiNPQ_MPF ,
            'qP_MPF' : qP_MPF ,
            'FvP_FmP_MPF' : FvP_FmP_MPF
        }
    return params

def check_fluorescence_data_quality(trace, f_values, indices, ramp_lights) -> dict:
    """
    Check the quality of fluorescence data and calculate key parameters with and without MPF.

    Parameters
    ----------
    trace : array-like
        Raw fluorescence trace.
    f_values : dict
        Dictionary containing 'Fs', 'FoPrime', and 'AFmP'.
    indices : list or array
        Indices of relevant points in the trace for fitting.
    ramp_lights : array-like
        Light ramp values used to fit MPF.

    Returns
    -------
    valid_outs : dict
        Dictionary containing calculated parameters for no-MPF and MPF-corrected cases.
    """

    valid_outs = {}

    # Fit fluorescence to determine MPF slope (m) and intercept (b)
    m, b = fit_fm_values(trace, indices, ramp_lights)

    # Always compute both parameter sets
    noMPF = calculate_fluorescence_params(f_values)
    valid_outs.update(noMPF)

    MPF   = calculate_fluorescence_params(f_values, FmPrime_corr=b)

    # -------------------------------
    # Quality checks only apply when fit succeeded (m > 0)
    # -------------------------------
    if m > 0:
        if not (0.10 < noMPF["fvfm_noMPF"] < 0.85):
            print("⚠️ fv/fm (Phi2) is outside expected range; consider discarding measurement.")
        if not (0.10 < noMPF["PhiNO_noMPF"] < 1.1):
            print("⚠️ PhiNO is outside expected range; consider discarding measurement.")
        if not (0.10 < noMPF["PhiNPQ_noMPF"] < 1.1):
            print("⚠️ PhiNPQ is outside expected range; consider discarding measurement.")
    else:
        valid_outs.update(MPF)

    valid_outs["noMPF"] = noMPF
    valid_outs["MPF"]   = MPF
    valid_outs["m"]     = m
    valid_outs["b"]     = b

    return valid_outs

def calculate_fluorescence_values(combined_df, index, plot_all):
    pulses = parse_array(combined_df[NUMBER_PULSES][index])
    ramp_lights = parse_array(combined_df[RAMP_LIGHT][index])
    trace = parse_array(combined_df[TRACE_COLUMN][index])
    genotype = combined_df[GENOTYPE_COLUMN][index]

    indices = calculate_indices(pulses, ramp_lights)

    fit_values = fit_fm_values(trace, indices, ramp_lights)
    f_values = extract_Fluro_paras(trace, indices,ramp_lights)
    valid_values = check_fluorescence_data_quality(trace, f_values, indices,ramp_lights)

    if plot_all:
        replicate = combined_df[REPLICATE_COLUMN][index]
        genotype = combined_df[GENOTYPE_COLUMN][index]
        light_intensity = combined_df[TREATMENT_COLUMN][index]

        plot_PAM(trace, light_intensity, genotype, replicate)

    df = pd.DataFrame.from_dict(valid_values["MPF"], orient='index', columns=[f'{genotype}'])

    df.index = [
        "Fs", "Fo_p", "Fm_p", "ΦII", "NPQt",
        "qL", "ΦNO", "ΦNPQ", "qP", "Fv_Fm_p"
    ]

    print(np.round(df, 3))

    add_new_cols = True
    if add_new_cols:
        combined_df.at[index, 'Fs'] = df.loc['Fs'].values[0]
        combined_df.at[index, 'Fo_p'] = df.loc['Fo_p'].values[0]
        combined_df.at[index, 'Fm_p'] = df.loc['Fm_p'].values[0]
        combined_df.at[index, 'phi_2'] = df.loc['ΦII'].values[0]
        combined_df.at[index, 'NPQ_t'] = df.loc['NPQt'].values[0]
        combined_df.at[index, 'qL'] = df.loc['qL'].values[0]
        combined_df.at[index, 'phi_NO'] = df.loc['ΦNO'].values[0]
        combined_df.at[index, 'phi_NPQ'] = df.loc['ΦNPQ'].values[0]
        combined_df.at[index, 'qP'] = df.loc['qP'].values[0]
        combined_df.at[index, 'Fv_Fm_p'] = df.loc["Fv_Fm_p"].values[0]

