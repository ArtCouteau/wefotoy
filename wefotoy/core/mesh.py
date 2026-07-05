from __future__ import annotations


class Mesh:
    N: int = 20
    NGhost: int = 1
    L: float = 1.0
    dx: float
    dy: float

    def __init__(self) -> None:
        self.dx = self.dy = self.L/self.N


mesh = Mesh
