from model.utils import from_str_time_to_int_seconds


class AudioInfo:
    def __init__(self, stdout):
        self.stdout_lines = [line for line in stdout]
        self.str_duration = self.get_str_duration()
        self.int_duration = from_str_time_to_int_seconds(self.str_duration)

    def get_str_duration(self):
        for stdout_line in self.stdout_lines:
            if 'Duration' in stdout_line:
                start = stdout_line.find(': ')
                end = stdout_line.find(', ')
                duration = stdout_line[start + 2:end]
                return duration

        raise ValueError
