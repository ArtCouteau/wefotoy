from __future__ import annotations

import enum


class Direction(enum.Enum):
    X = 0
    Y = 1


class Location(enum.Enum):
    CENTER = 0
    FACE_X = 1
    FACE_Y = 2
    CORNER = 3
