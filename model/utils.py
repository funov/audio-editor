def to_str_time(seconds, minutes, hours):
    seconds, minutes = convert(seconds, minutes)
    minutes, hours = convert(minutes, hours)

    if hours > 99:
        raise ValueError

    return f'{hours}:{minutes}:{seconds}'


def from_str_time_to_int_seconds(str_time):
    list_time = list(map(lambda x: float(x), str_time.split(':')))

    return list_time[0] * 60 * 60 + list_time[1] * 60 + list_time[2]


def convert(from_, to_):
    if from_ > 59:
        to_ += from_ // 60
        from_ %= 60

    return from_, to_
