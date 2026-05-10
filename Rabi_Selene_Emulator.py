#Implementing a Rabi plot using Guppy

import numpy as np
import matplotlib.pyplot as plt
from guppylang import guppy
from guppylang.std.builtins import result, comptime
from guppylang.std.quantum import qubit, measure, rx, ry
from guppylang.std.angles import angle

#gate angles
thetas = np.linspace(0, np.pi, 50)
#dimensionless detuning values
deltas = np.linspace(-1.5, 1.5, 50)
shots_per_point = 100
populations = np.zeros((len(deltas), len(thetas)))
for i, delta in enumerate(deltas):
    for j, theta_val in enumerate(thetas):
        #calculating effective Rabi frequency based on detuning
        omega_eff = np.sqrt(1.0 + delta**2)
        phi = theta_val * omega_eff
        beta = np.arctan(delta)
        #building a new Guppy kernel each time, as these are not reusable. 
        @guppy
        def experiment() -> None:
            #initializing a qubit in |0>
            q = qubit()
            #gate operations implementing detuning.
            ry(q, angle(comptime(-beta)))
            rx(q, angle(comptime(phi)))
            ry(q, angle(comptime(beta)))
            #measuring it
            outcome = measure(q)
            result("Excited", outcome)
        #typechecking
        experiment.check()
        #taking the circuit defined by experiment and runs it on a classical emulator for the specified number of shots, returns a result for each configuration.
        shots = (
            experiment
            .emulator(n_qubits=1)
            .with_shots(shots_per_point)
            .run()
        )
        #adding up the number of measured excited states.
        excited_count = sum(
            1 for shot in shots
            if shot.as_dict().get("Excited", False)
        )
        #ratio of successfully excited qubits to number of shots, yielding a plottable color gradient
        pop = excited_count / shots_per_point
        populations[i, j] = pop
#standard python plotting, producing a heatmap
plt.figure(figsize=(9, 6))
plt.pcolormesh(thetas, deltas, populations, shading='auto', cmap='viridis')
plt.colorbar(label='Excited-State Population P(|1⟩)')
plt.xlabel("Simulated pulse length")
plt.ylabel("Detuning")
plt.title("Rabi Chevron Plot Utilizing Classical Emulator")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
