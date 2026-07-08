from __future__ import annotations

from .equation import Equation
from .mesh import Mesh
from . import integration


class Simulation():
    mesh: Mesh
    equation: Equation
    integrator: integration.TimeIntegrator

    def __init__(self, mesh: Mesh) -> None:
        self.equation = Equation(mesh)
        self.integrator = integration.EulerForward()
        self.mesh = mesh
