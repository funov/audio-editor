import os

from model.command_line_executor import CommandLineExecutor
from model.audio_info import AudioInfo
from model.time_utils import get_file_name, from_str_time_to_int_seconds
from model.spectrogram import Spectrogram


class AudioEditor:
    @staticmethod
    def glue_audio(input_audio_paths, output_audio_path, is_debug=False):
        command = f'ffmpeg -i "concat:{"|".join(input_audio_paths)}" ' \
                  f'{output_audio_path}'

        AudioEditor._execute_command(command, is_debug)

    @staticmethod
    def crop_audio(
            input_audio_path,
            output_audio_path,
            start_time=None,
            end_time=None,
            is_debug=False
    ):
        input_audio_info = AudioEditor.get_audio_info(
            input_audio_path,
            is_debug
        )

        if start_time is None and end_time is None:
            command = f'ffmpeg -i {input_audio_path} {output_audio_path}'
        elif start_time is not None and end_time is not None:
            int_start_time = from_str_time_to_int_seconds(start_time)
            int_end_time = from_str_time_to_int_seconds(end_time)

            if not (0 <= int_start_time < int_end_time
                    <= input_audio_info.int_duration):
                raise ValueError

            command = f'ffmpeg -ss {start_time} -to {end_time} -i ' \
                      f'{input_audio_path} {output_audio_path}'
        elif start_time is None:
            int_end_time = from_str_time_to_int_seconds(end_time)

            if not (0 <= int_end_time <= input_audio_info.int_duration):
                raise ValueError

            command = f'ffmpeg -to {end_time} -i {input_audio_path} ' \
                      f'{output_audio_path}'
        else:
            int_start_time = from_str_time_to_int_seconds(start_time)

            if not (0 <= int_start_time <= input_audio_info.int_duration):
                raise ValueError

            command = f'ffmpeg -ss {start_time} -i {input_audio_path} ' \
                      f'{output_audio_path}'

        AudioEditor._execute_command(command, is_debug)

    @staticmethod
    def paste_audio(
            target_audio_path,
            input_audio_path,
            output_audio_path,
            paste_time,
            is_debug=False
    ):
        target_audio_info = AudioEditor.get_audio_info(
            target_audio_path,
            is_debug
        )
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

        AudioEditor.glue_audio(
            [
                first_file_name,
                input_audio_path.replace('/', current_sep),
                second_file_name
            ],
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
            start_time=None,
            end_time=None,
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
                start_time,
                end_time,
                is_debug
            )

        reversed_file_name \
            = f'{output_audio_folder}{current_sep}{get_file_name()}.mp3'

        AudioEditor.reverse_audio(
            second_file_name,
            reversed_file_name,
            is_debug=is_debug
        )

        AudioEditor._glue_three_parts(
            first_file_name,
            reversed_file_name,
            third_file_name,
            output_audio_path,
            is_debug
        )

    @staticmethod
    def change_speed(
            input_audio_path,
            output_audio_path,
            speed,
            is_debug=False
    ):
        if 10 < float(speed) < 0.5:
            raise ValueError

        command = f'ffmpeg -i {input_audio_path} -af atempo={speed} ' \
                  f'{output_audio_path}'
        AudioEditor._execute_command(command, is_debug)

    @staticmethod
    def change_fragment_speed(
            input_audio_path,
            output_audio_path,
            speed,
            start_time=None,
            end_time=None,
            is_debug=False
    ):
        AudioEditor._change_fragment_value(
            input_audio_path,
            output_audio_path,
            speed,
            AudioEditor.change_speed,
            start_time,
            end_time,
            is_debug
        )

    @staticmethod
    def change_volume(
            input_audio_path,
            output_audio_path,
            volume,
            is_debug=False
    ):
        if not (-30 < int(volume) < 30):
            raise ValueError

        command = f'ffmpeg -i {input_audio_path} -af "volume={volume}dB" ' \
                  f'{output_audio_path}'
        AudioEditor._execute_command(command, is_debug)

    @staticmethod
    def change_fragment_volume(
            input_audio_path,
            output_audio_path,
            volume,
            start_time=None,
            end_time=None,
            is_debug=False
    ):
        AudioEditor._change_fragment_value(
            input_audio_path,
            output_audio_path,
            volume,
            AudioEditor.change_volume,
            start_time,
            end_time,
            is_debug
        )

    @staticmethod
    def convert(input_audio_path, output_audio_path, is_debug=False):
        command = f'ffmpeg -i {input_audio_path} {output_audio_path}'
        AudioEditor._execute_command(command, is_debug)

    @staticmethod
    def get_audio_info(audio_path, is_debug=False):
        command = f'ffmpeg -i {audio_path}'
        stdout = AudioEditor._execute_command(command, is_debug)
        info = AudioInfo(stdout)

        return info

    @staticmethod
    def get_spectrogram(
            input_audio_path,
            output_picture_path,
            is_debug=False
    ):
        if input_audio_path.split('.')[-1] != 'wav':
            converted_audio_path = '.'.join(
                input_audio_path.split('.')[:-1]
            ) + '.wav'
            AudioEditor.convert(
                input_audio_path,
                converted_audio_path,
                is_debug
            )
        else:
            converted_audio_path = input_audio_path

        spectrogram = Spectrogram(converted_audio_path, is_debug)
        result = spectrogram.get_spectrogram()
        Spectrogram.save_spectrogram(result, output_picture_path)

    @staticmethod
    def _change_fragment_value(
            input_audio_path,
            output_audio_path,
            value,
            change_value_func,
            start_time,
            end_time,
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
                start_time,
                end_time,
                is_debug
            )

        changed_value_file_name \
            = f'{output_audio_folder}{current_sep}{get_file_name()}.mp3'

        change_value_func(
            second_file_name,
            changed_value_file_name,
            value,
            is_debug=is_debug
        )

        AudioEditor._glue_three_parts(
            first_file_name,
            changed_value_file_name,
            third_file_name,
            output_audio_path,
            is_debug
        )

    @staticmethod
    def _glue_three_parts(
            first_file_name,
            second_file_name,
            third_file_name,
            output_audio_path,
            is_debug=False
    ):
        glue_paths = []
        if first_file_name is not None:
            glue_paths.append(first_file_name)
        glue_paths.append(second_file_name)
        if third_file_name is not None:
            glue_paths.append(third_file_name)

        AudioEditor.glue_audio(
            glue_paths,
            output_audio_path,
            is_debug=is_debug
        )

    @staticmethod
    def _crop_three_parts(
            input_audio_path,
            output_audio_folder,
            current_sep,
            start_time,
            end_time,
            is_debug=False
    ):
        first_file_name = None
        third_file_name = None

        if start_time is not None:
            first_file_name \
                = f'{output_audio_folder}{current_sep}{get_file_name()}.mp3'
            AudioEditor.crop_audio(
                input_audio_path,
                first_file_name,
                None,
                start_time,
                is_debug=is_debug
            )

        second_file_name \
            = f'{output_audio_folder}{current_sep}{get_file_name()}.mp3'
        AudioEditor.crop_audio(
            input_audio_path,
            second_file_name,
            start_time,
            end_time,
            is_debug=is_debug
        )

        if end_time is not None:
            third_file_name \
                = f'{output_audio_folder}{current_sep}{get_file_name()}.mp3'
            AudioEditor.crop_audio(
                input_audio_path,
                third_file_name,
                end_time,
                None,
                is_debug=is_debug
            )

        return first_file_name, second_file_name, third_file_name

    @staticmethod
    def _execute_command(command, is_debug=False):
        command_executor = CommandLineExecutor(command)
        process = command_executor.run()

        result = process.communicate()

        stdout = result[0]

        if not is_debug:
            return stdout

        AudioEditor._print_std(stdout)

        return stdout

    @staticmethod
    def _print_std(std_output):
        for line in std_output.split('\n'):
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
