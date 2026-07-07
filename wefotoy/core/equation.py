from __future__ import annotations

from .field import Location, Scalar, Vector, Matrix, zeros
from .interpolation import interp_x, interp_y
from . import constant


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


class NavierStokesPrimitiveVariable:
    velocity: Vector
    pressure: Scalar

    def __init__(self) -> None:
        self.velocity = Vector(
            zeros((Location['FACE'], Location['CENTER'])),
            zeros((Location['CENTER'], Location['FACE']))
        )
        self.pressure = zeros((Location['CENTER'], Location['CENTER']))


class NavierStokesProperty:
    specificGasConstant: float
    specificHeatPressure: float
    specificHeatRatio: float

    def __init__(self) -> None:
        self.specificGasConstant = constant.DRY_AIR_SPECIFIC_GAS_CONSTANT
        self.specificHeatPressure = constant.DRY_AIR_SPECIFIC_HEAT_PRESSURE
        self.specificHeatRatio = constant.DRY_AIR_SPECIFIC_HEAT_RATIO


class NavierStokesFlux:
    density: Vector
    momentum: Matrix
    potentialTemperatureDensity: Vector


class NavierStokesAdvectiveFlux:
    equation: NavierStokesEquation

    def compute(self) -> NavierStokesFlux:
        _flux = NavierStokesFlux()

        _flux.density = Vector(
            interp_x(self.equation.variable.conserved.density) * self.equation.variable.primitive.velocity.x,
            interp_y(self.equation.variable.conserved.density) * self.equation.variable.primitive.velocity.y
        )

        _densityCorner = interp_x(interp_y(self.equation.variable.conserved.density))
        _velocityCenter = Vector(
            interp_x(self.equation.variable.primitive.velocity.x),
            interp_y(self.equation.variable.primitive.velocity.y)
        )
        _velocityCorner = Vector(
            interp_y(self.equation.variable.primitive.velocity.x),
            interp_x(self.equation.variable.primitive.velocity.y)
        )
        _fluxMomentumXX = self.equation.variable.conserved.density * _velocityCenter.x.pow_(2)
        _fluxMomentumXY = _densityCorner * _velocityCorner.x * _velocityCorner.y
        _fluxMomentumYY = self.equation.variable.conserved.density * _velocityCenter.y.pow_(2)
        _flux.momentum = Matrix(Vector(_fluxMomentumXX, _fluxMomentumXY), Vector(_fluxMomentumXY, _fluxMomentumYY))

        _flux.potentialTemperatureDensity = Vector(
            (
                interp_x(self.equation.variable.conserved.potentialTemperatureDensity)
                * self.equation.variable.primitive.velocity.x
            ),
            (
                interp_y(self.equation.variable.conserved.potentialTemperatureDensity)
                * self.equation.variable.primitive.velocity.y
            )
        )

        return _flux


class NavierStokesEquation:
    property: NavierStokesProperty
    variable: NavierStokesVariable

    def __init__(self) -> None:
        super().__init__()
        self.variable = NavierStokesVariable()

    def _conserved_to_primitive(self) -> None:
        self.variable.primitive.velocity.x.copy_(
            self.variable.conserved.momentum.x/interp_x(self.variable.conserved.density)
        )
        self.variable.primitive.velocity.y.copy_(
            self.variable.conserved.momentum.x/interp_y(self.variable.conserved.density)
        )
        self.variable.primitive.pressure.copy_(
            constant.REFERENCE_PRESSURE
            * (
                self.property.specificGasConstant
                * self.variable.conserved.potentialTemperatureDensity
                / constant.REFERENCE_PRESSURE
            ).pow_(self.property.specificHeatRatio)
        )

    def rhs(self) -> None:
        # 1. Convert conserved to primitives
        self._conserved_to_primitive()
