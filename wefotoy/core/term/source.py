from __future__ import annotations


from .term import Term
from ..state import State, ConservativeState
from ..thermo import Thermodynamics


class SourceTerm(Term):
    def _compute_source(self, state: State, thermo: Thermodynamics) -> ConservativeState: ...

    def compute(self, state: State, thermo: Thermodynamics) -> ConservativeState:
        return self._compute_source(state, thermo)


class PressureTerm(SourceTerm):
    def _compute_source(self, state: State, thermo: Thermodynamics) -> ConservativeState:
        _tmp = ConservativeState(self.mesh)

        _tmp.momentum.copy_(self.mesh.gradient_scalar(state.primitive.pressure).mul_(-1.0))

        return _tmp
