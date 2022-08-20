from command_line_executor import CommandLineExecutor
from audio_info import AudioInfo
from utils import to_str_time


class AudioEditor:
    @staticmethod
    def execute_command(command, is_debug=False):
        command_executor = CommandLineExecutor(command)
        process = command_executor.run()

        if not is_debug:
            return process

        AudioEditor.print_std(process.stdout)
        AudioEditor.print_std(process.stderr)

        return process

    @staticmethod
    def print_std(std):
        if std is None:
            return
        for line in std:
            print(line)

    @staticmethod
    def reverse_audio(input_audio_path, output_audio_path, is_debug=False):
        command = f'ffmpeg -i {input_audio_path} -map 0 -af "areverse" {output_audio_path}'
        AudioEditor.execute_command(command, is_debug)

    @staticmethod
    def convert(input_audio_path, output_audio_path, is_debug=False):
        command = f'ffmpeg -i {input_audio_path} {output_audio_path}'
        AudioEditor.execute_command(command, is_debug)

    @staticmethod
    def glue_audio(input_audio_paths, output_audio_path, is_debug=False):
        command = f'ffmpeg -i "concat:{"|".join(input_audio_paths)}" {output_audio_path}'
        AudioEditor.execute_command(command, is_debug)

    @staticmethod
    def change_speed(input_audio_paths, output_audio_path, speed, is_debug=False):
        if speed <= 0:
            raise ValueError

        command = f'ffmpeg -i {input_audio_paths} -af atempo={speed} {output_audio_path}'
        AudioEditor.execute_command(command, is_debug)

    @staticmethod
    def crop_audio(input_audio_paths, output_audio_path, start_s, start_m, start_h, duration, is_debug=False):
        start = to_str_time(start_s, start_m, start_h)
        command = f'ffmpeg -ss {start} -i {input_audio_paths} -t {duration} {output_audio_path}'
        AudioEditor.execute_command(command, is_debug)

    @staticmethod
    def change_volume(input_audio_paths, output_audio_path, volume, is_debug=False):
        command = f'ffmpeg -i {input_audio_paths} -af "volume={volume}dB" {output_audio_path}'
        AudioEditor.execute_command(command, is_debug)

    @staticmethod
    def get_audio_info(audio_path, is_debug=False):
        command = f'ffmpeg -i {audio_path}'
        process = AudioEditor.execute_command(command, is_debug)
        info = AudioInfo(process.stdout)

        return info
