from __future__ import annotations

from .diagnostic import velocity_norm
from .equation import Equation
from .field import Scalar
from .scheme.scheme import NumericalSchemes
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

    def _compute_dt(self, mesh: Mesh, schemes: NumericalSchemes, equation: Equation) -> float:
        return min(
            (limiter.max_time_step(mesh, schemes, equation) for limiter in self.limiters.values()),
            default=self.dt,
        )

    def advance(self, mesh: Mesh, schemes: NumericalSchemes, equation: Equation) -> None:
        self.dt = self._compute_dt(mesh, schemes, equation)
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

    def max_time_step(self, mesh: Mesh, schemes: NumericalSchemes, equation: Equation) -> float: ...
    def compute(self, mesh: Mesh, schemes: NumericalSchemes, equation: Equation, dt: float) -> Scalar: ...


class CFLTimeStepLimiter(TimeStepLimiter):
    def __init__(self, target: float = 0.5) -> None:
        super().__init__(target)

    def max_time_step(self, mesh: Mesh, schemes: NumericalSchemes, equation: Equation) -> float:
        return (
            self.target * mesh.dx
            / max(
                velocity_norm(equation.state.primitive.velocity, schemes).max(),
                equation.thermo.speed_of_sound(equation.state.conservative.tracers['potential_temperature']).max()
            )
        )

    def compute(self, mesh: Mesh, schemes: NumericalSchemes, equation: Equation, dt: float) -> Scalar:
        return (
            velocity_norm(equation.state.primitive.velocity, schemes).maximum(
                equation.thermo.speed_of_sound(equation.state.conservative.tracers['potential_temperature'])
            ).mul_(dt/mesh.dx)
        )
