def to_str_time(seconds, minutes, hours):
    seconds, minutes = convert(seconds, minutes)
    minutes, hours = convert(minutes, hours)

    if hours > 99:
        raise ValueError

    return f'{hours}:{minutes}:{seconds}'


def convert(from_, to_):
    if from_ > 99:
        to_ += from_ // 60
        from_ %= 60

    return from_, to_
