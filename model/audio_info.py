from model.time_utils import from_str_time_to_int_seconds


class AudioInfo:
    def __init__(self, process_std):
        self.std_output = process_std[0]
        self.std_err = process_std[1]

        self.stdout_lines = [line for line in self.std_output.split('\n')]
        self.stderr_lines = [line for line in self.std_err.split('\n')]

        self.str_duration = self.get_str_duration()
        self.int_duration = from_str_time_to_int_seconds(self.str_duration)

    def get_str_duration(self):
        for stdout_line in self.stdout_lines:
            if 'Duration' in stdout_line:
                start = stdout_line.find(': ')
                end = stdout_line.find(', ')
                duration = stdout_line[start + 2:end]
                return duration

        for stderr_line in self.stderr_lines:
            if 'Duration' in stderr_line:
                start = stderr_line.find(': ')
                end = stderr_line.find(', ')
                duration = stderr_line[start + 2:end]
                return duration

        raise ValueError
