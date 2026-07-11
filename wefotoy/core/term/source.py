from __future__ import annotations


from .term import Term
from ..derivative import gradient_scalar
from ..state import State, ConservativeState
from ..thermo import Thermodynamics


class SourceTerm(Term):
    def _compute_source(self, state: State, thermo: Thermodynamics) -> ConservativeState: ...

    def compute(self, state: State, thermo: Thermodynamics) -> ConservativeState:
        return self._compute_source(state, thermo)


class PressureTerm(SourceTerm):
    def _compute_source(self, state: State, thermo: Thermodynamics) -> ConservativeState:
        _tmp = ConservativeState(self.mesh)

        _tmp.momentum.copy_(gradient_scalar(state.primitive.pressure, self.mesh).mul_(-1.0))

        return _tmp
