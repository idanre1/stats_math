"""Curated math and statistics helpers. Submodules load on first use (PEP 562), so
``from stats_math import make_rng`` needs only numpy, not matplotlib or statsmodels."""

from importlib import import_module

_LAZY = {
    "compute_features_from_correl": "stats_math.correlation.src.corr_features",
    "estimate_kde": "stats_math.kde.src.optuna_cv",
    "get_linspace_from_kde": "stats_math.kde.src.optuna_cv",
    "plot_kde": "stats_math.kde.src.optuna_cv",
    "cdf_from_kde": "stats_math.kde.src.optuna_cv",
    "pval_from_cdf": "stats_math.kde.src.optuna_cv",
    "realized_var": "stats_math.moments.src.realized_moments",
    "realized_skew": "stats_math.moments.src.realized_moments",
    "realized_kurt": "stats_math.moments.src.realized_moments",
    "white_test": "stats_math.stats_tests.tests",
    "make_rng": "stats_math.rng.src.rng",
}
__all__ = list(_LAZY)


def __getattr__(name):
    if name not in _LAZY:
        raise AttributeError(f"module 'stats_math' has no attribute {name!r}")
    value = getattr(import_module(_LAZY[name]), name)
    globals()[name] = value
    return value


def __dir__():
    return sorted(__all__)
