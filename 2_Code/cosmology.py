"""
Cosmology utilities for SN Ia distance modulus modeling.

Assumptions:
- Flat Universe: Omega_k = 0, so Omega_Lambda = 1 - Omega_m.
- H0 is fixed by default (H0 = 70 km/s/Mpc), but can be passed to functions.

Physical formulas:
- E(z) = sqrt(Omega_m (1+z)^3 + Omega_Lambda)
- Comoving distance: chi(z) = c / H0 * integral_0^z dz' / E(z')
- Luminosity distance: d_L(z) = (1+z) * chi(z)
- Distance modulus: mu = 5 log10(d_L / 1 Mpc) + 25  (d_L in Mpc)

AI assistance: Some helper comments and non-critical scaffolding were generated with AI assistance; core physics formulas and implementation were verified by the author.
"""

import numpy as np
from scipy.integrate import quad

# Physical constants / defaults
c = 299792.458  # speed of light in km/s
DEFAULT_H0 = 70.0  # km/s/Mpc


def E(z, Omega_m, Omega_lambda=None):
    """Dimensionless Hubble parameter E(z) = H(z)/H0 for a flat or non-flat model.
    For flat models Omega_lambda can be omitted (Omega_lambda = 1 - Omega_m).
    """
    if Omega_lambda is None:
        Omega_lambda = 1.0 - Omega_m
    return np.sqrt(Omega_m * (1.0 + z) ** 3 + Omega_lambda)


def _invE_integrand(zp, Omega_m, Omega_lambda):
    return 1.0 / E(zp, Omega_m, Omega_lambda)


def comoving_distance(z, Omega_m, Omega_lambda=None, H0=DEFAULT_H0):
    """Compute comoving distance chi(z) in Mpc.

    Uses scipy.integrate.quad for accuracy; vectorized for array inputs.
    """
    if Omega_lambda is None:
        Omega_lambda = 1.0 - Omega_m

    def single(zi):
        val, _ = quad(_invE_integrand, 0.0, zi, args=(Omega_m, Omega_lambda))
        return (c / H0) * val

    z = np.atleast_1d(z)
    chi = np.array([single(zi) for zi in z])
    return chi if chi.size > 1 else chi[0]


def luminosity_distance(z, Omega_m, Omega_lambda=None, H0=DEFAULT_H0):
    """Luminosity distance d_L in Mpc."""
    chi = comoving_distance(z, Omega_m, Omega_lambda, H0)
    return (1.0 + z) * chi


def distance_modulus(z, Omega_m, Omega_lambda=None, H0=DEFAULT_H0):
    """Distance modulus mu(z) = 5 log10(d_L / 1 Mpc) + 25, with d_L in Mpc."""
    dL = luminosity_distance(z, Omega_m, Omega_lambda, H0)
    return 5.0 * np.log10(dL) + 25.0
