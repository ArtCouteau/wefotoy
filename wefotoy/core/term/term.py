from __future__ import annotations

from ..mesh import Mesh
from ..scheme.scheme import NumericalSchemes
from ..state import State, ConservativeState
from ..thermo import Thermodynamics


class Term:
    mesh: Mesh
    schemes: NumericalSchemes

    def __init__(self, mesh: Mesh, schemes: NumericalSchemes) -> None:
        self.mesh = mesh
        self.schemes = schemes

    def compute(self, state: State, thermo: Thermodynamics) -> ConservativeState: ...
