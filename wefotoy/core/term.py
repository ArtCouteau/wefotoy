from __future__ import annotations

from .field import Vector, Matrix, Direction
from . import derivative, equation, interpolation


class NavierStokesRHS(equation.NavierStokesConservedVariable):
    ...

    def __mul__(self, other: int | float) -> NavierStokesRHS:
        self.density.mul_(other)
        self.momentum.x.mul_(other)
        self.momentum.y.mul_(other)
        self.potentialTemperatureDensity.mul_(other)

        return self

    def __rmul__(self, other: int | float) -> NavierStokesRHS:
        return self.__mul__(other)


class NavierStokesTerm:
    equation: equation.NavierStokesEquation

    def __init__(self, navierStokes: equation.NavierStokesEquation) -> None:
        self.equation = navierStokes

    def compute(self) -> NavierStokesRHS: ...


class NavierStokesFlux:
    density: Vector
    momentum: Matrix
    potentialTemperatureDensity: Vector


class NavierStokesFluxTerm(NavierStokesTerm):
    def _compute_flux(self) -> NavierStokesFlux: ...

    def compute(self) -> NavierStokesRHS:
        _rhs = NavierStokesRHS()
        _flux = self._compute_flux()

        _rhs.density.copy_(derivative.divergence_vector(_flux.density))
        _rhs.momentum.x.copy_(derivative.divergence_vector(_flux.momentum.x))
        _rhs.momentum.y.copy_(derivative.divergence_vector(_flux.momentum.y))
        _rhs.potentialTemperatureDensity.copy_(derivative.divergence_vector(_flux.potentialTemperatureDensity))

        return _rhs


class NavierStokesAdvectionTerm(NavierStokesFluxTerm):
    def __init__(self, navierStokes: equation.NavierStokesEquation) -> None:
        super().__init__(navierStokes)

    def _compute_flux(self) -> NavierStokesFlux:
        _flux = NavierStokesFlux()
        _cons = self.equation.variable.conserved
        _prim = self.equation.variable.primitive

        _flux.density = _cons.momentum

        _flux.momentum = Matrix(
            Vector(
                interpolation.linear(_cons.momentum.x, Direction.X)
                * self.equation.reconstructor.velocity.apply(_prim.velocity.x, _prim.velocity.x, Direction.X),
                interpolation.linear(_cons.momentum.y, Direction.X)
                * self.equation.reconstructor.velocity.apply(_prim.velocity.x, _prim.velocity.y, Direction.Y)
            ),
            Vector(
                interpolation.linear(_cons.momentum.x, Direction.Y)
                * self.equation.reconstructor.velocity.apply(_prim.velocity.y, _prim.velocity.x, Direction.X),
                interpolation.linear(_cons.momentum.y, Direction.Y)
                * self.equation.reconstructor.velocity.apply(_prim.velocity.y, _prim.velocity.y, Direction.Y)
            )
        )

        _flux.potentialTemperatureDensity = Vector(
            self.equation.reconstructor.scalar.apply(
                _prim.potentialTemperature, _prim.velocity.x, Direction.X
            ) * _cons.momentum.x,
            self.equation.reconstructor.scalar.apply(
                _prim.potentialTemperature, _prim.velocity.y, Direction.Y
            ) * _cons.momentum.y
        )

        return _flux


class NavierStokesSourceTerm(NavierStokesTerm):
    def __init__(self, navierStokes: equation.NavierStokesEquation) -> None:
        super().__init__(navierStokes)

    def _compute_source(self) -> NavierStokesRHS: ...

    def compute(self) -> NavierStokesRHS:
        return self._compute_source()


class NavierStokesPressureTerm(NavierStokesSourceTerm):
    def _compute_source(self) -> NavierStokesRHS:
        _rhs = NavierStokesRHS()

        _pressureGrad = derivative.gradient_scalar(self.equation.variable.primitive.pressure)
        _rhs.momentum.x.copy_(- _pressureGrad.x)
        _rhs.momentum.x.copy_(- _pressureGrad.y)

        return _rhs
