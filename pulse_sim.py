import numpy as np
import matplotlib.pyplot as plt

from guppylang import guppy
from guppylang.std.builtins import result, comptime
from guppylang.std.quantum import qubit, measure, rx, ry
from guppylang.std.angles import angle

# ====================== Sweep parameters ======================
thetas = np.linspace(0, 4 * np.pi, 60)      # pulse length proxy (Ωt)
deltas = np.linspace(-2.0, 2.0, 25)         # detuning δ = Δ/Ω  (feel free to shrink for speed)
shots_per_point = 200                       # start low while testing; increase later for smoother data

populations = np.zeros((len(deltas), len(thetas)))

print("Starting 2D sweep (θ × δ) — this will take a couple of minutes...")

for i, delta in enumerate(deltas):
    for j, theta_val in enumerate(thetas):
        # Exact detuned Rabi parameters (classical pre-computation)
        omega_eff = np.sqrt(1.0 + delta**2)
        phi = theta_val * omega_eff
        beta = np.arctan(delta)

        # Fresh Guppy kernel for this exact (θ, δ) pair
        @guppy
        def experiment() -> None:
            q = qubit()
            # Exact decomposition of the detuned drive unitary:
            #   Ry(−β) Rx(φ) Ry(+β)
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

        # Progress indicator
        if j % 15 == 0:
            print(f"  δ = {delta:+.2f} | θ = {theta_val:.2f} → P(|1⟩) = {pop:.3f}")

# ====================== 2D Chevron Plot ======================
plt.figure(figsize=(9, 6))
plt.pcolormesh(thetas, deltas, populations, shading='auto', cmap='viridis')
plt.colorbar(label='Excited-State Population P(|1⟩)')
plt.xlabel("On-resonance rotation angle θ = Ωt (rad) — proportional to pulse length")
plt.ylabel("Detuning δ = Δ/Ω")
plt.title("Rabi Chevron Plot\n(sweep over pulse length + detuning)")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
