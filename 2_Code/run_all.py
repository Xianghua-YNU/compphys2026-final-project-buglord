# 2_Code/run_all.py
"""
Coordinator script to run both MCMC fits (1D Omega_m and 2D Omega_m/Omega_lambda),
and the frequentist least-squares fit for comparison. Saves outputs in 2_Code/output/.

Usage example:
    python 2_Code/run_all.py --data 3_Data/processed_data/sn_sample.csv --quick

--quick reduces nsteps for fast testing.
"""
import argparse
import numpy as np
import os
from .data_utils import load_sn_csv
from .emcee_fit import run_emcee
from .emcee_fit_2d import run_emcee_2d
from .ls_fit import fit_least_squares
from .analysis import save_samples, plot_corner, plot_mu_z


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, required=True)
    parser.add_argument("--quick", action="store_true", help="Use fewer steps for quick test")
    return parser.parse_args()


def main():
    args = parse_args()
    z, mu, mu_err = load_sn_csv(args.data)

    # Quick or full settings
    if args.quick:
        nwalkers, nsteps, burn = 16, 500, 100
    else:
        nwalkers, nsteps, burn = 32, 2000, 500

    print("Running 1D Omega_m emcee fit...")
    sampler1, samples1 = run_emcee(z, mu, mu_err, nwalkers=nwalkers, nsteps=nsteps, burn=burn)
    save_samples(samples1, filename="samples_omega_m.npz")
    plot_corner(samples1, labels=[r"$\Omega_m$", r"$\mu_0$"], filename="corner_omega_m.png")
    plot_mu_z(z, mu, mu_err, samples1, filename="mu_fit_omega_m.png")

    print("Running 2D Omega_m/Omega_lambda emcee fit...")
    sampler2, samples2 = run_emcee_2d(z, mu, mu_err, nwalkers=max(32, nwalkers), nsteps=nsteps, burn=burn)
    # Save only Omega_m, Omega_lambda, mu0 samples
    save_samples(samples2, filename="samples_omega_m_omega_lambda.npz")
    plot_corner(samples2, labels=[r"$\Omega_m$", r"$\Omega_\Lambda$", r"$\mu_0$"], filename="corner_omega_m_omega_lambda.png")
    plot_mu_z(z, mu, mu_err, samples2, filename="mu_fit_omega_m_omega_lambda.png")

    print("Running least-squares fit for comparison...")
    res = fit_least_squares(z, mu, mu_err, fit_omega_lambda=False)
    print("Least-squares result (Omega_m, mu0):", res.x)

    # Save LS result
    out_dir = "2_Code/output"
    os.makedirs(out_dir, exist_ok=True)
    np.savetxt(os.path.join(out_dir, "ls_fit_omega_m.txt"), res.x)

    print("All tasks completed. Outputs are in 2_Code/output/")

if __name__ == '__main__':
    main()
