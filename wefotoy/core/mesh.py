from __future__ import annotations

from .defs import AxisLocation, Side


class Mesh:
    N: int = 20
    NGhost: int = 1
    L: float = 1.0
    dx: float
    dy: float
    interior: dict[AxisLocation, slice]
    boundary: dict[AxisLocation, dict[Side, slice]]

    def __init__(self) -> None:
        self.dx = self.dy = self.L/self.N
        self.interior = {
            AxisLocation.CENTER: slice(self.NGhost, -self.NGhost),
            AxisLocation.FACE: slice(None),
        }
        self.boundary = {
            AxisLocation.CENTER: {
                Side.LOWER: slice(0, self.NGhost),
                Side.UPPER: slice(-self.NGhost, None),
            },
            AxisLocation.FACE: {
                Side.LOWER: slice(0, 1),
                Side.UPPER: slice(-1, None),
            },
        }
