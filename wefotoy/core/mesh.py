from __future__ import annotations

from .defs import AxisLocation, Side


class Mesh:
    N: int = 20
    NGhost: int = 1
    L: float = 1.0
    dx: float
    dy: float
    adjacent: dict[Side, slice]
    boundary: dict[AxisLocation, dict[Side, slice]]
    interior: dict[AxisLocation, slice]

    def __init__(self) -> None:
        self.dx = self.dy = self.L/self.N
        self.adjacent = {
            Side.LOWER: slice(0, 1),
            Side.UPPER: slice(-1, None)
        }
        self.boundary = {
            AxisLocation.CENTER: {
                Side.LOWER: slice(0, self.NGhost),
                Side.UPPER: slice(-self.NGhost, None)
            },
            AxisLocation.FACE: {
                Side.LOWER: slice(0, 1),
                Side.UPPER: slice(-1, None)
            },
        }
        self.interior = {
            AxisLocation.CENTER: slice(self.NGhost, -self.NGhost),
            AxisLocation.FACE: slice(1, -1)
        }
