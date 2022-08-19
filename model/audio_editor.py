from command_line_executor import CommandLineExecutor


class AudioEditor:
    @staticmethod
    def reverse_audio():
        # Аудио наоборот
        # ffmpeg -i input.mp3 -map 0 -af "areverse" output.mp3
        pass

    @staticmethod
    def convert():
        # Конвертировать wav в mp3
        # ffmpeg -i a.wav b.mp3
        # ffmpeg -i C:\Users\funov\Desktop\test\a.wav C:\Users\funov\Desktop\b.mp3

        # Конвертировать mp3 в wav
        # ffmpeg -i result.mp3 a.wav
        pass

    @staticmethod
    def glue_audio():
        # Склейка
        # ffmpeg -i "concat:output.mp3|run.mp3|b.mp3" r.mp3
        pass

    @staticmethod
    def change_speed():
        # Скорость
        # ffmpeg -i b.mp3 -af atempo=5 q.mp3
        pass

    @staticmethod
    def crop_audio():
        # Обрезка
        # ffmpeg -ss 00:00:02 -i b.mp3 -t 2 result.mp3
        pass

    @staticmethod
    def change_volume():
        # Громкость
        # ffmpeg -i b.mp3 -af "volume=1dB" d.mp3
        pass
