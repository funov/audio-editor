def to_str_time(seconds, minutes, hours):
    seconds, minutes = convert(seconds, minutes)
    minutes, hours = convert(minutes, hours)

    if hours > 99:
        raise ValueError

    hours = add_start_zeros(hours)
    minutes = add_start_zeros(minutes)
    seconds = add_start_zeros(seconds)

    return hours + ':' + minutes + ':' + seconds


def from_str_time_to_int_seconds(str_time):
    list_time = list(map(lambda x: float(x), str_time.split(':')))

    return list_time[0] * 60 * 60 + list_time[1] * 60 + list_time[2]


def add_start_zeros(float_value):
    if len(str(int(float_value))) == 1:
        str_value = '0' + str(float_value)
        return str_value

    return str(float_value)


def convert(from_, to_):
    if from_ > 59:
        to_ += from_ // 60
        from_ %= 60

    return from_, to_
