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

    Returns
    -------
    r_val : float
        The calculated correlation coefficient.
    p_val : float
        The p-value of the correlation.
        Note: this is from the correlation function, not a p-value estimated from the bootstrap.
    cis : tuple of (float, float)
        Confidence interval, estimated from the bootstrap.
    estimates : 1d array
        The distribution of bootstrap estimates.
        Only returned if `return_estimates` is True.
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

    Returns
    -------
    r_diff : float
        The calculated difference of correlation values.
    p_val : float
        The p-value of the difference, calculated from the bootstrap distribution.
    cis : list of [float, float]
        Confidence interval, estimated from the bootstrap.
    diff : 1d array
        The distribution of bootstrap difference estimates.
        Only returned if `return_estimates` is True.
    """

    # Calculate measured correlations of the data
    r_ab, p_ab = func(vec_a, vec_b)
    r_ac, p_ac = func(vec_a, vec_c)
    r_bc, p_bc = func(vec_b, vec_c)

    # Calculate the difference in measures correlation between AB & AC
    r_diff = r_ab - r_ac

    # Resample bootstraps
    boot_a, boot_b, boot_c = sample_bootstrap(n_samples, vec_a, vec_b, vec_c)

    # Compute estimates across resamples
    corrs_ab = compute_bootstrap_estimates(boot_a, boot_b, func)
    corrs_ac = compute_bootstrap_estimates(boot_a, boot_c, func)

    # Calculate differences, across bootstrap resamples
    diffs = corrs_ab - corrs_ac

    # Compute confidence intervals from distribution of differences
    cis = compute_cis(diffs, alpha)

    # Calculate the p-value of the difference from the bootstrap distribution
    p_val = compute_pvalue(0, diffs)

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
        Function to calculate estimate between data.

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
        Computed confidence intervals.
    """

    lower = np.quantile(estimates, alpha / 2.)
    upper = np.quantile(estimates, 1 - alpha / 2.)

    return lower, upper


def compute_pvalue(value, estimates):
    """Compute the empirical p-value from a bootstrapped distribution.

    Parameters
    ----------
    value : float
        Value to test against the bootstrapped estimates.
    estimates : 1d array
        Distribution of estimates from the bootstrap sample.

    Returns
    -------
    p_val : float
        Estimated p-value, computed from the bootstrap distribution.

    Notes
    -----
    By default, this computes a two-sided comparison against null hypothesis of 0.
    """

    # Calculate empirical p: proportion of estimates below test value
    sorted_estimates = np.sort(estimates)
    p_value = sum(sorted_estimates < value) / len(sorted_estimates)

    # Make two sided
    p_value = 2 * np.min([p_value, 1 - p_value])

    return p_value


def plot_bootstrap(values, cis=None):
    """Plot a histogram of bootstrapped estimates.

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
