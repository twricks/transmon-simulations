#Program to visualize the effects of detuning, coupling
import numpy as np
import matplotlib.pyplot as plt

Deltas = np.linspace(-5, 5, 400)
gs = np.linspace(0, 0.5, 300)
hjc = np.zeros((2,2),dtype=float)

C = np.zeros((len(Deltas), len(gs)))
grndstate = np.zeros((len(Deltas), len(gs)))

for i, Delta in enumerate(Deltas):
    for j, g in enumerate(gs):
        hjc[0][0]=Delta/2
        hjc[1][1]=-Delta/2
        hjc[0][1]=g
        hjc[1][0]=g
        evals,evecs = np.linalg.eigh(hjc)
        state = evecs[:,0] #obtaining the first eigenstate
        p_atom = np.abs(state[0])**2 ##obtaining state coefficients
        p_photon = 1-p_atom
        C[i,j] = 2*np.sqrt(p_atom*p_photon) #calculating the concurrence
        grndstate[i,j] = evals[1]-evals[0]
plt.imshow(C.T, cmap='bwr', extent=[Deltas[0], Deltas[-1], gs[0],gs[-1]], origin='lower', aspect='auto')       # color map

plt.colorbar(label='Concurrence.')
plt.xlabel('Detuning δ ')
plt.ylabel('Coupling $\it{g}$')
plt.title('Atom-photon Cavity Entanglement (N=1).')
plt.show()
plt.imshow(grndstate.T, cmap='magma', extent=[Deltas[0], Deltas[-1], gs[0],gs[-1]], origin='lower', aspect='auto')       # color map

plt.colorbar(label='Energy')
plt.xlabel('Detuning δ ')
plt.ylabel('Coupling $\it{g}$')
plt.title('Eigenvalue 1.')
plt.show()
