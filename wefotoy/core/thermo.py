from __future__ import annotations

from . import constant


class Thermodynamics:
    properties: dict[str, float]

    def __init__(self) -> None:
        self.properties = {
            'specific_gas_constant': constant.DRY_AIR_SPECIFIC_GAS_CONSTANT,
            'specific_heat_pressure': constant.DRY_AIR_SPECIFIC_HEAT_PRESSURE,
            'specific_heat_ratio': constant.DRY_AIR_SPECIFIC_HEAT_RATIO
        }
