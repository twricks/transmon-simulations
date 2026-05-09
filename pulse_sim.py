import numpy as np
import matplotlib.pyplot as plt

from guppylang import guppy
from guppylang.std.builtins import result
from guppylang.std.quantum import qubit, measure, rx


@guppy
def experiment(theta) -> None:
    q = qubit()
    rx(q, theta)
    outcome = measure(q)
    result("Excited", outcome)


thetas = np.linspace(0, 2*np.pi, 100)
shots_per_point = 20

populations = []

emulator = experiment.emulator(n_qubits=1)

for theta in thetas:

    shots = (
        emulator
        .with_shots(shots_per_point)
        .run(theta=theta)
    )

    excited_count = sum(
        1 for shot in shots
        if shot.as_dict().get("Excited", False)
    )

    pop = excited_count / shots_per_point
    populations.append(pop)

    print(f"angle = {theta:.3f} -> population = {pop:.3f}")


plt.figure(figsize=(8,5))
plt.plot(thetas, populations, 'o-')
plt.xlabel("Rotation Angle (rad)")
plt.ylabel("Excited-State Population")
plt.title("Rabi Oscillations")
plt.grid(True)
plt.show()