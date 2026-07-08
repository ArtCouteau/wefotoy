from __future__ import annotations

from . import equation


class TimeIntegrator:
    dt: float

    def __init__(self) -> None:
        self.dt = 0.01

    def advance(self, navierStokes: equation.NavierStokesEquation) -> None: ...


class EulerForward(TimeIntegrator):
    def __init__(self) -> None:
        super().__init__()

    def advance(self, navierStokes: equation.NavierStokesEquation) -> None:
        navierStokes.variable.conserved.add_(self.dt * navierStokes.rhs())
