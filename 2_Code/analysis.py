"""
Analysis and plotting utilities: corner plot of posterior and mu(z) fit plot.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import corner
from .cosmology import distance_modulus


OUTPUT_DIR = "2_Code/output"


def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def save_samples(samples, filename="samples.npz"):
    ensure_output_dir()
    np.savez_compressed(os.path.join(OUTPUT_DIR, filename), samples=samples)


def plot_corner(samples, labels=[r"$\Omega_m$", r"$\mu_0$"], filename="corner.png"):
    ensure_output_dir()
    fig = corner.corner(samples, labels=labels, truths=None, show_titles=True)
    fig.savefig(os.path.join(OUTPUT_DIR, filename), dpi=150)
    plt.close(fig)


def plot_mu_z(z, mu_obs, mu_err, samples, filename="mu_fit.png", n_models=100):
    """Plot data and a subset of model realizations drawn from samples."""
    ensure_output_dir()
    # pick random posterior draws
    idx = np.random.choice(len(samples), size=min(n_models, len(samples)), replace=False)
    zgrid = np.linspace(np.min(z) * 0.95, np.max(z) * 1.05, 200)

    plt.figure(figsize=(8, 6))
    # plot posterior predictive curves
    for i in idx:
        Om, mu0 = samples[i]
        mu_model = distance_modulus(zgrid, Om) + mu0
        plt.plot(zgrid, mu_model, color="C0", alpha=0.05)

    # plot best-fit median curve
    med = np.median(samples, axis=0)
    mu_med = distance_modulus(zgrid, med[0]) + med[1]
    plt.plot(zgrid, mu_med, color="C1", lw=2, label="posterior median")

    plt.errorbar(z, mu_obs, yerr=mu_err, fmt="o", ms=4, color="k", label="data")
    plt.xlabel("z")
    plt.ylabel(r"Distance modulus (z)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, filename), dpi=150)
    plt.close()
