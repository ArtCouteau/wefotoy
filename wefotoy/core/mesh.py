from __future__ import annotations

import torch


class Grid:
    cells: Cells

    def __init__(self):
        super().__init__()


class Cells:
    centers: Centers
    faces: Faces

    def __init__(self):
        super().__init__()


class Centers:
    variables: dict[str, torch.Tensor]

    def __init__(self):
        super().__init__()


class Faces:
    variables: dict[str, torch.Tensor]

    def __init__(self):
        super().__init__()
