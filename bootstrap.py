"""Bootstrapping correlations, to calculate confidence intervals & differences measures."""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import spearmanr

###################################################################################################
###################################################################################################

def bootstrap_corr(vec1, vec2, n_samples=5000, alpha=0.05, func=spearmanr, return_estimates=False):
    """Calculate a correlation, with bootstrapped confidence intervals.

    Parameters
    ----------
    vec1, vec2: 1d arrays
        Arrays or data to compute bootstrapped correlations between.
    n_samples : int, optional, default: 5000
        Number of bootstrap resamples to perform.
    alpha : float, optional, default: 0.05
        Alpha value, that defines the confidence interval value.
        At default value of 0.05, computes 95% confidence intervals.
    func : callable, optional, default: spearmanr
        Function to use to compute correlations.
    return_estimates : bool, optional, default: False
        Whether to return to distribution of bootstrapped estimates.
    """

    # Calculate measured correlation of the data
    r_val, p_val = func(vec1, vec2)

    # Resample bootstraps
    bootstrap_x, bootstrap_y = sample_bootstrap(n_samples, vec1, vec2)

    # Compute estimates across resamples
    estimates = compute_bootstrap_estimates(bootstrap_x, bootstrap_y, func)

    # Compute confidence intervals from bootstrapped distribution
    cis = compute_cis(estimates, alpha)

    if return_estimates:
        return r_val, p_val, cis, estimates
    else:
        return r_val, p_val, cis


def bootstrap_diff(vec_a, vec_b, vec_c, n_samples=5000, alpha=0.05,
                   func=spearmanr, return_estimates=False):
    """Calculate a bootstrapped difference measure of correlations AB vs. AC.

    Parameters
    ----------
    vec_a, vec_b, vec_c: 1d array
        Arrays of data to calculate the difference measure of.
        Data should be organized to compare whether corr(vec_a, vec_b) != corr(vec_a, vec_b).
    n_samples : int, optional, default: 5000
        Number of bootstrap resamples to perform.
    alpha : float, optional, default: 0.05
        Alpha value, that defines the confidence interval value.
        At default value of 0.05, computes 95% confidence intervals.
    func : callable, optional, default: spearmanr
        Function to use to compute correlations.
    return_estimates : bool, optional, default: False
        Whether to return to distribution of bootstrapped estimates.
    """

    # Calculate measured correlations of the data
    r_ab, p_ab = corr_func(vec_a, vec_b)
    r_ac, p_ac = corr_func(vec_a, vec_c)
    r_bc, p_bc = corr_func(vec_b, vec_c)

    # Calculate the difference in measures correlation between AB & AC
    r_diff = r_ab - r_ac

    # Resample bootstraps
    boot_a, boot_b, boot_c = sample_bootstrap(n_samples, vec_a, vec_b, vec_c)

    # Compute estimates across resamples
    corrs_ab = compute_bootstrap_estimates(boot_a, boot_b, corr_func)
    corrs_ac = compute_bootstrap_estimates(boot_a, boot_c, corr_func)

    # Calculate differences, across bootstrap resamples
    diffs = corrs_ab - corrs_ac

    # Compute confidence intervals from distribution of differences
    cis = compute_cis(diffs, alpha)

    # Calculate the p-value of the
    _, p_val = compute_pvalue(r_diff, cis)

    if return_estimates:
        return r_diff, p_val, cis, diffs
    else:
        return r_diff, p_val, cis


def sample_bootstrap(n_samples, *arrs):
    """Resample data for bootstrapping.

    Parameters
    ----------
    n_samples : int
        How many resamples to computes
    *arrs : 1d array
        Arrays to resample.

    Returns
    -------
    *2d arrays
        Resamples of input arrays, each with shape: [n_resamples, n_values].

    Notes
    -----
    This function samples and returns as many arrays as are passed in.
    """

    sample_size = len(arrs[0])
    new_idx = np.random.choice(np.arange(sample_size), replace=True,
                               size=(n_samples, sample_size))

    bootstrap_arrs = [arr[new_idx] for arr in arrs]

    return bootstrap_arrs


def compute_bootstrap_estimates(x, y, func):
    """Compute estimates across bootstrapped resamples between x & y.

    Parameters
    ----------
    x, y : 2d arrays
        Resampled data to compute estimates from, with shape: [n_resamples, n_values].
    func : callable
        Function to calculate esimate between data.

    Returns
    -------
    estimates : 1d array
        Computed estimates.
    """

    n_samples = x.shape[0]
    estimates = np.zeros(n_samples)
    for ind in range(n_samples):
        estimates[ind] = func(x[ind], y[ind])[0]

    return estimates


def compute_cis(estimates, alpha):
    """Compute confidence intervals from a distribution of bootstrapped estimates.

    Parameters
    ----------
    estimates : 1d array
        Distribution of estimates of a measure from across bootstrapped resamples.
    alpha : float
        Alpha value, that defines the confidence interval value.

    Returns
    -------
    lower, upper : float
        Computd confidence intervals.
    """

    lower = np.quantile(estimates, alpha / 2.)
    upper = np.quantile(estimates, 1 - alpha / 2.)

    return lower, upper


def compute_pvalue(diff, cis, z_val=1.96):
    """Compute the p-value of a difference measure, from bootstraped CI's.

    Parameters
    ----------
    diff : float
        Measured difference between measures, to test for significance.
    cis : list of [float, float]
        xx
    z_val : float, default: 1.96
        Z-value to use, corresponding to the confidence interval value.

    Notes
    -----
    - Default z-val of 1.96 assumes CI's at 95%.
    - Implementation from https://www.bmj.com/content/343/bmj.d2304

        If the upper and lower limits of a 95% CI are u and l respectively:
        1) calculate the standard error: SE = (u − l)/(2×1.96)
        2) calculate the test statistic: z = Est/SE
        3) calculate the P value2: P = exp(−0.717×z − 0.416×z2).
    """

    std_error = (cis[1] - cis[0]) / (2 * z_val)
    test_stat = diff / std_error

    p_val = np.exp(-0.717 * np.abs(test_stat) - 0.416 * test_stat**2)

    return test_stat, p_val


def plot_bootstrap(values, cis=None):
    """Plot a histogram of bootstraped estimates.

    Parameters
    ----------
    values : 1d array
        Distribution of bootstrap estimates.
    cis : list of [float, float], optional
        Confidence intervals to add to plot.
    """

    plt.hist(values)
    plt.axvline(values.mean(), color='k', linestyle='dashed', linewidth=4)

    if cis:
        plt.axvline(cis[0], color='r', linestyle='dashed', linewidth=2)
        plt.axvline(cis[1], color='r', linestyle='dashed', linewidth=2)
