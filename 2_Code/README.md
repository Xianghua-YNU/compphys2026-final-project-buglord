
This directory implements the emcee-based MCMC pipeline to fit the matter density parameter Omega_m
from Type Ia supernova distance modulus data.

Files
- cosmology.py : cosmological model functions (E(z), comoving distance, luminosity distance, distance modulus).
- data_utils.py: small helper to load a CSV with columns z, mu, mu_err.
- emcee_fit.py : likelihood / prior / emcee run wrapper. Fits parameters (Omega_m, mu0).
- emcee_fit_2d.py : emcee run wrapper to fit (Omega_m, Omega_lambda, mu0).
- ls_fit.py   : least-squares frequentist fit for comparison.
- analysis.py  : plotting helpers (corner, mu(z) fit visualization).
- main.py      : entrypoint for single fit. Example usage below.
- run_all.py   : convenience script to run the MCMC 1D, MCMC 2D, and least-squares comparison.
- requirements.txt : Python dependencies for this directory.

How to run
1) Install dependencies:
   pip install -r 2_Code/requirements.txt
   pip install emcee

3) Run a quick full pipeline (recommended for first test):
   python 2_Code/run_all.py --data 3_Data/processed_data/sn_sample.csv --quick

4) Or run a longer MCMC for production-quality results:
   python 2_Code/run_all.py --data 3_Data/processed_data/sn_sample.csv

5) If you want to reproduce more complete results, please use this: python -m 2_Code.run_all --data 3_Data/raw_data/all_sample.csv --quick

Outputs
- 2_Code/output/ contains a set of files:
  - samples_omega_m.npz
  - corner_omega_m.png
  - mu_fit_omega_m.png
  - samples_omega_m_omega_lambda.npz
  - corner_omega_m_omega_lambda.png
  - mu_fit_omega_m_omega_lambda.png
  - ls_fit_omega_m.txt

Notes
- H0 is fixed at 70 km/s/Mpc by default; mu0 is included as a nuisance parameter absorbing absolute magnitude/H0 degeneracy.
- The 2D fit includes Omega_lambda as a free parameter; priors are broad but constrained to avoid pathological regions.
