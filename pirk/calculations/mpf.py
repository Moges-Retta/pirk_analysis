from pirk.fitting.fitters import fit_fm_values
from pirk.parsing.loader import parse_array, extract_Fluro_paras


def calculate_params_noMPF(f_values):
    # --- Fs, Fo', and AFmP for reuse ---
    Fs = f_values["Fs"]
    FoPrime = f_values["FoPrime"]
    AFmP = f_values["AFmP"]

    # --- phi2 (w/ and w/o MPF) ---
    fvfm_noMPF = (AFmP - Fs) / AFmP

    # --- NPQt (w/ and w/o MPF) ---
    npqt_noMPF = 4.88 / ((AFmP / FoPrime) - 1) - 1

    # --- qL (w/ and w/o MPF) ---
    qL_noMPF = ((AFmP - Fs) * FoPrime) / ((AFmP - FoPrime) * Fs)

    # --- PhiNO (w/ and w/o MPF) ---
    PhiNO_noMPF = 1 / (npqt_noMPF + 1 + qL_noMPF * 4.88)

    # --- PhiNPQ (w/ and w/o MPF) ---
    PhiNPQ_noMPF = 1 - fvfm_noMPF - PhiNO_noMPF

    # --- qP (w/ and w/o MPF) ---
    qP_noMPF = (AFmP - Fs) / (AFmP - FoPrime)

    # --- Fv'/Fm' (w/ and w/o MPF) ---
    FvP_FmP_noMPF = (AFmP - FoPrime) / AFmP

    params = {
        'fvfm_noMPF': fvfm_noMPF,
        'npqt_noMPF': npqt_noMPF,
        'qL_noMPF': qL_noMPF,
        'PhiNO_noMPF': PhiNO_noMPF,
        'PhiNPQ_noMPF': PhiNPQ_noMPF,
        'qP_noMPF': qP_noMPF,
        'FvP_FmP_noMPF': FvP_FmP_noMPF
    }
    return params


def calculate_params_MPF(f_values, intercept):
    FmPrime_corr = intercept

    # --- Fs, Fo', and AFmP for reuse ---
    Fs = f_values["Fs"]
    FoPrime = f_values["FoPrime"]
    AFmP = f_values["AFmP"]

    # --- phi2 (w/ and w/o MPF) ---
    fvfm_MPF = (FmPrime_corr - Fs) / FmPrime_corr

    # --- NPQt (w/ and w/o MPF) ---
    npqt_MPF = 4.88 / ((FmPrime_corr / FoPrime) - 1) - 1

    # --- qL (w/ and w/o MPF) ---
    qL_MPF = ((FmPrime_corr - Fs) * FoPrime) / ((FmPrime_corr - FoPrime) * Fs)

    # --- PhiNO (w/ and w/o MPF) ---
    PhiNO_MPF = 1 / (npqt_MPF + 1 + qL_MPF * 4.88)

    # --- PhiNPQ (w/ and w/o MPF) ---
    PhiNPQ_MPF = 1 - fvfm_MPF - PhiNO_MPF

    # --- qP (w/ and w/o MPF) ---
    qP_MPF = (FmPrime_corr - Fs) / (FmPrime_corr - FoPrime)

    # --- Fv'/Fm' (w/ and w/o MPF) ---
    FvP_FmP_MPF = (FmPrime_corr - FoPrime) / FmPrime_corr

    params = {
        'Fs': Fs,
        'FoPrime': FoPrime,
        'FmPrime': FmPrime_corr,
        'fvfm_MPF': fvfm_MPF,
        'npqt_MPF': npqt_MPF,
        'qL_MPF': qL_MPF,
        'PhiNO_MPF': PhiNO_MPF,
        'PhiNPQ_MPF': PhiNPQ_MPF,
        'qP_MPF': qP_MPF,
        'FvP_FmP_MPF': FvP_FmP_MPF,
    }

    return params

def check_data(trace,fit_values,f_values,indices,ramp_lights):
    valid_outs = {}

    fit_values = fit_fm_values (trace,indices,ramp_lights)
    m = fit_values[0]
    b = fit_values[1]
    no_MPF = calculate_params_noMPF(f_values)
    valid_outs.update(no_MPF)
    MPF = calculate_params_MPF(f_values,b)

    # mpf failed
    if m>0:
        if no_MPF["fvfm_noMPF"] <= 0.10 or no_MPF["fvfm_noMPF"] >= 0.85:
            print("Phi2 is outside of the expected range, please consider discarding the measurement")

        if no_MPF["PhiNO_noMPF"] <= 0.10 or no_MPF["PhiNO_noMPF"]  >= 1.1:
            print("phiNO is outside of the expected range, please consider discarding the measurement")

        if no_MPF["PhiNPQ_noMPF"]  <= 0.10 or no_MPF["PhiNPQ_noMPF"] >= 1.1:
            print("phiNPQ is outside of the expected range, please consider discarding the measurement")
    else:
        valid_outs.update(MPF)
    valid_outs["MPF"] = MPF
    valid_outs["noMPF"] = no_MPF

    return valid_outs


def calculate_fvalues(combined_df, index, plot_all):
    pulses = parse_array(combined_df['number_pulses'][index])
    ramp_lights = parse_array(combined_df['RAMP_light'][index])
    trace = parse_array(combined_df['trace'][index])
    genotype = combined_df['genotype'][index]

    indices = calculate_indices(pulses, ramp_lights)

    fit_values = fit_fm_values(trace, indices, ramp_lights)
    f_values = extract_Fluro_paras(trace, indices)
    valid_values = check_data(trace, fit_values, f_values, indices, ramp_lights)

    if plot_all:
        replicate = combined_df['replicate'][index]
        genotype = combined_df['genotype'][index]
        light_intensity = combined_df['light_intensity'][index]

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

