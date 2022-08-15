import ffmpeg


# TODO изменение громкости фрагмента, изменение скорости, склейка, вставка, история изменений

path = 'C:/Users/funov/Desktop/test/ok-i-pull-up.mp3'
foo = ffmpeg.input(path)
foo = ffmpeg.trim(foo, start=2, end=6)
foo = ffmpeg.output(foo, 'C:/Users/funov/Desktop/test/result.mp3')
ffmpeg.run(foo)
