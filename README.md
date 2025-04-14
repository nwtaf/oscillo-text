# Oscillo Text
Converts text to oscilloscope visuals using audio waveforms. Includes text-to-WAV script, setup instructions, and a circle test pattern.

## Table of Contents

## Requirements


## Installation
- Use UV package manager
- `git clone https://github.com/nwtaf/OscilloText.git`

## Use
- Within `src\oscillo_text` there are two files, 'circle.py' and 'oscillotext.py'. Run circle.py first, to test the physical configuration. The oscilloscope should display a perfect circle.
- Run 'oscillotext.py' when the configuration has been tested to print some text to the oscilloscope.

## Required Oscilloscope Settings
- XY Mode

### Recomended Oscilloscope Settings
- Bandwidth Limit (BW): 20M
- Volts/Div: Coarse

### What Worked for Me
- Volume was at about 70%. 
- x-axis scale was set to 200mV
- y-axis scale was set to 2V

## Troubleshooting
- The visualization only works with good x and y scale settings. If there are too many letters or the volume is too high or low, the visualization will fail and it will look like a cloud of dots. It is important to tweak the input volume and the x and y scale.
- Also important is to confirm that stereo output is enabled in your machine's settings. If not enabled, the circle test script will look like a moving cloud, akin to a positive linear function (sweeps up and down diagnally). 

## Disclaimer
This was vibe-coded and took about two hours. This project does not reflect best practices or my best work. I was only able to get two letters to show properly at one time, more was too fast for my configuration. This repo serves as a good platform to continue development with.