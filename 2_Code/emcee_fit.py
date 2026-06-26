# 2_Code/emcee_fit.py
"""
emcee wrapper for fitting Omega_m (and a magnitude zero-point offset mu0)
to supernova distance modulus data.

Parameters fit: theta = [Omega_m, mu0]
- Omega_m: matter density parameter in [0,1]
- mu0: additive zero-point offset (absorbs absolute magnitude and H0 degeneracy)

AI assistance: scaffolding and docstrings were AI-assisted. Mathematical logic implemented by the author.
"""

import numpy as np
import emcee
from .cosmology import distance_modulus


def log_prior(theta):
    Omega_m, mu0 = theta
    # Uniform prior for Omega_m in (0,1), broad uniform prior for mu0
    if 0.0 < Omega_m < 1.0 and -10.0 < mu0 < 10.0:
        return 0.0
    return -np.inf


def log_likelihood(theta, z, mu_obs, mu_err):
    Omega_m, mu0 = theta
    mu_model = distance_modulus(z, Omega_m) + mu0
    inv_sigma2 = 1.0 / (mu_err ** 2)
    return -0.5 * np.sum((mu_obs - mu_model) ** 2 * inv_sigma2)


def log_probability(theta, z, mu_obs, mu_err):
    lp = log_prior(theta)
    if not np.isfinite(lp):
        return -np.inf
    return lp + log_likelihood(theta, z, mu_obs, mu_err)


def run_emcee(z, mu_obs, mu_err, nwalkers=32, nsteps=4000, burn=1000, seed=None):
    rng = np.random.default_rng(seed)
    ndim = 2
    # initialize walkers around reasonable guesses
    p0 = np.empty((nwalkers, ndim))
    p0[:, 0] = 0.3 + 1e-3 * rng.standard_normal(nwalkers)  # Omega_m
    p0[:, 1] = 0.0 + 1e-2 * rng.standard_normal(nwalkers)  # mu0

    sampler = emcee.EnsembleSampler(nwalkers, ndim, log_probability, args=(z, mu_obs, mu_err))
    sampler.run_mcmc(p0, nsteps, progress=True)

    samples = sampler.get_chain(discard=burn, flat=True)
    return sampler, samples
