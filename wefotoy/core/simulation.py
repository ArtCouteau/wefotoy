from __future__ import annotations

from .defs import Direction
from .equation import Equation
from .io import write_tensor
from .mesh import Mesh
from .scheme.scheme import NumericalSchemes


class Simulation():
    equation: Equation
    mesh: Mesh
    schemes: NumericalSchemes
    step: int
    time: float

    def __init__(self, mesh: Mesh) -> None:
        self.mesh = mesh
        self.schemes = NumericalSchemes()
        self.equation = Equation(mesh, self.schemes)
        self.step = 0
        self.time = 0.0

    def _synchronize(self) -> None:
        self.equation.apply_conservative_boundary_conditions(self.mesh)
        self.equation.update_primitive_variables()
        self.equation.apply_primitive_boundary_conditions(self.mesh)

    def run(self, t_end: float, output_path: str | None = None, output_every: int = 1) -> None:
        self._synchronize()
        if output_path is not None:
            self.write_output(output_path)

        while self.time < t_end:
            self.schemes.integrator.advance(self.mesh, self.equation)
            self._synchronize()

            self.time += self.schemes.integrator.dt
            self.step += 1
            if output_path is not None and self.step % output_every == 0:
                self.write_output(output_path)

    def write_output(self, path: str) -> None:
        conservative = self.equation.state.conservative
        primitive = self.equation.state.primitive
        prefix = f'step_{self.step:06d}'
        write_tensor(path, f'{prefix}/density', conservative.density.data)
        write_tensor(path, f'{prefix}/pressure', primitive.pressure.data)
        for direction in Direction:
            write_tensor(path, f'{prefix}/momentum/{direction.name}', conservative.momentum[direction].data)
            write_tensor(path, f'{prefix}/velocity/{direction.name}', primitive.velocity[direction].data)
        for key, tracer in primitive.tracers.items():
            write_tensor(path, f'{prefix}/tracers/{key}', tracer.data)
