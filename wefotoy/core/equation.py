from __future__ import annotations

from .mesh import Mesh
from .scheme.scheme import NumericalSchemes
from .state import State, ConservativeState
from .term.term import Term
from .term.flux import AdvectionTerm
from .term.source import PressureTerm
from .thermo import Thermodynamics


class Equation:
    rhs: ConservativeState
    state: State
    terms: list[Term]
    thermo: Thermodynamics

    def __init__(self, mesh: Mesh, schemes: NumericalSchemes) -> None:
        self.rhs = ConservativeState(mesh)
        self.state = State(mesh, schemes)
        self.thermo = Thermodynamics()
        self.terms = [
            AdvectionTerm(mesh, schemes),
            PressureTerm(mesh, schemes)
        ]

    def update(self) -> None:
        self.state.primitive.update(self.state.conservative, self.thermo)

    def compute_rhs(self, state: State) -> ConservativeState:
        self.rhs.zero_()
        for term in self.terms:
            self.rhs.add_(term.compute(state, self.thermo))

        return self.rhs
