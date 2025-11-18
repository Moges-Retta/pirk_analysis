import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def plot_corr_matrix(pcov, labels):
    lower_triangle = np.tril(pcov)

    param_std = np.sqrt(np.diag(pcov))  # Standard deviations
    outer_std = np.outer(param_std, param_std)

    # Avoid division by zero
    with np.errstate(divide='ignore', invalid='ignore'):
        corr_matrix = np.divide(pcov, outer_std)
        corr_matrix[~np.isfinite(corr_matrix)] = 0  # Replace nan/inf with 0

        # Create mask for upper triangle
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))

    # Plot only lower triangle
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, xticklabels=labels, yticklabels=labels,
                mask=mask, annot=True, fmt=".2f", cmap='coolwarm', vmin=-1, vmax=1)
    plt.title("Lower Triangle of Correlation Matrix")
    plt.tight_layout()
    plt.show()


def print_fit_table(combined_df,index,guess_dict,fit,pcov,trace_y,dirk_pirk_y):
    # Calculate standard errors
    perr = np.sqrt(np.diag(pcov))

    # Compute residuals (differences between actual and predicted)
    residuals = trace_y - dirk_pirk_y

    # Compute RMSE
    rmse = np.sqrt(np.mean(residuals ** 2))

    labels = guess_dict.keys()

    # Print table
    threshold = 0.5  # Threshold: relative error > 0.5 considered unreliable

    print(
        f"\nFitted Parameters and Standard Errors index. {index} : genotype {combined_df['genotype'][index]} Replicate :{combined_df['replicate'][index]}\n")
    print(f"RMSE: {rmse:.3f}")

    print(f"{'Parameter':35} {'Value':>10} {'Std. Error':>12} {'95% CI':>15}")
    print("-" * 85)

    for label, val, err in zip(labels, fit, perr):
        rel_err = abs(err / val) if val != 0 else float('inf')
        ci_low = val - 1.96 * err
        ci_high = val + 1.96 * err

        if rel_err > threshold or np.round(err, 3) == 0:
            color_start = '\033[91m'  # Red for high relative error
            color_end = '\033[0m'
        else:
            color_start = ''
            color_end = ''

        print(f"{color_start}{label:35} {val:10.3f} {err:12.3f} [{ci_low:7.3f}, {ci_high:7.3f}]{color_end}")

def plot_MPF_noMPF(fluro_values):

    width = 0.35
    i_incs = list(fluro_values.keys())
    index = range(len(i_incs))

    metrics = {
            "fvfm": r"$\phi_{II}$",
            "qL": "qL",
            "npqt": "NPQt",
            "PhiNPQ": r"$\phi_{NPQ}$",
            "PhiNO": r"$\phi_{NO}$"
        }

    for base_key, label in metrics.items():
        mpf_vals = [fluro_values[i][f"{base_key}_MPF"] for i in i_incs]
        no_mpf_vals = [fluro_values[i][f"{base_key}_noMPF"] for i in i_incs]

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(index, mpf_vals, width, label='MPF')
        ax.bar([i + width for i in index], no_mpf_vals, width, label='noMPF')
        ax.set_xticks([i + width / 2 for i in index])
        ax.set_xticklabels(i_incs)
        ax.set_xlabel("Light Intensity")
        ax.set_ylabel(label)
        ax.set_title(f"{label} Comparison (MPF vs. no MPF)")
        ax.legend()