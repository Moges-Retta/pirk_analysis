# Extrace info from data frame that contains str object or numpy array
import ast
import numpy as np

def parse_array(value):
    """
    Safely parse a value (possibly a stringified list) into a NumPy array.
    """
    try:
        if isinstance(value, str):
            parsed = ast.literal_eval(value)
        else:
            parsed = value
        return np.array([x for x in parsed if x is not None])
    except (ValueError, SyntaxError, TypeError) as e:
        print(f"Error parsing array: {e}, value: {value}")
        return np.array([])  # Return empty array on failure

def parse_indices(value):
    """
    Safely parse index tuple/list (b, e) from a string or list-like.
    """
    try:
        if isinstance(value, str):
            b, e = ast.literal_eval(value)
        else:
            b, e = value
        return int(b), int(e)
    except (ValueError, SyntaxError, TypeError, IndexError) as e:
        print(f"Error parsing indices: {e}, value: {value}")
        return 0, 0  # Fallback to 0,0 on failure


def extract_Fluro_paras(trace, indices):
    # get trace and sort it from low to high
    Fs_trace = np.sort(trace[indices["fs_begin"]:indices["fs_end"]])[::-1]
    AFmP_trace = np.sort(trace[indices["Fm_1_begin"]:indices["Fm_1_end"]])[::-1]

    # Fs_trace = trace[indices["fs_begin"]:indices["fs_end"]]
    # Fs_trace.sort(reverse=True)

    # AFmP_trace = trace[indices["Fm_1_begin"]:indices["Fm_1_end"]]
    # AFmP_trace.sort(reverse=True)

    Fs = np.mean(Fs_trace[-4:-1])  # the last 4 values of F
    AFmP = np.mean(AFmP_trace[2:20])  # the 18 large values

    Fm_steps = {
        f"FmP_step{i}": np.mean(trace[indices[f"Fm_{i}_begin"]:indices[f"Fm_{i}_end"]][2:6])
        for i in range(2, 6)  # take the 4 largest values and average them
    }

    FoPrime = np.mean(trace[indices["FoPrime_begin"]:indices["FoPrime_end"]][2:6])

    results = {"Fs": Fs, "AFmP": AFmP, "FoPrime": FoPrime, **Fm_steps}

    return results


