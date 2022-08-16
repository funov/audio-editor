import subprocess

cmd = 'ffmpeg -i result.mp3 '

process = subprocess.Popen(
    cmd,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    universal_newlines=True,
    cwd='C:/Users/funov/Desktop/test'
)

for line in process.stdout:
    print(line)
