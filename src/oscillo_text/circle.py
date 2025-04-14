import numpy as np
from scipy.io.wavfile import write
import sounddevice as sd

# List available audio devices
print("Available audio devices:")
for i, device in enumerate(sd.query_devices()):
    print(f"  {i:2d} {device['name']}, {device['hostapi']} ({device['max_input_channels']} in, {device['max_output_channels']} out)")

# Find your Focusrite output device (ensure it has output channels)
focusrite_name = "Focusrite USB"  # Partial name match should work
focusrite_device = None

for i, device in enumerate(sd.query_devices()):
    if (focusrite_name.lower() in device['name'].lower() and 
            device['max_output_channels'] > 0):
        focusrite_device = i
        print(f"Found Focusrite output device at index {i}: {device['name']}")
        break

if focusrite_device is not None:
    device_info = sd.query_devices(focusrite_device)
    sd.default.device = focusrite_device
    print(f"Using audio device: {device_info['name']}")
    # Check how many output channels this device supports
    output_channels = device_info['max_output_channels']
    print(f"Device supports {output_channels} output channels")
else:
    print("Focusrite output device not found. Using system default.")
    device_info = sd.query_devices(sd.default.device[1])  # Get default output device
    output_channels = device_info['max_output_channels']
    print(f"Default device supports {output_channels} output channels")

fs = 44100
duration = 5  # seconds
frequency = 5000  # Increased from 5 to 100 Hz for faster rotation
t = np.linspace(0, 2 * np.pi * frequency, fs * duration)  #  Hz cycle

x = 0.8 * np.cos(t)
y = 0.8 * np.sin(t)

# Adjust the number of channels based on device capabilities
if output_channels == 1:
    # For mono output, just use one channel
    audio_data = x.reshape(-1, 1).astype(np.float32)
    print("Using mono output")
else:
    # For stereo or more, use both channels
    audio_data = np.vstack((x, y)).T.astype(np.float32)
    print(f"Using stereo output with shape {audio_data.shape}")

# Save to WAV file
write(r'OscilloText\visuals\test_circle.wav', fs, audio_data)

# Play the waveform in an infinite loop
try:
    print("Playing in infinite loop. Press Ctrl+C to stop...")
    while True:
        sd.play(audio_data, fs)
        sd.wait()  # Wait until the audio is finished playing
except KeyboardInterrupt:
    sd.stop()
    print("\nPlayback stopped.")
