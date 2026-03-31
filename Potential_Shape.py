

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import *
from matplotlib.pyplot import cm
from pylab import *
import array as arr
np.set_printoptions(precision=3)
np.set_printoptions(suppress=True)
from numpy import linalg as LA
h_bar=0.5
w = 2*np.pi #fixed for now; we will step through it to make the plot later
a= (np.pi)/6 #alpha
#numerical code to demonstrate the effect of a modified potential on energy structure for an LC oscillator vs. one w/Josephson Junction
#We will create two different quantized Hamiltonians, H_L and H_J, expressed as matrices, solve the matrices as eigenvalues using linalg functions,
#and plot them against their potential component.
n = 3
H_L=np.zeros((n,n),dtype=float)
H_J=np.zeros((n,n),dtype=float)

for i in arange(0,n):
    for j in arange(0,n):
        if(i==j):
            H_L[i][j]= h_bar*w*(i+0.5)
            
H_J[0][0]= h_bar*w*0.5
H_J[1][1]=h_bar*w + h_bar*w*0.5
H_J[2][2] = (2*h_bar*w+(1.5)*np.sqrt(2)*a)+h_bar*w*0.5
#print(H_L) 
E_L,vecs=LA.eig(H_L)
E_J,vecs=LA.eig(H_J)
#u=np.zeros((Es,N+1),dtype=float) #Wavefunction mesh
#loading spatial mesh
#print(E_L)
#print(E_J)
#plt.xlabel('X')
#plt.ylabel ('$ψ^2$')
# specifying horizontal line type
phs = np.arange(-np.pi,np.pi,0.01)
pot = phs**2
# ----- Plotting both in the same figure -----

fig, axs = plt.subplots(1, 2, figsize=(13,5))

# --- Quantum Harmonic Oscillator ---
phs = np.arange(-np.pi, np.pi, 0.01)
pot = phs**2
trans=0.3
axs[0].plot(phs, pot, color='b',alpha=trans)
axs[0].axhline(y=E_L[0], color='b', linestyle='-')
axs[0].axhline(y=E_L[1], color='b', linestyle='-')
axs[0].axhline(y=E_L[2], color='r', linestyle='-')

axs[0].set_title('Quantum Harmonic Oscillator')
axs[0].set_xlabel('$ϕ$')
axs[0].set_ylabel('Energy')


# --- Transmon ---
pot = -5*np.cos(phs) + 5

axs[1].plot(phs, pot, color='b',alpha=trans)
axs[1].axhline(y=E_J[0], color='b', linestyle='-')
axs[1].axhline(y=E_J[1], color='b', linestyle='-')
axs[1].axhline(y=E_J[2], color='r', linestyle='-')
axs[1].set_title('Josephson Junction')
axs[1].set_xlabel('$ϕ$')
axs[1].set_ylabel('Energy')

plt.tight_layout()
plt.show()

