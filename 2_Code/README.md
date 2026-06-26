# 2_Code/README.md

This directory implements the emcee-based MCMC pipeline to fit the matter density parameter Omega_m
from Type Ia supernova distance modulus data.

Files
- cosmology.py : cosmological model functions (E(z), comoving distance, luminosity distance, distance modulus).
- data_utils.py: small helper to load a CSV with columns z, mu, mu_err.
- emcee_fit.py : likelihood / prior / emcee run wrapper. Fits parameters (Omega_m, mu0).
- analysis.py  : plotting helpers (corner plot and mu(z) fit visualization).
- main.py      : entrypoint. Example usage below.
- requirements.txt : Python dependencies for this directory.

How to run
1) Install dependencies:
   pip install -r 2_Code/requirements.txt

2) Run the MCMC pipeline (example):
   python 2_Code/main.py --data 3_Data/processed_data/sn_sample.csv --nwalkers 32 --nsteps 4000

Outputs
- 2_Code/output/samples.npz : compressed numpy archive containing posterior samples (samples key)
- 2_Code/output/corner.png  : corner plot of posterior
- 2_Code/output/mu_fit.png  : mu(z) with posterior predictive curves

Notes
- H0 is fixed at 70 km/s/Mpc by default; mu0 is included as a nuisance parameter absorbing absolute magnitude/H0 degeneracy.
- The code includes brief AI-assistance declarations in file headers where relevant.
