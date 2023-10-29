"""Tests for bootstrap."""

import numpy as np

from bootstrap.bootstrap import *

###################################################################################################
###################################################################################################

def test_bootstrap_corr():

    d1 = np.random.rand(10)
    d2 = np.random.rand(10)

    r_val, p_val, cis = bootstrap_corr(d1, d2)
    assert isinstance(r_val, float)
    assert isinstance(p_val, float)
    assert isinstance(cis, tuple)

def test_bootstrap_diff():

    d1 = np.random.rand(10)
    d2 = np.random.rand(10)
    d3 = np.random.rand(10)

    r_diff, p_val, cis = bootstrap_diff(d1, d2, d3)
    assert isinstance(r_diff, float)
    assert isinstance(p_val, float)
    assert isinstance(cis, tuple)

def test_sample_bootstrap():

    n_points = 50
    arr = np.random.rand(n_points)
    n_samples = 5

    resamples = sample_bootstrap(n_samples, arr)
    assert resamples[0].shape == (n_samples, n_points)

def test_compute_bootstrap_estimates():

    n_points = 10
    n_resamples = 5
    d1 = np.random.rand(5, 10)
    d2 = np.random.rand(5, 10)

    estimates = compute_bootstrap_estimates(d1, d2, spearmanr)
    assert isinstance(estimates, np.ndarray)

def test_compute_cis():

    vals = np.random.rand(50)
    alpha = 0.05

    lower_ci, upper_ci = compute_cis(vals, alpha)
    assert isinstance(lower_ci, float)
    assert isinstance(upper_ci, float)

def test_compute_pvalue():

    value = 0
    estimates = np.random.rand(50)

    p_val = compute_pvalue(value, estimates)
    assert isinstance(p_val, float)

def test_plot_bootstrap():

    values = np.random.rand(50)
    plot_bootstrap(values)
