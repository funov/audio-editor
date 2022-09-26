import numpy as np
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
import matplotlib


fs, data = wav.read("C:\\Users\\funov\\Desktop\\test\\166351110187705372620876.wav")

if len(data.shape) > 1:
    data = data[..., 0]

overlap_fac = 0.5
fft_size = 2 ** 10

hop_size = np.int32(np.floor(fft_size * (1 - overlap_fac)))
pad_end_size = fft_size  # the last segment can overlap the end of the data array by no more than one window size
total_segments = np.int32(np.ceil(len(data) / np.float32(hop_size)))
t_max = len(data) / np.float32(fs)

window = np.hanning(fft_size)  # our half cosine window
inner_pad = np.zeros(fft_size)  # the zeros which will be used to double each segment size

proc = np.concatenate((data, np.zeros(pad_end_size)))  # the data to process
result = np.empty((total_segments, fft_size), dtype=np.float32)  # space to hold the result

for i in range(total_segments):  # for each segment
    current_hop = hop_size * i  # figure out the current segment offset
    segment = proc[current_hop:current_hop + fft_size]  # get the current segment
    windowed = segment * window  # multiply by the half cosine function
    padded = np.append(windowed, inner_pad)  # add 0s to double the length of the data
    spectrum = np.fft.fft(padded) / fft_size  # take the Fourier Transform and scale by the number of samples
    auto_power = np.abs(spectrum * np.conj(spectrum))  # find the auto_power spectrum
    result[i, :] = auto_power[:fft_size]  # append to the results array

result = 20 * np.log10(result)  # scale to db
result = np.clip(result, -40, 200)  # clip values

matplotlib.use('TkAgg')

img = plt.imshow(result, origin='lower', cmap='jet', interpolation='nearest', aspect='auto')
plt.show()
