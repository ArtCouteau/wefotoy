from __future__ import annotations

from ..equation import Equation


class TimeIntegrator:
    dt: float

    def __init__(self) -> None:
        self.dt = 0.01

    def advance(self, equation: Equation) -> None: ...


class EulerForward(TimeIntegrator):
    def __init__(self) -> None:
        super().__init__()

    def advance(self, equation: Equation) -> None:
        equation.state.conservative.add_(equation.compute_rhs(equation.state).mul_(self.dt))
