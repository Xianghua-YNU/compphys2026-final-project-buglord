# 2_Code/main.py
"""
Entry point to run MCMC fit of Omega_m using emcee on SN Ia distance modulus data.

Usage example:
  python 2_Code/main.py --data 3_Data/processed_data/sn_sample.csv --nwalkers 32 --nsteps 4000

Outputs written to 2_Code/output/ : samples.npz, corner.png, mu_fit.png
"""

import argparse
import numpy as np
import os
from .data_utils import load_sn_csv
from .emcee_fit import run_emcee
from .analysis import save_samples, plot_corner, plot_mu_z


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, required=True, help="Path to SN CSV (z,mu,mu_err)")
    parser.add_argument("--nwalkers", type=int, default=32)
    parser.add_argument("--nsteps", type=int, default=4000)
    parser.add_argument("--burn", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=None)
    return parser.parse_args()


def main():
    args = parse_args()
    z, mu, mu_err = load_sn_csv(args.data)

    print(f"Loaded {len(z)} SN points from {args.data}")

    sampler, samples = run_emcee(z, mu, mu_err, nwalkers=args.nwalkers, nsteps=args.nsteps, burn=args.burn, seed=args.seed)

    print("MCMC finished. Saving outputs...")
    save_samples(samples)
    plot_corner(samples)
    plot_mu_z(z, mu, mu_err, samples)

    print("Outputs saved to 2_Code/output/")


if __name__ == "__main__":
    main()
