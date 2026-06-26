"""
Fetch Pantheon-like SN data and prepare a CSV with columns: z,mu,mu_err

This script is robust to two common data formats:
1) Pre-computed distance modulus columns (MU/dMU or mu/dmu): it will use these directly.
2) Light-curve fit outputs (mb, dmb, x1, dx1, color, dcolor): it will compute mu using
   mu = mb + alpha * x1 - beta * color - M
   and propagate uncertainties with an additional intrinsic scatter term.

Usage example:
  python fetch_and_prepare_pantheon.py --url <raw_url> --out out.csv
  python fetch_and_prepare_pantheon.py --url <raw_url> --out out.csv --alpha 0.14 --beta 3.1 --M -19.3 --sigma_int 0.12

Notes:
- Default nuisance parameters (alpha, beta, M, sigma_int) are set to reasonable values but
  you should check the data release documentation for recommended values when using a
  particular dataset (Pantheon, Pantheon+, JLA, etc.).
- If the remote file does not include MU/dMU, and also does not include the necessary
  light-curve columns, the script will raise an error asking for manual preprocessing.

AI assistance: This helper script was produced with AI assistance and reviewed by the author.
"""

import argparse
import io
from urllib.request import urlopen

import numpy as np
import pandas as pd


def download_text(url):
    with urlopen(url) as response:
        return response.read().decode('utf-8')


def try_parse_text_to_df(text):
    # Try several pandas readers to be robust to different whitespace/sep conventions
    readers = [
        lambda s: pd.read_csv(io.StringIO(s), delim_whitespace=True, comment='#', header=0, engine='python'),
        lambda s: pd.read_csv(io.StringIO(s), sep='\t', comment='#', header=0, engine='python'),
        lambda s: pd.read_csv(io.StringIO(s), sep=',', comment='#', header=0, engine='python'),
    ]
    last_err = None
    for r in readers:
        try:
            df = r(text)
            if df.shape[1] > 1:
                return df
        except Exception as e:
            last_err = e
    raise ValueError(f"Failed to parse text into DataFrame. Last error: {last_err}")


def compute_mu_from_lightcurve(df, alpha, beta, M, sigma_int):
    # required columns for this path
    required = ['mb', 'dmb', 'x1', 'dx1', 'color', 'dcolor']
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required light-curve columns to compute mu: {missing}")

    mb = df['mb'].astype(float).values
    dmb = df['dmb'].astype(float).values
    x1 = df['x1'].astype(float).values
    dx1 = df['dx1'].astype(float).values
    color = df['color'].astype(float).values
    dcolor = df['dcolor'].astype(float).values

    mu = mb + alpha * x1 - beta * color - M
    # propagate errors: dmu^2 = dmb^2 + (alpha*dx1)^2 + (beta*dcolor)^2 + sigma_int^2
    dmu = np.sqrt(dmb**2 + (alpha * dx1)**2 + (beta * dcolor)**2 + sigma_int**2)

    out = pd.DataFrame({'z': df['z'].astype(float), 'mu': mu, 'mu_err': dmu})
    return out


def prepare(df, alpha, beta, M, sigma_int):
    # First, attempt to find precomputed MU and dMU
    mu_candidates = ['MU', 'mu', 'MU0', 'MU_B']
    dmu_candidates = ['dMU', 'dmu', 'MU_err', 'dMU0', 'dMU_err']
    z_candidates = ['z', 'zcmb', 'zhel', 'Z', 'ZCMB']

    zcol = next((c for c in z_candidates if c in df.columns), None)
    mucol = next((c for c in mu_candidates if c in df.columns), None)
    dmucol = next((c for c in dmu_candidates if c in df.columns), None)

    if mucol is not None and dmucol is not None and zcol is not None:
        out = pd.DataFrame()
        out['z'] = df[zcol].astype(float)
        out['mu'] = df[mucol].astype(float)
        out['mu_err'] = df[dmucol].astype(float)
        out = out.dropna(subset=['z', 'mu', 'mu_err'])
        return out

    # If MU not present, attempt to compute from light-curve parameters
    try:
        out = compute_mu_from_lightcurve(df, alpha, beta, M, sigma_int)
        out = out.dropna(subset=['z', 'mu', 'mu_err'])
        return out
    except ValueError as e:
        # Re-raise with a helpful message
        raise ValueError(f"Could not prepare Pantheon data automatically: {e}\n"
                         f"Available columns: {list(df.columns)[:50]}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', required=True, help='Raw URL to download Pantheon-like data')
    parser.add_argument('--out', required=True, help='Output CSV path (z,mu,mu_err)')
    parser.add_argument('--alpha', type=float, default=0.14, help='Stretch-luminosity coefficient (default 0.14)')
    parser.add_argument('--beta', type=float, default=3.1, help='Color-luminosity coefficient (default 3.1)')
    parser.add_argument('--M', type=float, default=-19.3, help='Absolute magnitude (used when computing mu from mb)')
    parser.add_argument('--sigma_int', type=float, default=0.12, help='Intrinsic scatter to add in quadrature to mu_err')
    args = parser.parse_args()

    print(f"Downloading data from {args.url}")
    text = download_text(args.url)
    df = try_parse_text_to_df(text)
    print(f"Parsed table with columns: {list(df.columns)[:50]}")

    out = prepare(df, alpha=args.alpha, beta=args.beta, M=args.M, sigma_int=args.sigma_int)
    out.to_csv(args.out, index=False)
    print(f"Wrote processed CSV to {args.out} with {len(out)} rows")


if __name__ == '__main__':
    main()
