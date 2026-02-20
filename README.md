# GenMap

Lightweight oceanographic visualization framework built on top of Matplotlib and Cartopy.

GenMap was designed to simplify the creation of publication-ready geospatial maps for oceanographic applications such as SST, chlorophyll, wind fields, sea level anomaly and surface currents.

---

## ✨ Features

- Clean object-oriented API
- Preset configurations for common oceanographic variables
- Automatic registration of custom CPT colormaps
- Optional Natural Earth state boundaries
- Scale bar support
- Flexible gridline styling
- Designed for scientific reproducibility

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/your-username/genmap.git
cd genmap
pip install -e .
```

## 🌊 Field Presets

| Field    | Colormap        | Extra       |
|----------|----------------|-------------|
| `sst`    | `genmap_sst`   | —           |
| `chl`    | `viridis` (log scale) | —     |
| `sla`    | `RdBu_r`       | —           |
| `wind`   | `plasma`       | quiver      |
| `current`| `cmo.speed`*   | streamlines |

\* if `cmocean` is installed.

## 🎨 Custom Colormaps

GenMap automatically registers CPT-based colormaps at import time.

Included palettes:

- `genmap_sst`
- `genmap_rainbow`

They can be used directly in Matplotlib:

```python
plt.imshow(data, cmap="genmap_sst")
```
