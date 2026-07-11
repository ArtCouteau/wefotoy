from __future__ import annotations

from .boundary import BoundaryCondition, Periodic
from .defs import Direction, Side
from .mesh import Mesh
from .scheme.scheme import NumericalSchemes
from .state import State, ConservativeState
from .term.term import Term
from .term.flux import AdvectionTerm
from .term.source import PressureTerm
from .thermo import Thermodynamics


class Equation:
    boundary_conditions: BoundaryConditions
    rhs: ConservativeState
    state: State
    terms: list[Term]
    thermo: Thermodynamics

    def __init__(self, mesh: Mesh, schemes: NumericalSchemes) -> None:
        self.boundary_conditions = BoundaryConditions()
        self.rhs = ConservativeState(mesh)
        self.state = State(mesh, schemes)
        self.thermo = Thermodynamics()
        self.terms = [
            AdvectionTerm(mesh, schemes),
            PressureTerm(mesh, schemes)
        ]

    def update_primitive_variables(self) -> None:
        self.state.primitive.update(self.state.conservative, self.thermo)

    def apply_boundary_conditions(self, mesh: Mesh) -> None:
        self.boundary_conditions.apply(self.state, mesh)

    def compute_rhs(self, state: State) -> ConservativeState:
        self.rhs.zero_()
        for term in self.terms:
            self.rhs.add_(term.compute(state, self.thermo))

        return self.rhs


class BoundaryConditions:
    density: list[BoundaryCondition]
    velocity: dict[Direction, list[BoundaryCondition]]
    tracers: dict[str, list[BoundaryCondition]]

    def __init__(self) -> None:
        self.density = [
            Periodic(Direction.X, Side.LOWER),
            Periodic(Direction.X, Side.UPPER),
            Periodic(Direction.Y, Side.LOWER),
            Periodic(Direction.Y, Side.UPPER),
        ]
        self.velocity = {
            direction: [
                Periodic(Direction.X, Side.LOWER),
                Periodic(Direction.X, Side.UPPER),
                Periodic(Direction.Y, Side.LOWER),
                Periodic(Direction.Y, Side.UPPER),
            ] for direction in Direction
        }
        self.tracers = {
            'potential_temperature': [
                Periodic(Direction.X, Side.LOWER),
                Periodic(Direction.X, Side.UPPER),
                Periodic(Direction.Y, Side.LOWER),
                Periodic(Direction.Y, Side.UPPER),
            ]
        }

    def apply(self, state: State, mesh: Mesh):
        for bc in self.density:
            bc.apply(state.conservative.density, mesh)
        for direction in Direction:
            for bc in self.velocity[direction]:
                bc.apply(state.primitive.velocity[direction], mesh)
        for key in self.tracers.keys():
            for bc in self.tracers[key]:
                bc.apply(state.primitive.tracers[key], mesh)
