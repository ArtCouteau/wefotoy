from __future__ import annotations

from .mesh import Mesh
from .state import State, ConservativeState
from .term import Term
from .thermo import Thermodynamics


class Equation:
    rhs: ConservativeState
    state: State
    terms: list[Term]
    thermo: Thermodynamics

    def __init__(self, mesh: Mesh) -> None:
        self.rhs = ConservativeState(mesh)
        self.state = State(mesh)
        self.thermo = Thermodynamics()

    def update(self) -> None:
        self.state.primitive.update(self.state.conservative, self.thermo)

    def compute_rhs(self) -> ConservativeState:
        self.rhs.zero_()
        for term in self.terms:
            self.rhs.add_(term.compute())

        return self.rhs
