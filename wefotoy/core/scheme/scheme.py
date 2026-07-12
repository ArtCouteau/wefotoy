from __future__ import annotations

from .interpolation import Interpolator, LinearInterpolator
from .reconstruction import Reconstructor


class NumericalSchemes:
    interpolator: Interpolator
    reconstructor: Reconstructor

    def __init__(self) -> None:
        self.interpolator = LinearInterpolator()
        self.reconstructor = Reconstructor()
