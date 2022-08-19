import subprocess

# Аудио наоборот
# ffmpeg -i input.mp3 -map 0 -af "areverse" output.mp3

# Конвертировать wav в mp3
# ffmpeg -i a.wav b.mp3

# Конвертировать mp3 в wav
# ffmpeg -i result.mp3 a.wav

# Склейка
# ffmpeg -i "concat:output.mp3|run.mp3|b.mp3" r.mp3

# Скорость
# ffmpeg -i b.mp3 -af atempo=5 q.mp3

# Обрезка
# ffmpeg -ss 00:00:02 -i b.mp3 -t 2 result.mp3

# Громкость
# ffmpeg -i b.mp3 -af "volume=1dB" d.mp3

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
