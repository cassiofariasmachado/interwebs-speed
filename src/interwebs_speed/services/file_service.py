import os


def save_csv(file_path, lines, mode='w'):
    with open(file_path, mode, encoding='utf-8') as file:
        file.write('\n'.join(lines) + '\n')


def exists(file_path):
    return os.path.isfile(file_path)
