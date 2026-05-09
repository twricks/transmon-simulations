import numpy as np
import matplotlib.pyplot as plt

from guppylang import guppy
from guppylang.std.builtins import result, comptime
from guppylang.std.quantum import qubit, measure, rx
from guppylang.std.angles import angle

thetas = np.linspace(0, 2*np.pi, 100)
shots_per_point = 20

populations = []

for theta in thetas:
    @guppy
    def experiment() -> None:
        q = qubit()
        q = rx(q,angle((comptime(theta))))
        outcome = measure(q)
        result("Excited",outcome)
    
    experiment.check()

    shots = (experiment.emulator(n_qubits=1).with_shots(shots_per_point).run())

    excited_count = sum(
        1 for shot in shots
        if shot.as_dict().get("excited",False)
    )

    pop = excited_count / shots_per_point
    populations.append(pop)

    #print()

plt.figure(figsize=(8,5))
plt.plot(thetas, populations, 'o-')
plt.xlabel("Rotation Angle (rad)")
plt.ylabel("Excited-State Population")
plt.title("Rabi Oscillations")
plt.grid(True)
plt.show()
