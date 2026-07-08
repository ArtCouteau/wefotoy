from __future__ import annotations

from .mesh import Mesh
from . import integration, equation


class Simulation():
    mesh: Mesh
    navierStokes: equation.NavierStokesEquation
    integrator: integration.TimeIntegrator

    def __init__(self, mesh: Mesh) -> None:
        self.navierStokes = equation.NavierStokesEquation()
        self.integrator = integration.EulerForward()
        self.mesh = mesh
