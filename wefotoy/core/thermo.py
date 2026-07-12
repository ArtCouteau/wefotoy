from __future__ import annotations

from . import constant
from .field import Scalar


class Thermodynamics:
    properties: dict[str, float]

    def __init__(self) -> None:
        self.properties = {
            'background_pressure': constant.BACKGROUND_PRESSURE,
            'specific_gas_constant': constant.DRY_AIR_SPECIFIC_GAS_CONSTANT,
            'specific_heat_pressure': constant.DRY_AIR_SPECIFIC_HEAT_PRESSURE,
            'specific_heat_ratio': constant.DRY_AIR_SPECIFIC_HEAT_RATIO
        }

    def Exner_equation_of_state(self, potential_temperature_density: Scalar) -> Scalar:
        return (
            self.properties['background_pressure']
            * (
                self.properties['specific_gas_constant']
                * potential_temperature_density
                / self.properties['background_pressure']
            ).pow_(self.properties['specific_heat_ratio'])
        )

    def speed_of_sound(self, potential_temperature_density: Scalar) -> Scalar:
        return potential_temperature_density.mul_(self.properties['specific_gas_constant']).sqrt_()
