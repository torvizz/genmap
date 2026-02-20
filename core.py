import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.colors import LogNorm
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.feature import NaturalEarthFeature
from geopy.distance import distance
from .fields import FIELD_PRESETS

class GenMap:
    """
    Helper class for generating publication-ready geospatial maps
    using Cartopy and Matplotlib.

    Parameters
    ----------
    N : float
        Northern latitude boundary.
    S : float
        Southern latitude boundary.
    E : float
        Eastern longitude boundary.
    W : float
        Western longitude boundary.
    projection : cartopy.crs projection, optional
        Map projection. Default is PlateCarree.
    figsize : tuple, optional
        Figure size in inches.
    tick_step : tuple, optional
        Step size for (latitude, longitude) ticks.
    tick_init : tuple, optional
        Initial offset for tick generation.
    degree_format : str, optional
        Format string for degree labels.
    """

    def __init__(
        self,
        N, S, E, W,
        projection=ccrs.PlateCarree(),
        figsize=(8, 6),
        tick_step=(1, 1),
        tick_init=(0, 0),
        degree_format="%.0f"
    ):

        self.N, self.S, self.E, self.W = N, S, E, W
        self.proj = projection

        self.fig = plt.figure(figsize=figsize)
        self.ax = self.fig.add_subplot(1, 1, 1, projection=projection)

        self.ax.set_extent([W, E, S, N], crs=projection)

        self._configure_ticks(tick_step, tick_init)
        self._add_default_features()

        self.fig.tight_layout()
        self.savefig = self.fig.savefig

    # ----------------------------------------------------------
    # INTERNAL UTILITIES
    # ---------------------------------------------------------

    def _mesh(self, lat, lon):
        """
        Ensure latitude and longitude arrays are 2D.

        Parameters
        ----------
        lat : ndarray
            Latitude array (1D or 2D).
        lon : ndarray
            Longitude array (1D or 2D).

        Returns
        -------
        lon2d, lat2d : ndarray
            2D longitude and latitude arrays.

        Raises
        ------
        TypeError
            If lat and lon dimensions do not match.
        """
        if lat.ndim == 1 and lon.ndim == 1:
            return np.meshgrid(lon, lat)
        elif lat.ndim == 2 and lon.ndim == 2:
            return lon, lat
        else:
            raise TypeError(
                "lat and lon must both be 1D arrays or both be 2D arrays."
            )

    def _configure_ticks(self, tick_step, tick_init):
        """
        Configure gridlines and tick positions.
        """

        yticks = np.arange(
            self.S + tick_init[0],
            self.N + tick_step[0],
            tick_step[0]
        )

        xticks = np.arange(
            self.W + tick_init[1],
            self.E + tick_step[1],
            tick_step[1]
        )

        self.ax.set_xticks(xticks, crs=self.proj)
        self.ax.set_yticks(yticks, crs=self.proj)

        self.ax.gridlines(
            draw_labels=False,
            linewidth=0.5,
            linestyle="--",
            alpha=0.3
        )

    def _add_default_features(self):
        """
        Add default geographic features:
        coastlines, land mask and borders.
        """
        
        states = NaturalEarthFeature(
            category="cultural",
            name="admin_1_states_provinces_lines",
            scale='10m',
            facecolor="none"
        )

        self.ax.coastlines(resolution="10m")
        self.ax.add_feature(cfeature.LAND, facecolor="0.8")
        self.ax.add_feature(cfeature.BORDERS, linewidth=0.5)
        self.ax.add_feature(
            states,
            linewidth=0.3,
            edgecolor="black",
            zorder=2.1
        )

    # ---------------------------------------------------------
    # GENERIC PLOTTING METHODS
    # ---------------------------------------------------------

    def contourf(
        self,
        lat,
        lon,
        data,
        levels=None,
        cmap="viridis",
        vmin=None,
        vmax=None,
        logscale=False,
        extend="both"
    ):
        """
        Plot filled contours.

        Parameters
        ----------
        lat : ndarray
            Latitude array.
        lon : ndarray
            Longitude array.
        data : ndarray
            2D data array.
        levels : array-like, optional
            Contour levels.
        cmap : str or Colormap
            Colormap.
        vmin, vmax : float, optional
            Color limits.
        logscale : bool, optional
            If True, use logarithmic normalization.
        extend : str, optional
            Colorbar extension behavior.

        Returns
        -------
        QuadContourSet
        """

        lonx, laty = self._mesh(lat, lon)

        norm = LogNorm(vmin=vmin, vmax=vmax) if logscale else None

        self.ctf = self.ax.contourf(
            lonx,
            laty,
            data,
            levels=levels,
            cmap=cmap,
            vmin=vmin,
            vmax=vmax,
            norm=norm,
            extend=extend,
            transform=self.proj
        )

        return self.ctf

    def quiver(
        self,
        lat,
        lon,
        u,
        v,
        step=None,
        scale=25,
        scale_units="inches"
    ):
        """
        Plot vector field using quiver.

        Parameters
        ----------
        lat, lon : ndarray
            Coordinates.
        u, v : ndarray
            Vector components.
        step : int, optional
            Subsampling step.
        scale : float
            Arrow scaling factor.
        scale_units : str
            Units for scaling.

        Returns
        -------
        Quiver
        """

        lonx, laty = self._mesh(lat, lon)

        if step:
            lonx = lonx[::step, ::step]
            laty = laty[::step, ::step]
            u = u[::step, ::step]
            v = v[::step, ::step]

        self.qv = self.ax.quiver(
            lonx,
            laty,
            u,
            v,
            scale=scale,
            scale_units=scale_units,
            transform=self.proj
        )

        return self.qv

    # ---------------------------------------------------------
    # COLORBAR
    # ---------------------------------------------------------

    def add_colorbar_by_coords(
        self,
        x0, y0,
        x1, y1,
        orientation="horizontal",
        **kwargs
    ):
        """
        Add colorbar positioned using data coordinates.

        Parameters
        ----------
        x0, y0 : float
            Lower-left data coordinate.
        x1, y1 : float
            Upper-right data coordinate.
        orientation : str
            'horizontal' or 'vertical'.

        Returns
        -------
        Colorbar
        """

        p0 = self.ax.transData.transform((x0, y0))
        p1 = self.ax.transData.transform((x1, y1))

        x0f, y0f = self.fig.transFigure.inverted().transform(p0)
        x1f, y1f = self.fig.transFigure.inverted().transform(p1)

        cbax = self.fig.add_axes([
            x0f,
            y0f,
            x1f - x0f,
            y1f - y0f
        ])

        self.cbar = self.fig.colorbar(
            self.ctf,
            cax=cbax,
            orientation=orientation,
            **kwargs
        )

        return self.cbar
    
    # ---------------------------------------------------------
    # SCALEBAR
    # ---------------------------------------------------------
    
    def add_scalebar(
        self,
        length_km,
        location=(0.5, 0.05),
        linewidth=3,
        text_offset=0.01,
        fontsize=10,
    ):
        """
        Add a horizontal scale bar.

        Parameters
        ----------
        length_km : float
            Length of scale bar in kilometers.
        location : tuple
            Relative position in axes coordinates (0–1).
        linewidth : float
            Line thickness.
        text_offset : float
            Vertical offset (axes fraction).
        fontsize : int
            Label font size.
        """

        # Convert axes fraction → data coordinates
        x_frac, y_frac = location
        lon_center = self.W + x_frac * (self.E - self.W)
        lat_pos = self.S + y_frac * (self.N - self.S)

        # Compute km per degree at map mid-latitude
        mid_lat = (self.N + self.S) / 2

        km_per_degree = distance(
            (mid_lat, self.W),
            (mid_lat, self.W - 1)
        ).km

        degree_length = length_km / km_per_degree

        lon_left = lon_center - degree_length / 2
        lon_right = lon_center + degree_length / 2

        self.ax.plot(
            [lon_left, lon_right],
            [lat_pos, lat_pos],
            color="k",
            linewidth=linewidth,
            transform=self.proj,
            solid_capstyle="butt"
        )

        self.ax.text(
            lon_center,
            lat_pos + text_offset * (self.N - self.S),
            f"{length_km} km",
            ha="center",
            va="bottom",
            fontsize=fontsize,
            transform=self.proj
        )
