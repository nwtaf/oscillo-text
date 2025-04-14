import numpy as np
from scipy.io.wavfile import write
import sounddevice as sd

# Parameters
sample_rate = 44100  # Maximum typical audio rate
duration = 5  # Shorter duration for faster refresh
text = "NT"  # Simple Text (Hello World)

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

# Use matplotlib to get character paths
from matplotlib.textpath import TextPath

def text_to_path(text, scale=1.0):
    path = TextPath((0, 0), text, size=1)
    vertices = np.array(path.vertices).copy()  # Create a writable copy of vertices
    codes = path.codes

    # Normalize and scale
    vertices -= vertices.min(axis=0)
    vertices /= vertices.max()
    vertices *= 2
    vertices -= 1
    vertices *= scale

    return vertices, codes

# Generate waveform
vertices, codes = text_to_path(text, scale=0.8)

# Interpolate to desired length
from scipy.interpolate import interp1d

# Calculate how many times to repeat the pattern for similar speed to circlv2.py
repetitions = 100  # Similar to the frequency in circlv2.py

t = np.linspace(0, 1, len(vertices))
interp_x = interp1d(t, vertices[:, 0], kind='linear')
interp_y = interp1d(t, vertices[:, 1], kind='linear')

# Create a longer signal with multiple repetitions
t_new = np.linspace(0, 1, int(sample_rate * duration / repetitions))
x_single = interp_x(t_new)
y_single = interp_y(t_new)

# Normalize the single pattern
x_single = x_single / np.max(np.abs(x_single))
y_single = y_single / np.max(np.abs(y_single))

# Repeat the pattern
x = np.tile(x_single, repetitions)
y = np.tile(y_single, repetitions)

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
write(r'OscilloText\visuals\visualize_text.wav', sample_rate, audio_data)
print("WAV file saved as 'OscilloText\visuals\visualize_text.wav'")

# Play the waveform in an infinite loop
try:
    print("Playing in infinite loop. Press Ctrl+C to stop...")
    while True:
        sd.play(audio_data, sample_rate)
        sd.wait()  # Wait until the audio is finished playing
except KeyboardInterrupt:
    sd.stop()
    print("\nPlayback stopped.")