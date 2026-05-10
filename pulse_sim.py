import numpy as np
import matplotlib.pyplot as plt
from guppylang import guppy
from guppylang.std.builtins import result, comptime
from guppylang.std.quantum import qubit, measure, rx, ry
from guppylang.std.angles import angle
thetas = np.linspace(0, 4 * np.pi, 50)
deltas = np.linspace(-5.0, 5.0, 50)
shots_per_point = 200
populations = np.zeros((len(deltas), len(thetas)))
for i, delta in enumerate(deltas):
    for j, theta_val in enumerate(thetas):
        omega_eff = np.sqrt(1.0 + delta**2)
        phi = theta_val * omega_eff
        beta = np.arctan(delta)
        @guppy
        def experiment() -> None:
            q = qubit()
            ry(q, angle(comptime(-beta)))
            rx(q, angle(comptime(phi)))
            ry(q, angle(comptime(beta)))
            outcome = measure(q)
            result("Excited", outcome)
        experiment.check()
        shots = (
            experiment
            .emulator(n_qubits=1)
            .with_shots(shots_per_point)
            .run()
        )
        excited_count = sum(
            1 for shot in shots
            if shot.as_dict().get("Excited", False)
        )
        pop = excited_count / shots_per_point
        populations[i, j] = pop
plt.figure(figsize=(9, 6))
plt.pcolormesh(thetas, deltas, populations, shading='auto', cmap='viridis')
plt.colorbar(label='Excited-State Population P(|1⟩)')
plt.xlabel("On-resonance rotation angle θ = Ωt (rad) — proportional to pulse length")
plt.ylabel("Detuning δ = Δ/Ω")
plt.title("Rabi Chevron Plot\n(sweep over pulse length + detuning)")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
