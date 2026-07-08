from __future__ import annotations

from .equation import Equation
from .mesh import Mesh
from .scheme.scheme import NumericalSchemes


class Simulation():
    equation: Equation
    mesh: Mesh
    schemes: NumericalSchemes

    def __init__(self, mesh: Mesh) -> None:
        self.equation = Equation(mesh)
        self.mesh = mesh
        self.schemes = NumericalSchemes()
