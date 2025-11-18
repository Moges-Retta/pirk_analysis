# Compute correlation matrix from covariance matrix
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
