from __future__ import annotations

from .field import Direction, Location, Scalar, Vector, zeros
from . import constant, interpolation, reconstruction, term


class NavierStokesVariable:
    conserved: NavierStokesConservedVariable
    primitive: NavierStokesPrimitiveVariable


class NavierStokesConservedVariable:
    density: Scalar
    momentum: Vector
    potentialTemperatureDensity: Scalar

    def __init__(self) -> None:
        self.density = zeros((Location.CENTER, Location.CENTER))
        self.momentum = Vector(
            zeros((Location['FACE'], Location['CENTER'])),
            zeros((Location['CENTER'], Location['FACE']))
        )
        self.potentialTemperatureDensity = zeros((Location['CENTER'], Location['CENTER']))

    def add_(self, other: term.NavierStokesRHS):
        self.density.add_(other.density)
        self.momentum.x.add_(other.momentum.x)
        self.momentum.y.add_(other.momentum.y)
        self.potentialTemperatureDensity.add_(other.potentialTemperatureDensity)


class NavierStokesPrimitiveVariable:
    velocity: Vector
    potentialTemperature: Scalar
    pressure: Scalar

    def __init__(self) -> None:
        self.velocity = Vector(
            zeros((Location['FACE'], Location['CENTER'])),
            zeros((Location['CENTER'], Location['FACE']))
        )
        self.potentialTemperature = zeros((Location['CENTER'], Location['CENTER']))
        self.pressure = zeros((Location['CENTER'], Location['CENTER']))


class NavierStokesProperty:
    specificGasConstant: float
    specificHeatPressure: float
    specificHeatRatio: float

    def __init__(self) -> None:
        self.specificGasConstant = constant.DRY_AIR_SPECIFIC_GAS_CONSTANT
        self.specificHeatPressure = constant.DRY_AIR_SPECIFIC_HEAT_PRESSURE
        self.specificHeatRatio = constant.DRY_AIR_SPECIFIC_HEAT_RATIO


class NavierStokesReconstructorScheme:
    scalar: reconstruction.Reconstructor
    velocity: reconstruction.Reconstructor


class NavierStokesEquation:
    property: NavierStokesProperty
    variable: NavierStokesVariable
    reconstructor: NavierStokesReconstructorScheme
    terms: list[term.NavierStokesTerm]

    def __init__(self) -> None:
        super().__init__()
        self.variable = NavierStokesVariable()
        self.property = NavierStokesProperty()
        self.reconstructor = NavierStokesReconstructorScheme()
        self.terms = [
            term.NavierStokesAdvectionTerm(self),
            term.NavierStokesPressureTerm(self)
        ]

    def _conserved_to_primitive(self) -> None:
        self.variable.primitive.velocity.x.copy_(
            self.variable.conserved.momentum.x/interpolation.linear(self.variable.conserved.density, Direction.X)
        )
        self.variable.primitive.velocity.y.copy_(
            self.variable.conserved.momentum.x/interpolation.linear(self.variable.conserved.density, Direction.Y)
        )
        self.variable.primitive.potentialTemperature.copy_(
            self.variable.conserved.potentialTemperatureDensity/self.variable.conserved.density
        )
        self.variable.primitive.pressure.copy_(
            constant.REFERENCE_PRESSURE
            * (
                self.property.specificGasConstant
                * self.variable.conserved.potentialTemperatureDensity
                / constant.REFERENCE_PRESSURE
            ).pow_(self.property.specificHeatRatio)
        )

    def rhs(self) -> term.NavierStokesRHS:
        # 1. Convert conserved to primitives
        self._conserved_to_primitive()

        # 2. Compute rhs
        _rhs = term.NavierStokesRHS()
        for _term in self.terms:
            _rhs.add_(_term.compute())

        return _rhs
