from __future__ import annotations

from .equation import Equation
from .field import Scalar
from .mesh import Mesh


class TimeIntegrator:
    dt: float
    limiters: dict[str, TimeStepLimiter]

    def __init__(self) -> None:
        self.dt = 0.0001
        self.limiters = {
            'CFL': CFLTimeStepLimiter()
        }

    def _advance(self, equation: Equation) -> None: ...

    def _compute_dt(self, mesh: Mesh, equation: Equation) -> float:
        return min(
            (limiter.max_time_step(mesh, equation) for limiter in self.limiters.values()),
            default=self.dt,
        )

    def advance(self, mesh: Mesh, equation: Equation) -> None:
        self.dt = self._compute_dt(mesh, equation)
        self._advance(equation)


class EulerForward(TimeIntegrator):
    def __init__(self) -> None:
        super().__init__()

    def _advance(self, equation: Equation) -> None:
        equation.state.conservative.add_(equation.compute_rhs(equation.state).mul_(self.dt))


class TimeStepLimiter:
    target: float

    def __init__(self, target: float) -> None:
        self.target = target

    def max_time_step(self, mesh: Mesh, equation: Equation) -> float: ...
    def compute(self, mesh: Mesh, equation: Equation, dt: float) -> Scalar: ...


class CFLTimeStepLimiter(TimeStepLimiter):
    def __init__(self, target: float = 0.5) -> None:
        super().__init__(target)

    def max_time_step(self, mesh: Mesh, equation: Equation) -> float:
        return (
            self.target * mesh.dx
            / max(
                equation.state.primitive.velocity.norm().max(),
                equation.thermo.speed_of_sound(equation.state.conservative).max()
            )
        )

    def compute(self, mesh: Mesh, equation: Equation, dt: float) -> Scalar:
        return (
            equation.state.primitive.velocity.norm().maximum(
                equation.thermo.speed_of_sound(equation.state.conservative)
            ).mul_(dt/mesh.dx)
        )
