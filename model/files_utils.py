import os


def replace_with_rename(source, destination_folder, new_name=None):
    destination = destination_folder + '/' + source.split('/')[-1]
    destination_with_new_name = destination

    if new_name is not None:
        destination_with_new_name = destination_folder + '/' + new_name

    try:
        os.replace(source, destination)
        if new_name is not None:
            os.rename(destination, destination_with_new_name)
    except OSError:
        print(f'Что-то пошло не так, проверьте пути:\n'
              f'Источник - {source}\n'
              f'Перемещенный источник - {destination}\n'
              f'Новое имя источника - {destination_with_new_name}')

    return destination_with_new_name
