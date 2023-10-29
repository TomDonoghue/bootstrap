# Bootstraps

Basic bootstrapping approaches for estimation statistics, in Python.

## Overview

This repo collects some code for doing bootstrapping, primarily for computing confidence intervals, and for correlation measures.

Main functionality:
- using bootstrapping to estimate confidence intervals correlation measures
- use bootstrapping to compare the differences of measures between groups
    - computing confidence intervals and estimated p-values of difference measures

## Organization

- `bootstrap/`: a collection of function for basic bootstrapping estimations
- `bootstrap-corr.ipynb`: a notebook which steps through available functionality

## Requirements

`bootstrap` is written in Python, and requires Python >= 3.6.

It has the following dependencies.

- [numpy](https://github.com/numpy/numpy)
- [scipy](https://github.com/scipy/scipy)
- [matplotlib](https://github.com/matplotlib/matplotlib)

## Installation

The `bootstrap` module can be installed with `pip`.

To clone and install this module, you can do:

```
$ git clone https://github.com/TomDonoghue/bootstrap
$ cd bootstrap
$ pip install .
```

## References

These explorations were part of exploring adding estimation statistics to my work.

For some context & information on estimation statistics, see:

- Editorial on estimation statistics in neuroscience:
    - https://www.eneuro.org/content/6/4/ENEURO.0259-19.2019
- Overview & introduction to estimation statistics:
    - https://www.eneuro.org/content/6/4/ENEURO.0205-19.2019

## License

This code is freely available for re-use / adaption / re-mixing etc - though with no guarantees of accuracy.
