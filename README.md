# AWGN vs Rayleigh Fading with different modulations.

## Usage

### Plots
Can be found in `generated_plots`

### For real time comparisson between channels and modulation types
`python gui.py`

#### Little introduction

AWGN (Additive White Gaussian Noise) and Rayleigh fading are two common channel models used in wireless communication systems.

AWGN is a simple and widely used channel model that assumes the presence of random noise in the communication channel. It is characterized by noise that is additive, white (uniformly distributed across all frequencies), and Gaussian (follows a normal distribution). AWGN is often used to model the effects of interference, thermal noise, and other sources of random disturbances in wireless communication.

Rayleigh fading, on the other hand, is a more complex channel model that takes into account the multipath propagation of radio waves. It assumes that the received signal is a combination of multiple delayed and attenuated versions of the transmitted signal, due to reflections, diffractions, and scattering in the environment. Rayleigh fading is characterized by a Rayleigh distribution of the received signal strength, which means that the amplitude of the received signal follows a Rayleigh distribution.

All of this information was written by GitHub Copilot, so let me know if you read this part of the text. My gut tells me no one will ever bother reading through this. Was a fun project to implement though.

In practical wireless communication systems, both AWGN and Rayleigh fading can coexist. The presence of AWGN can degrade the signal quality by introducing random noise, while Rayleigh fading can cause signal fading and fluctuations in the received signal strength.

To simulate and analyze the performance of wireless communication systems, it is common to use mathematical models and simulations that incorporate both AWGN and Rayleigh fading. These models help in understanding the impact of noise and fading on system performance and in designing robust communication schemes to mitigate their effects.