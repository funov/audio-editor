import os
import time

from model.command_line_executor import CommandLineExecutor
from model.audio_info import AudioInfo
from model.time_utils import get_file_name, from_str_time_to_int_seconds


class AudioEditor:
    @staticmethod
    def glue_audio(input_audio_paths, output_audio_path, is_debug=False):
        # TODO Попробовать .mp3 и .wav
        command = f'ffmpeg -i "concat:{"|".join(input_audio_paths)}" ' \
                  f'{output_audio_path}'

        AudioEditor._execute_command(command, is_debug)

    @staticmethod
    def crop_audio(
            input_audio_path,
            output_audio_path,
            start_time,
            end_time,
            is_debug=False
    ):
        input_audio_info = AudioEditor.get_audio_info(input_audio_path, is_debug)
        int_start_time = from_str_time_to_int_seconds(start_time)
        int_end_time = from_str_time_to_int_seconds(end_time)

        if not (0 <= int_start_time < int_end_time <= input_audio_info.int_duration):
            raise ValueError

        command = f'ffmpeg -ss {start_time} -to {end_time} -i {input_audio_path} {output_audio_path}'

        AudioEditor._execute_command(command, is_debug)

    @staticmethod
    def paste_audio(
            target_audio_path,
            input_audio_path,
            output_audio_path,
            paste_time,
            is_debug=False
    ):
        target_audio_info = AudioEditor.get_audio_info(target_audio_path, is_debug)
        int_paste_time = from_str_time_to_int_seconds(paste_time)

        if not (0 <= int_paste_time <= target_audio_info.int_duration):
            raise ValueError

        current_sep = AudioEditor._get_current_sep(output_audio_path)

        output_audio_folder = AudioEditor._get_folder(
            output_audio_path,
            current_sep
        )

        first_file_name \
            = f'{output_audio_folder}{current_sep}{get_file_name()}.mp3'

        AudioEditor.crop_audio(
            target_audio_path,
            first_file_name,
            "00:00:00",
            paste_time,
            is_debug=is_debug
        )

        second_file_name \
            = f'{output_audio_folder}{current_sep}{get_file_name()}.mp3'

        AudioEditor.crop_audio(
            target_audio_path,
            second_file_name,
            paste_time,
            target_audio_info.str_duration,
            is_debug=is_debug
        )

        time.sleep(3)

        AudioEditor.glue_audio(
            [first_file_name, input_audio_path.replace('/', current_sep), second_file_name],
            output_audio_path,
            is_debug=is_debug
        )

    @staticmethod
    def reverse_audio(input_audio_path, output_audio_path, is_debug=False):
        command = f'ffmpeg -i {input_audio_path} -map 0 -af "areverse" ' \
                  f'{output_audio_path}'
        AudioEditor._execute_command(command, is_debug)

    @staticmethod
    def reverse_fragment_audio(
            input_audio_path,
            output_audio_path,
            start_s=None,
            start_m=None,
            start_h=None,
            duration_s=None,
            duration_m=None,
            duration_h=None,
            is_debug=False
    ):
        current_sep = AudioEditor._get_current_sep(output_audio_path)

        output_audio_folder = AudioEditor._get_folder(
            output_audio_path,
            current_sep
        )

        first_file_name, second_file_name, third_file_name \
            = AudioEditor._crop_three_parts(
                input_audio_path,
                output_audio_folder,
                current_sep,
                start_s,
                start_m,
                start_h,
                duration_s,
                duration_m,
                duration_h,
                is_debug
            )

        reversed_file_name \
            = output_audio_folder + current_sep + get_file_name()

        AudioEditor.reverse_audio(
            second_file_name,
            reversed_file_name,
            is_debug=is_debug
        )

        AudioEditor.glue_audio(
            [first_file_name, reversed_file_name, third_file_name],
            output_audio_path,
            is_debug=is_debug
        )

    @staticmethod
    def change_speed(
            input_audio_path,
            output_audio_path,
            speed,
            is_debug=False
    ):
        if 99 < speed < 0.5:
            raise ValueError

        command = f'ffmpeg -i {input_audio_path} -af atempo={speed} ' \
                  f'{output_audio_path}'
        AudioEditor._execute_command(command, is_debug)

    @staticmethod
    def change_fragment_speed(
            input_audio_path,
            output_audio_path,
            speed,
            start_s=None,
            start_m=None,
            start_h=None,
            duration_s=None,
            duration_m=None,
            duration_h=None,
            is_debug=False
    ):
        AudioEditor._change_fragment_value(
            input_audio_path,
            output_audio_path,
            speed,
            AudioEditor.change_speed,
            start_s,
            start_m,
            start_h,
            duration_s,
            duration_m,
            duration_h,
            is_debug
        )

    @staticmethod
    def change_volume(
            input_audio_path,
            output_audio_path,
            volume,
            is_debug=False
    ):
        command = f'ffmpeg -i {input_audio_path} -af "volume={volume}dB" ' \
                  f'{output_audio_path}'
        AudioEditor._execute_command(command, is_debug)

    @staticmethod
    def change_fragment_volume(
            input_audio_path,
            output_audio_path,
            volume,
            start_s=None,
            start_m=None,
            start_h=None,
            duration_s=None,
            duration_m=None,
            duration_h=None,
            is_debug=False
    ):
        AudioEditor._change_fragment_value(
            input_audio_path,
            output_audio_path,
            volume,
            AudioEditor.change_volume,
            start_s,
            start_m,
            start_h,
            duration_s,
            duration_m,
            duration_h,
            is_debug
        )

    @staticmethod
    def convert(input_audio_path, output_audio_path, is_debug=False):
        command = f'ffmpeg -i {input_audio_path} {output_audio_path}'
        AudioEditor._execute_command(command, is_debug)

    @staticmethod
    def get_audio_info(audio_path, is_debug=False):
        command = f'ffmpeg -i {audio_path}'
        process = AudioEditor._execute_command(command, is_debug)
        info = AudioInfo(process.stdout)

        return info

    @staticmethod
    def _change_fragment_value(
            input_audio_path,
            output_audio_path,
            value,
            change_value_func,
            start_s=None,
            start_m=None,
            start_h=None,
            duration_s=None,
            duration_m=None,
            duration_h=None,
            is_debug=False
    ):
        current_sep = AudioEditor._get_current_sep(output_audio_path)

        output_audio_folder = AudioEditor._get_folder(
            output_audio_path,
            current_sep
        )

        first_file_name, second_file_name, third_file_name \
            = AudioEditor._crop_three_parts(
                input_audio_path,
                output_audio_folder,
                current_sep,
                start_s,
                start_m,
                start_h,
                duration_s,
                duration_m,
                duration_h,
                is_debug
            )

        changed_value_file_name \
            = output_audio_folder + current_sep + get_file_name()

        change_value_func(
            second_file_name,
            changed_value_file_name,
            value,
            is_debug=is_debug
        )

        AudioEditor.glue_audio(
            [first_file_name, changed_value_file_name, third_file_name],
            output_audio_path,
            is_debug=is_debug
        )

    @staticmethod
    def _crop_three_parts(
            input_audio_path,
            output_audio_folder,
            current_sep,
            start_s,
            start_m,
            start_h,
            duration_s,
            duration_m,
            duration_h,
            is_debug
    ):
        first_file_name \
            = output_audio_folder + current_sep + get_file_name()
        second_file_name \
            = output_audio_folder + current_sep + get_file_name()
        third_file_name \
            = output_audio_folder + current_sep + get_file_name()

        AudioEditor.crop_audio(
            input_audio_path,
            first_file_name,
            duration_s=start_s,
            duration_m=start_m,
            duration_h=start_h,
            is_debug=is_debug
        )
        AudioEditor.crop_audio(
            input_audio_path,
            second_file_name,
            start_s=start_s,
            start_m=start_m,
            start_h=start_h,
            duration_s=duration_s,
            duration_m=duration_m,
            duration_h=duration_h,
            is_debug=is_debug
        )
        AudioEditor.crop_audio(
            input_audio_path,
            third_file_name,
            start_s=duration_s,
            start_m=duration_m,
            start_h=duration_h,
            is_debug=is_debug
        )

        return first_file_name, second_file_name, third_file_name

    @staticmethod
    def _execute_command(command, is_debug=False):
        command_executor = CommandLineExecutor(command)
        process = command_executor.run()

        if not is_debug:
            return process

        AudioEditor._print_std(process.stdout)
        AudioEditor._print_std(process.stderr)

        return process

    @staticmethod
    def _print_std(std):
        if std is None:
            return
        for line in std:
            print(line)

    @staticmethod
    def _get_current_sep(path):
        if os.sep in path:
            current_sep = os.sep
        else:
            current_sep = '/'

        return current_sep

    @staticmethod
    def _get_folder(path, current_sep):
        folder_list = path.split(current_sep)[:-1]
        folder = f'{current_sep}'.join(folder_list)

        return folder
