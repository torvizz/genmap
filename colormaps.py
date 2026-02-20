# src/genmap/colormaps.py

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
from pathlib import Path


BASE_DIR = Path(__file__).parent
PALETTE_DIR = BASE_DIR / "color_paletes"


def _load_cpt(path: Path):

    if not path.exists():
        raise FileNotFoundError(f"CPT file not found: {path}")

    x = []
    r = []
    g = []
    b = []

    color_model = "RGB"

    with open(path, "r") as f:
        lines = f.readlines()

    for line in lines:
        if line.startswith("#"):
            if "HSV" in line:
                color_model = "HSV"
            continue

        parts = line.split()
        if parts[0] in ("B", "F", "N"):
            continue

        x0, r0, g0, b0, x1, r1, g1, b1 = map(float, parts[:8])

        x.extend([x0, x1])
        r.extend([r0, r1])
        g.extend([g0, g1])
        b.extend([b0, b1])

    x = np.array(x)
    r = np.array(r)
    g = np.array(g)
    b = np.array(b)

    if color_model == "RGB":
        r /= 255.0
        g /= 255.0
        b /= 255.0

    x_norm = (x - x.min()) / (x.max() - x.min())

    color_dict = {
        "red":   [(x_norm[i], r[i], r[i]) for i in range(len(x))],
        "green": [(x_norm[i], g[i], g[i]) for i in range(len(x))],
        "blue":  [(x_norm[i], b[i], b[i]) for i in range(len(x))],
    }

    return color_dict


def _register_custom_colormaps():
    """
    Register custom GenMap colormaps.
    Safe to call multiple times.
    """

    try:
        rainbow_dict = _load_cpt(PALETTE_DIR / "rainbow.cpt")
        sst_dict     = _load_cpt(PALETTE_DIR / "sst.cpt")

        rainbow_cm = LinearSegmentedColormap("genmap_rainbow", rainbow_dict)
        sst_cm     = LinearSegmentedColormap("genmap_sst", sst_dict)

        plt.colormaps.register(rainbow_cm, force=True)
        plt.colormaps.register(sst_cm, force=True)

    except Exception as e:
        raise RuntimeError(f"Error registering GenMap colormaps: {e}")


# Register automatically at import
_register_custom_colormaps()
