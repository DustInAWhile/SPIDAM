import numpy as np
import matplotlib.pyplot as plt

def plot_sine_wave(frequency=2, amplitude=1, duration=1, sample_rate=1000):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    y = amplitude * np.sin(2 * np.pi * frequency * t)
    plt.figure(figsize=(10, 4))
    plt.plot(t, y, label=f'{frequency} Hz, Amplitude {amplitude}')
    plt.title("Sine Wave")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.legend()
    plt.show()
