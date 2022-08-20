class AudioInfo:
    def __init__(self, stdout):
        self.stdout_lines = [line for line in stdout]
        self.duration = self.get_duration()

    def get_duration(self):
        for stdout_line in self.stdout_lines:
            if 'Duration' in stdout_line:
                start = stdout_line.find(': ')
                end = stdout_line.find(', ')
                duration = stdout_line[start + 2:end]
                return duration

        raise ValueError
