from __future__ import annotations

from . import integration, equation


class Simulation():
    navierStokes: equation.NavierStokesEquation
    integrator: integration.TimeIntegrator

    def __init__(self) -> None:
        self.navierStokes = equation.NavierStokesEquation()
        self.integrator = integration.EulerForward()
