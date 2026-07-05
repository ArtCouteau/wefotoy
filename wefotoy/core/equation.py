from __future__ import annotations

from . import field


class Variable:
    conserved: dict[str, field.Field]
    primitive: dict[str, field.Field]
    reference: dict[str, field.Field]

    def __init__(self):
        self.conserved = {}
        self.primitive = {}
        self.reference = {}


class Equation:
    variable: Variable

    def __init__(self):
        self.variable = Variable()


class NavierStokesEquation(Equation):
    def __init__(self):
        super().__init__()

        loc = field.Location
        self.variable.conserved = {
            'density': field.zeros((loc['CENTER'], loc['CENTER'])),
            'momentum_x': field.zeros((loc['FACE'], loc['CENTER'])),
            'momentum_y': field.zeros((loc['CENTER'], loc['FACE'])),
            'potentialTemperature': field.zeros((loc['CENTER'], loc['CENTER']))
        }
        self.variable.primitive = {
            'velocity_x': field.zeros((loc['FACE'], loc['CENTER'])),
            'velocity_y': field.zeros((loc['CENTER'], loc['FACE'])),
            'pressure': field.zeros((loc['CENTER'], loc['CENTER']))
        }
