# src/genmap/fields.py

FIELD_PRESETS = {

    "sst": dict(
        cmap="genmap_sst",
        logscale=False,
        label="Sea Surface Temperature (°C)",
    ),

    "chl": dict(
        cmap="genmap_rainbow",
        logscale=True,
        label="Chlorophyll-a (mg m⁻³)",
    ),

    "sla": dict(
        cmap="RdBu_r",
        logscale=False,
        label="Sea Level Anomaly (cm)",
    ),

    "wind": dict(
        cmap="genmap_rainbow",
        logscale=False,
        label="Wind speed (m s⁻¹)",
        vectors=True,
    ),

    "current": dict(
        cmap="cmo.speed",  # exemplo se usar cmocean
        logscale=False,
        label="Current speed (m s⁻¹)",
        streamlines=True,
    ),
}
