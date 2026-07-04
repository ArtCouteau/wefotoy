from __future__ import annotations

import torch
from typing import Literal

from . import flux

INFO = {
    'N_X': 20,
    'N_Y': 20
}


class Grid:
    cells: Cells

    def __init__(self):
        self.cells = Cells()


class Cells:
    centers: Centers
    faces: dict[str, Faces]

    def __init__(self):
        self.centers = Centers(self)
        self.faces = {face: Faces(self) for face in ['x-', 'x+', 'y-', 'y+']}


class Centers:
    cells: Cells
    variables: dict[str, torch.Tensor]

    def __init__(self, cells: Cells):
        self.cells = cells
        self.variables = {
            'velocity': torch.zeros(2, INFO['N_X'], INFO['N_Y'])
        }


class Faces:
    cells: Cells
    fluxes: dict[str, flux.Flux]
    variables: dict[str, torch.Tensor]

    def __init__(self, cells: Cells):
        self.cells = cells
        self.variables = {
            'density': torch.zeros(INFO['N_X'], INFO['N_Y'])
        }

    def compute_fluxes(self) -> torch.Tensor | Literal[0]:
        return sum(flux.compute() for flux in self.fluxes.values())
