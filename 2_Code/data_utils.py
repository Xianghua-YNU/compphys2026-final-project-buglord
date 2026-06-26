# 2_Code/data_utils.py
"""
Data loading utilities for SN Ia sample.

Expected CSV format (header): z, mu, mu_err

This module returns numpy arrays (z, mu, mu_err).
"""

import numpy as np
import pandas as pd


def load_sn_csv(path):
    """Load a small SN sample CSV with columns: z, mu, mu_err.

    Returns:
        z, mu, mu_err as numpy arrays.
    """
    df = pd.read_csv(path)
    # Minimal validation
    required = {"z", "mu", "mu_err"}
    if not required.issubset(df.columns):
        raise ValueError(f"CSV at {path} must contain columns: {required}")
    z = df["z"].values
    mu = df["mu"].values
    mu_err = df["mu_err"].values
    return z, mu, mu_err
