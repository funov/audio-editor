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

# последний сегмент может перекрывать конец массива данных не более чем на один размер окна
pad_end_size = fft_size

total_segments = np.int32(np.ceil(len(data) / np.float32(hop_size)))
t_max = len(data) / np.float32(fs)

# наше окно с половинным косинусом
window = np.hanning(fft_size)

# нули, которые будут использоваться для удвоения размера каждого сегмента
inner_pad = np.zeros(fft_size)

# данные для обработки
proc = np.concatenate((data, np.zeros(pad_end_size)))

# пространство для хранения результата
result = np.empty((total_segments, fft_size), dtype=np.float32)

# для каждого сегмента
for i in range(total_segments):
    # определите текущее смещение сегмента
    current_hop = hop_size * i

    # получить текущий сегмент
    segment = proc[current_hop:current_hop + fft_size]

    # умножьте на функцию половины косинуса
    windowed = segment * window

    # добавьте нули, чтобы удвоить длину данных
    padded = np.append(windowed, inner_pad)

    # возьмите преобразование Фурье и масштабируйте по количеству выборок
    spectrum = np.fft.fft(padded) / fft_size

    # найдите спектр автоматической мощности
    auto_power = np.abs(spectrum * np.conj(spectrum))

    # добавить к массиву результатов
    result[i, :] = auto_power[:fft_size]

# масштабировать до дБ
result = 20 * np.log10(result)

# обрезать значения
result = np.clip(result, -40, 200)

result = np.rot90(result)
result = np.flipud(result)

matplotlib.use('TkAgg')

img = plt.imshow(result, origin='lower', cmap='jet', interpolation='nearest', aspect='auto')

plt.ylabel('Частота')
plt.xlabel('Время')

plt.xticks([])
plt.yticks([])

# TODO заменить на plt.imsave()
plt.show()
