from command_line_executor import CommandLineExecutor


class AudioEditor:
    @staticmethod
    def execute_command(command, is_debug=False):
        command_executor = CommandLineExecutor(command)
        process = command_executor.run()

        if not is_debug:
            return

        AudioEditor.print_std(process.stdout)
        AudioEditor.print_std(process.stderr)

    @staticmethod
    def print_std(std):
        if std is None:
            return
        for line in std:
            print(line)

    @staticmethod
    def reverse_audio(input_audio_path, output_audio_path, is_debug=False):
        # Аудио наоборот
        # ffmpeg -i input.mp3 -map 0 -af "areverse" output.mp3

        command = f'ffmpeg -i {input_audio_path} -map 0 -af "areverse" {output_audio_path}'
        AudioEditor.execute_command(command, is_debug)

    @staticmethod
    def convert(input_audio_path, output_audio_path, is_debug=False):
        # Конвертировать wav в mp3
        # ffmpeg -i C:\Users\funov\Desktop\test\a.wav C:\Users\funov\Desktop\b.mp3

        command = f'ffmpeg -i {input_audio_path} {output_audio_path}'
        AudioEditor.execute_command(command, is_debug)

    @staticmethod
    def glue_audio(input_audio_paths, output_audio_path, is_debug=False):
        # Склейка
        # ffmpeg -i "concat:output.mp3|run.mp3|b.mp3" r.mp3

        command = f'ffmpeg -i "concat:{"|".join(input_audio_paths)}" {output_audio_path}'
        AudioEditor.execute_command(command, is_debug)

    @staticmethod
    def change_speed(input_audio_paths, output_audio_path, speed, is_debug=False):
        # Скорость
        # ffmpeg -i b.mp3 -af atempo=5 q.mp3

        if speed <= 0:
            raise ValueError

        command = f'ffmpeg -i {input_audio_paths} -af atempo={speed} {output_audio_path}'
        AudioEditor.execute_command(command, is_debug)

    @staticmethod
    def crop_audio(input_audio_paths, output_audio_path, start, duration, is_debug=False):
        # Обрезка
        # ffmpeg -ss 00:00:02 -i b.mp3 -t 2 result.mp3

        command = f'ffmpeg -ss {start} -i {input_audio_paths} -t {duration} {output_audio_path}'
        AudioEditor.execute_command(command, is_debug)

    @staticmethod
    def change_volume(input_audio_paths, output_audio_path, volume, is_debug=False):
        # Громкость
        # ffmpeg -i b.mp3 -af "volume=1dB" d.mp3
        # volume любой

        command = f'ffmpeg -i {input_audio_paths} -af "volume={volume}dB" {output_audio_path}'
        AudioEditor.execute_command(command, is_debug)
