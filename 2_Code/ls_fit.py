# 2_Code/ls_fit.py
"""
Frequentist least-squares fit for Omega_m (and optionally Omega_lambda) and mu0.
Returns best-fit parameters by minimizing chi^2 using scipy.optimize.least_squares.
"""

import numpy as np
from scipy.optimize import least_squares
from .cosmology import distance_modulus


def residuals_theta(theta, z, mu_obs, mu_err, fit_omega_lambda=False):
    if fit_omega_lambda:
        Omega_m, Omega_lambda, mu0 = theta
        mu_model = distance_modulus(z, Omega_m, Omega_lambda) + mu0
    else:
        Omega_m, mu0 = theta
        mu_model = distance_modulus(z, Omega_m) + mu0
    return (mu_obs - mu_model) / mu_err


def fit_least_squares(z, mu_obs, mu_err, fit_omega_lambda=False, initial=None):
    if fit_omega_lambda:
        if initial is None:
            initial = [0.3, 0.7, 0.0]
        bounds = ([0.0, -1.0, -10.0], [2.0, 2.0, 10.0])
        res = least_squares(residuals_theta, initial, args=(z, mu_obs, mu_err, True), bounds=bounds)
    else:
        if initial is None:
            initial = [0.3, 0.0]
        bounds = ([0.0, -10.0], [2.0, 10.0])
        res = least_squares(residuals_theta, initial, args=(z, mu_obs, mu_err, False), bounds=bounds)

    return res
