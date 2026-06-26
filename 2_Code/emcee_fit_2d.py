# 2_Code/emcee_fit_2d.py
"""
emcee wrapper for fitting (Omega_m, Omega_lambda, mu0) to SN distance modulus data.

This extends emcee_fit.py to allow a 2D cosmological parameter inference and produces
posteriors for Omega_m and Omega_lambda (plus mu0 nuisance parameter).
"""

import numpy as np
import emcee
from .cosmology import distance_modulus


def log_prior(theta):
    Omega_m, Omega_lambda, mu0 = theta
    # Priors: Omega_m in (0,2), Omega_lambda in (-1,2), broad mu0
    if 0.0 < Omega_m < 2.0 and -1.0 < Omega_lambda < 2.0 and -10.0 < mu0 < 10.0:
        return 0.0
    return -np.inf


def log_likelihood(theta, z, mu_obs, mu_err):
    Omega_m, Omega_lambda, mu0 = theta
    mu_model = distance_modulus(z, Omega_m, Omega_lambda) + mu0
    inv_sigma2 = 1.0 / (mu_err ** 2)
    return -0.5 * np.sum((mu_obs - mu_model) ** 2 * inv_sigma2)


def log_probability(theta, z, mu_obs, mu_err):
    lp = log_prior(theta)
    if not np.isfinite(lp):
        return -np.inf
    return lp + log_likelihood(theta, z, mu_obs, mu_err)


def run_emcee_2d(z, mu_obs, mu_err, nwalkers=48, nsteps=5000, burn=1000, seed=None):
    rng = np.random.default_rng(seed)
    ndim = 3
    p0 = np.empty((nwalkers, ndim))
    p0[:, 0] = 0.3 + 1e-3 * rng.standard_normal(nwalkers)  # Omega_m
    p0[:, 1] = 0.7 + 1e-3 * rng.standard_normal(nwalkers)  # Omega_lambda
    p0[:, 2] = 0.0 + 1e-2 * rng.standard_normal(nwalkers)  # mu0

    sampler = emcee.EnsembleSampler(nwalkers, ndim, log_probability, args=(z, mu_obs, mu_err))
    sampler.run_mcmc(p0, nsteps, progress=True)

    samples = sampler.get_chain(discard=burn, flat=True)
    return sampler, samples
