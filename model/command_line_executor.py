import subprocess


class CommandLineExecutor:
    def __init__(self, command, with_output=False, working_directory=None):
        self.command = command
        self.working_directory = working_directory
        self.with_output = with_output

    def run(self):
        stdout = subprocess.PIPE if self.with_output else None
        stderr = subprocess.STDOUT if self.with_output else None

        process = subprocess.Popen(
            self.command,
            stdout=stdout,
            stderr=stderr,
            universal_newlines=True,
            cwd=self.working_directory
        )

        return process
