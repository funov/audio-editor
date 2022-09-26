import numpy as np
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
import matplotlib


matplotlib.use('TkAgg')


class Spectrogram:
    def __init__(self, audio_path, overlap_factor=0.5, fft_size=2**10):
        self.audio_path = audio_path

        fs, data = wav.read(audio_path)
        if len(data.shape) > 1:
            data = data[..., 0]
        self.fs = fs
        self.data = data

        self.overlap_factor = overlap_factor
        self.fft_size = fft_size

        self.hop_size = np.int32(np.floor(fft_size * (1 - overlap_factor)))

    def get_spectrogram(self):
        # последний сегмент может перекрывать конец массива данных не более чем на один размер окна
        pad_end_size = self.fft_size

        total_segments = np.int32(np.ceil(len(self.data) / np.float32(self.hop_size)))

        # наше окно с половинным косинусом
        window = np.hanning(self.fft_size)

        # нули, которые будут использоваться для удвоения размера каждого сегмента
        inner_pad = np.zeros(self.fft_size)

        # данные для обработки
        proc = np.concatenate((self.data, np.zeros(pad_end_size)))

        # пространство для хранения результата
        result = np.empty((total_segments, self.fft_size), dtype=np.float32)

        # для каждого сегмента
        for i in range(total_segments):
            # определите текущее смещение сегмента
            current_hop = self.hop_size * i

            # получить текущий сегмент
            segment = proc[current_hop:current_hop + self.fft_size]

            # умножьте на функцию половины косинуса
            windowed = segment * window

            # добавьте нули, чтобы удвоить длину данных
            padded = np.append(windowed, inner_pad)

            # возьмите преобразование Фурье и масштабируйте по количеству выборок
            spectrum = np.fft.fft(padded) / self.fft_size

            # найдите спектр автоматической мощности
            auto_power = np.abs(spectrum * np.conj(spectrum))

            # добавить к массиву результатов
            result[i, :] = auto_power[:self.fft_size]

        # масштабировать до дБ
        result = 20 * np.log10(result)

        # обрезать значения
        result = np.clip(result, -40, 200)

        result = np.rot90(result)
        result = np.flipud(result)

        return result

    def save_spectrogram(self, spectrogram, path):
        plt.imshow(spectrogram, origin='lower', cmap='jet', interpolation='nearest', aspect='auto')

        plt.ylabel('Частота')
        plt.xlabel('Время')

        plt.xticks([])
        plt.yticks([])

        plt.savefig(path)
