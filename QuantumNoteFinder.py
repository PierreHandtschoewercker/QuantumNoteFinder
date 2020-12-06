try:
    import pyaudio
    import numpy as np
    import pylab
    import matplotlib.pyplot as plt
    from scipy.io import wavfile
    import time
    import sys
    import seaborn as sns
    import aubio
except:
    print("Something didn't import")

"""i=0
f,ax = plt.subplots(2)

# Prepare the Plotting Environment with random starting values
x = np.arange(10000)
y = np.random.randn(10000)

# Plot 0 is for raw audio data
li, = ax[0].plot(x, y)
ax[0].set_xlim(0,1000)
ax[0].set_ylim(-5000,5000)
ax[0].set_title("Raw Audio Signal")
# Plot 1 is for the FFT of the audio
li2, = ax[1].plot(x, y)
ax[1].set_xlim(0,5000)
ax[1].set_ylim(-100,100)
ax[1].set_title("Fast Fourier Transform")
# Show the plot, but without blocking updates
plt.pause(0.01)
plt.tight_layout()"""
win_s = 4096
FORMAT = pyaudio.paFloat32  # We use 16bit format per sample
CHANNELS = 1
SAMPLE_RATE = 44100
BUFFER_SIZE = 2048  # 1024bytes of data red from a buffer


def callback(in_data, frame_count, time_info, status):
    # get and convert the data to float
    audio_data = np.fromstring(in_data, np.int16)
    # Fast Fourier Transform, 10*log10(abs) is to scale it to dB
    # and make sure it's not imaginary
    dfft = 10. * np.log10(abs(np.fft.rfft(audio_data)))

    # Force the new data into the plot, but without redrawing axes.
    # If uses plt.draw(), axes are re-drawn every time
    # print audio_data[0:10]
    # print dfft[0:10]
    # print
    samples = np.fromstring(in_data,
                            dtype=aubio.float_type)
    # Finally get the pitch.
    pitch = pDetection(samples)[0]
    # Compute the energy (volume)
    # of the current frame.
    volume = np.sum(samples ** 2) / len(samples)
    # Format the volume output so it only
    # displays at most six numbers behind 0.
    volume = "{:6f}".format(volume)

    # Finally print the pitch and the volume.
    print(str(pitch) + " " + str(volume))
    return in_data, pyaudio.paContinue


# Show the updated plot, but without blocking
# plt.pause(0.01)

audio = pyaudio.PyAudio()

# start Recording
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=SAMPLE_RATE,
                    input=True,
                    output=True,
                    stream_callback=callback)  # ,
# frames_per_buffer=CHUNK)

pDetection = aubio.pitch("yin", win_s,
                         1024, SAMPLE_RATE)
# Set unit.
pDetection.set_unit("Hz")
# Frequency under -40 dB will considered
# as a silence.
pDetection.set_silence(-40)


# Open the connection and start streaming the data
stream.start_stream()
print("\n+---------------------------------+")
print("| Press Ctrl+C to Break Recording |")
print("+---------------------------------+\n")

# Loop so program doesn't end while the stream callback's
# itself for new data
while stream.is_active():
    time.sleep(0.1)

# Close up shop (currently not used because KeyboardInterrupt
# is the only way to close)
stream.stop_stream()
stream.close()

audio.terminate()
