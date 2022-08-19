import subprocess


class CommandLineExecutor:
    def __init__(self, command, working_directory=None):
        self.command = command
        self.working_directory = working_directory

    def run(self):
        process = subprocess.Popen(
            self.command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            cwd=self.working_directory
        )

        return process
