from model.command_line_executor import CommandLineExecutor
from model.audio_info import AudioInfo
from model.utils import to_str_time


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
    def change_speed(input_audio_path, output_audio_path, speed, is_debug=False):
        if speed <= 0:
            raise ValueError

        command = f'ffmpeg -i {input_audio_path} -af atempo={speed} {output_audio_path}'
        AudioEditor.execute_command(command, is_debug)

    @staticmethod
    def crop_audio(input_audio_path, output_audio_path, start_s, start_m, start_h, duration, is_debug=False):
        start_time = to_str_time(start_s, start_m, start_h)
        command = f'ffmpeg -ss {start_time} -i {input_audio_path} -t {duration} {output_audio_path}'
        AudioEditor.execute_command(command, is_debug)

    @staticmethod
    def change_volume(input_audio_path, output_audio_path, volume, is_debug=False):
        command = f'ffmpeg -i {input_audio_path} -af "volume={volume}dB" {output_audio_path}'
        AudioEditor.execute_command(command, is_debug)

    @staticmethod
    def paste_audio():
        # target_audio_path, input_audio_path, output_audio_path, paste_s, paste_m, paste_h, is_debug=False
        # paste_time = to_str_time(paste_s, paste_m, paste_h)
        # target_info = AudioEditor.get_audio_info(target_audio_path, is_debug)
        pass

    @staticmethod
    def change_fragment_speed():
        pass

    @staticmethod
    def change_fragment_volume():
        pass

    @staticmethod
    def reverse_fragment_audio():
        pass

    @staticmethod
    def get_audio_info(audio_path, is_debug=False):
        command = f'ffmpeg -i {audio_path}'
        process = AudioEditor.execute_command(command, is_debug)
        info = AudioInfo(process.stdout)

        return info
