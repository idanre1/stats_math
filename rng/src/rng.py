"""One seed policy for every random draw: a top-level seed plus named child streams."""

from __future__ import annotations

import hashlib

import numpy as np


def make_rng(seed: int | None, stream: str | None = None) -> np.random.Generator:
    """Create a NumPy generator from a top-level seed and an optional stream name.

    Use one top-level ``seed`` per run and give each stochastic component its own
    ``stream`` (e.g. ``"bootstrap"``, ``"alacpd::det1"``). Components then draw
    independent numbers that do not shift when another component changes how many
    draws it makes.

    Parameters
    ----------
    seed : int or None
        Top-level seed. An int gives bit-identical reruns; ``None`` uses OS entropy
        (never a hidden default seed).
    stream : str or None, default None
        Stable component name. ``None`` returns ``np.random.default_rng(seed)``.
        With a name, the child seed is ``SeedSequence([seed, h])`` with ``h`` the
        first 64 bits of ``sha256(stream)``, so it does not depend on Python's
        per-process ``hash`` salt.

    Returns
    -------
    numpy.random.Generator
        A PCG64 generator.

    Raises
    ------
    TypeError
        If ``seed`` is not an int or None (floats are rejected rather than truncated).

    Examples
    --------
    >>> a = make_rng(7, "bootstrap").normal(size=3)
    >>> b = make_rng(7, "bootstrap").normal(size=3)
    >>> bool((a == b).all())
    True
    >>> bool((make_rng(7, "null").normal(size=3) == a).any())
    False
    >>> isinstance(make_rng(None, "bootstrap").random(), float)
    True
    """
    if seed is not None and not isinstance(seed, (int, np.integer)):
        raise TypeError(f"seed must be int or None, got {type(seed).__name__}")
    if stream is None:
        return np.random.default_rng(seed)
    if seed is None:
        return np.random.default_rng(np.random.SeedSequence(None).spawn(1)[0])
    stream_key = int(hashlib.sha256(stream.encode("utf-8")).hexdigest()[:16], 16)
    return np.random.default_rng(np.random.SeedSequence([int(seed), stream_key]).spawn(1)[0])
