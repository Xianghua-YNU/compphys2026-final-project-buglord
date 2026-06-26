This directory implements an emcee-based MCMC pipeline to fit cosmological parameters
(from Type Ia supernova distance modulus data) and compares Bayesian (emcee) and
frequentist (least-squares) fits.

Files
- cosmology.py         : cosmological model functions (E(z), comoving distance, luminosity distance, distance modulus).
- data_utils.py        : helper to load a CSV with columns z, mu, mu_err.
- emcee_fit.py         : likelihood/prior and emcee wrapper for (Omega_m, mu0).
- emcee_fit_2d.py      : emcee wrapper to fit (Omega_m, Omega_lambda, mu0).
- ls_fit.py            : least-squares frequentist fit for comparison.
- analysis.py          : plotting helpers (corner plot, mu(z) fit visualization).
- main.py              : entrypoint for single fit runs.
- run_all.py           : convenience script to run MCMC 1D, MCMC 2D, and least-squares comparison.
- requirements.txt     : Python dependencies for this directory.
- output/              : generated samples, diagnostic plots, and fit summaries.

How to run
1) Install dependencies:
   pip install -r 2_Code/requirements.txt
   pip install emcee

2) Quick test (fast, recommended for first run):
   python 2_Code/run_all.py --data 3_Data/processed_data/sn_sample.csv --quick

3) Full run (longer, more samples):
   python 2_Code/run_all.py --data 3_Data/processed_data/sn_sample.csv

Outputs
- 2_Code/output/ contains:
  - samples_omega_m.npz
  - corner_omega_m.png
  - mu_fit_omega_m.png
  - samples_omega_m_omega_lambda.npz
  - corner_omega_m_omega_lambda.png
  - mu_fit_omega_m_omega_lambda.png
  - ls_fit_omega_m.txt

Notes and important fixes
- H0 is fixed at 70 km/s/Mpc by default; mu0 is included as a nuisance parameter absorbing absolute magnitude/H0 degeneracy.
- The 2D fit includes Omega_lambda as a free parameter; priors are broad but constrained to avoid pathological regions.
- Visualisation fix: the mu(z) plotting routine previously used a hard-coded mu0 = 0.3 for drawing model realizations. This has been fixed so that the plotted curves are drawn using the mu0 values from the posterior samples (see analysis.py). If you have previously generated mu_fit_*.png before this fix, re-run the pipeline to regenerate the plots so they reflect the posterior properly.
- For reproducibility, plot functions accept an optional seed parameter (see analysis.plot_mu_z).

Notes on numerical/physical robustness
- E(z) uses a small floor inside sqrt to avoid negative values from extreme/unphysical parameters; this avoids complex numbers but can hide parameter choices that are physically invalid — treat out-of-bound fits with caution.
- If you change priors or parameter bounds, re-check the sampling diagnostics (autocorrelation, acceptance fraction, and trace plots).

Contact / debugging
- If you see NaNs or exceptions during integration in cosmology.comoving_distance, check that the sampled Omega_m/Omega_lambda are within reasonable ranges. The integration uses scipy.integrate.quad and will work for typical cosmological parameters.
