#code to demonstrate homodyne IQ mixing for qubit state discrimination
import numpy as np
import array as arr
import random
import matplotlib.pyplot as plt 

t = 200 #time steps; really number of samples per shot
shots = 500 #number of measurements/ demodulations
sig_array = np.zeros((t), dtype=float) #array to store signal values
I_array = np.zeros((t), dtype=float) 
Q_array= np.zeros((t), dtype=float)
example_sig_1 = np.zeros((t), dtype=float)
example_sig_2 = np.zeros((t), dtype=float)
phi_array = np.zeros((2),dtype=float) 
phi1 = np.random.uniform(-np.pi, np.pi) # generating a random signal phase
phi2 = (np.pi/3)+ phi1 #preset phase difference from the first randomly generated one. 
phi_array[:] = [phi1, phi2] if abs(phi1) <= abs(phi2) else [phi2, phi1] #we assign the phase closer to zero to be the ground state
carrier_omega = 2*np.pi *0.15 
I_vals = np.zeros((shots),dtype=float)
Q_vals = np.zeros((shots),dtype=float)
phases = np.zeros((shots), dtype=int) #stores which choice of random phase was actually present for each shot
example_taken=[False,False] #boolean array to track whether we're taken an example shot for each phase


for k in range(0,shots):
    phase_choice = np.random.choice([0, 1]) #random choice of phase per shot
    phases[k] = phase_choice #storing which phase was used for plotting
    phi = phi_array[phase_choice]
    for q in range(0,t):
        amp = 1.0 #np.random.normal(loc=1.0, scale=0.05)#some normally distributed variation in amplitude
        noise = 0.6 * np.random.normal() #generate a gaussian-distributed random noise at each time step
        sig_array[q]=amp*np.cos(carrier_omega*q+phi) + noise #load the signal into an array
        I_array[q] = np.cos(carrier_omega*q)*sig_array[q] #perform the multiplications
        Q_array[q] = -np.sin(carrier_omega*q)*sig_array[q]
    I = np.mean(I_array) #time averaging
    Q = np.mean(Q_array)
    I_vals[k]=I
    Q_vals[k]=Q
    if not example_taken[phase_choice]:
        if phase_choice == 0:
            example_sig_1[:] = sig_array  # copy an example for the ground state phase
        else:
            example_sig_2[:] = sig_array  # copy an example for the excited state phase
        example_taken[phase_choice] = True



rec_amp = 2*np.sqrt(I**2+Q**2)
rec_phi = np.arctan2(Q,I) #testing that I-Q demodulation is working correctly by checking the recovered waveform
#print(rec_amp)
phase_colors = ['red' if p==0 else 'blue' for p in phases] #creating a list to color code shot results by phase

plt.figure(figsize=(10,4))
plt.gcf().canvas.manager.set_window_title("3.2: Homodyne I-Q Demodulation")
plt.subplot(1,2,1)
plt.plot(example_sig_1[:30],color='red', label=r"$|0\rangle$")
plt.plot(example_sig_2[:30], color = 'blue', label=r"$|1\rangle$")
plt.xlabel("Time (sample steps).")
plt.ylabel("Amplitude (arbitrary units).")
plt.title("Example Phase-offset Signals")
plt.legend()
plt.grid(True)

# plot the I-Q scatter
plt.subplot(1,2,2)
plt.scatter(I_vals, Q_vals, c=phase_colors, alpha=0.4)
plt.xlabel("I (in-phase component).")
plt.ylabel("Q (quadrature component).")
plt.title("Signal Demodulation in I-Q Plane")
plt.axis('equal')
plt.grid(True)

plt.tight_layout()
plt.show()

#max_val = max(np.max(np.abs(I_vals)), np.max(np.abs(Q_vals))) * 1.1 #scatter plot is 10% bigger than the biggest values
#plt.xlim(-max_val, max_val)
#plt.ylim(-max_val, max_val)
plt.show()