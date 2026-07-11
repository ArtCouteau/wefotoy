from __future__ import annotations


from .term import Term
from ..defs import Direction, AxisLocation, Location
from ..derivative import divergence_vector, divergence_matrix
from ..field import Vector, Matrix, scalar_zeros
from ..mesh import Mesh
from ..state import State, ConservativeState
from ..thermo import Thermodynamics


class Flux:
    density: Vector
    momentum: Matrix
    tracers: dict[str, Vector]

    def __init__(self, mesh: Mesh) -> None:
        self.density = Vector(
            scalar_zeros(Location(AxisLocation.FACE, AxisLocation.CENTER), mesh),
            scalar_zeros(Location(AxisLocation.CENTER, AxisLocation.FACE), mesh)
        )
        self.momentum = Matrix(
            Vector(
                scalar_zeros(Location(AxisLocation.CENTER, AxisLocation.CENTER), mesh),
                scalar_zeros(Location(AxisLocation.FACE, AxisLocation.FACE), mesh)
            ),
            Vector(
                scalar_zeros(Location(AxisLocation.FACE, AxisLocation.FACE), mesh),
                scalar_zeros(Location(AxisLocation.CENTER, AxisLocation.CENTER), mesh)
            )
        )
        self.tracers = {
            'potential_temperature': Vector(
                scalar_zeros(Location(AxisLocation.FACE, AxisLocation.CENTER), mesh),
                scalar_zeros(Location(AxisLocation.CENTER, AxisLocation.FACE), mesh)
            )
        }


class FluxTerm(Term):
    def _compute_flux(self, state: State, thermo: Thermodynamics) -> Flux: ...

    def compute(self, state: State, thermo: Thermodynamics) -> ConservativeState:
        _flux = self._compute_flux(state, thermo)
        _tmp = ConservativeState(self.mesh)

        _tmp.density.copy_(divergence_vector(_flux.density, self.mesh))
        _tmp.momentum.copy_(divergence_matrix(_flux.momentum, self.mesh))
        for key in _flux.tracers.keys():
            _tmp.tracers[key].copy_(divergence_vector(_flux.tracers[key], self.mesh))

        return _tmp


class AdvectionTerm(FluxTerm):
    def _compute_flux(self, state: State, thermo: Thermodynamics) -> Flux:
        _flux = Flux(self.mesh)
        _cons = state.conservative
        _prim = state.primitive

        _flux.density.copy_(_cons.momentum).mul_(-1.0)

        _flux.momentum.copy_(
            Matrix(
                Vector(
                    self.schemes.interpolator.apply(_cons.momentum.x, Direction.X)
                    * self.schemes.reconstructor.velocity.apply(_prim.velocity.x, _prim.velocity.x, Direction.X),
                    self.schemes.interpolator.apply(_cons.momentum.y, Direction.X)
                    * self.schemes.reconstructor.velocity.apply(_prim.velocity.x, _prim.velocity.y, Direction.Y)
                ),
                Vector(
                    self.schemes.interpolator.apply(_cons.momentum.x, Direction.Y)
                    * self.schemes.reconstructor.velocity.apply(_prim.velocity.y, _prim.velocity.x, Direction.X),
                    self.schemes.interpolator.apply(_cons.momentum.y, Direction.Y)
                    * self.schemes.reconstructor.velocity.apply(_prim.velocity.y, _prim.velocity.y, Direction.Y)
                )
            )
        ).mul_(-1.0)

        for key in _flux.tracers.keys():
            _flux.tracers[key].copy_(
                Vector(
                    self.schemes.reconstructor.scalar.apply(_prim.tracers[key], _prim.velocity.x, Direction.X)
                    * _cons.momentum.x,
                    self.schemes.reconstructor.scalar.apply(_prim.tracers[key], _prim.velocity.y, Direction.Y)
                    * _cons.momentum.y
                )
            ).mul_(-1.0)

        return _flux
