from __future__ import annotations

from .integration import EulerForward, TimeIntegrator
from .interpolation import Interpolator, LinearInterpolator
from .reconstruction import LinearInterpolationReconstructor, Reconstructor


class NumericalSchemes:
    integrator: TimeIntegrator
    interpolator: Interpolator
    reconstructor: Reconstructor

    def __init__(self) -> None:
        self.integrator = EulerForward()
        self.interpolator = LinearInterpolator()
        self.reconstructor = LinearInterpolationReconstructor()
