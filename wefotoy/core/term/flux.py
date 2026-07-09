from __future__ import annotations


from .term import Term
from ..defs import Direction, AxisLocation, Location
from ..field import Vector, Matrix
from ..mesh import Mesh
from ..state import State, ConservativeState
from ..thermo import Thermodynamics


class Flux:
    density: Vector
    momentum: Matrix
    tracers: dict[str, Vector]

    def __init__(self, mesh: Mesh) -> None:
        self.density = Vector(
            mesh.zeros(Location(AxisLocation.FACE, AxisLocation.CENTER)),
            mesh.zeros(Location(AxisLocation.CENTER, AxisLocation.FACE))
        )
        self.momentum = Matrix(
            Vector(
                mesh.zeros(Location(AxisLocation.CENTER, AxisLocation.CENTER)),
                mesh.zeros(Location(AxisLocation.CENTER, AxisLocation.FACE))
            ),
            Vector(
                mesh.zeros(Location(AxisLocation.FACE, AxisLocation.CENTER)),
                mesh.zeros(Location(AxisLocation.CENTER, AxisLocation.CENTER))
            )
        )
        self.tracers = {
            'potential_temperature': Vector(
                mesh.zeros(Location(AxisLocation.FACE, AxisLocation.CENTER)),
                mesh.zeros(Location(AxisLocation.CENTER, AxisLocation.FACE))
            )
        }


class FluxTerm(Term):
    def _compute_flux(self, state: State, thermo: Thermodynamics) -> Flux: ...

    def compute(self, state: State, thermo: Thermodynamics) -> ConservativeState:
        _flux = self._compute_flux(state, thermo)
        _tmp = ConservativeState(self.mesh)

        _tmp.density.copy_(self.mesh.divergence_vector(_flux.density))
        _tmp.momentum.copy_(self.mesh.divergence_matrix(_flux.momentum))
        for key in _flux.tracers.keys():
            _tmp.tracers[key].copy_(self.mesh.divergence_vector(_flux.tracers[key]))

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
