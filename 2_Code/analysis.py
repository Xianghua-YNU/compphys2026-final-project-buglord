# Analysis and plotting utilities: corner plot of posterior and mu(z) fit plot.

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


def plot_corner(samples, labels=None, filename="corner.png"):
    """
    Draw a corner/triangle plot for posterior samples.
    If labels is None, generate sensible labels for 2D/3D cases.
    """
    ensure_output_dir()
    ndim = samples.shape[1]
    if labels is None:
        if ndim == 2:
            labels = [r"$\Omega_m$", r"$\mu_0$"]
        elif ndim == 3:
            labels = [r"$\Omega_m$", r"$\Omega_\Lambda$", r"$\mu_0$"]
        else:
            labels = [f"p{i}" for i in range(ndim)]
    fig = corner.corner(samples, labels=labels, truths=None, show_titles=True)
    fig.savefig(os.path.join(OUTPUT_DIR, filename), dpi=150)
    plt.close(fig)


def plot_mu_z(z, mu_obs, mu_err, samples, filename="mu_fit.png", n_models=100, seed=None):
    """
    Plot data and a subset of model realizations drawn from samples.
    Assumes samples shape is (N_samples, n_params) and that mu0 is the last parameter.
    """
    ensure_output_dir()
    rng = np.random.default_rng(seed)
    nsamp = len(samples)
    if nsamp == 0:
        raise ValueError("samples is empty")

    idx = rng.choice(nsamp, size=min(n_models, nsamp), replace=False)
    zgrid = np.linspace(np.min(z) * 0.95, np.max(z) * 1.05, 200)

    plt.figure(figsize=(8, 6))

    for i in idx:
        Om = samples[i][0]
        mu0 = samples[i][-1]  # take last column as mu0 (works for 2D and 3D cases)
        mu_model = distance_modulus(zgrid, Om) + mu0
        plt.plot(zgrid, mu_model, color="C0", alpha=0.05)

    med = np.median(samples, axis=0)
    Om_med = med[0]
    mu0_med = med[-1]
    mu_med = distance_modulus(zgrid, Om_med) + mu0_med
    plt.plot(zgrid, mu_med, color="C1", lw=2, label="posterior median")

    plt.errorbar(z, mu_obs, yerr=mu_err, fmt="o", ms=4, color="k", label="data")
    plt.xlabel("z")
    plt.ylabel("Distance modulus (mag) or $\mu$")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, filename), dpi=150)
    plt.close()
