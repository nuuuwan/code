import os

from utils import File, Log

log = Log('small_files')
VALID_EXT_LIST = ['.py', '.js']
N_LINES_INFO, N_LINES_WARNING, N_LINES_ERROR = 100, 150, 200


def process_file(file_path):
    ext = os.path.splitext(file_path)[1]
    if ext not in VALID_EXT_LIST:
        return

    lines = File(file_path).read_lines()
    n_lines = len(lines)

    message = f'{n_lines} {file_path} '
    if n_lines > N_LINES_ERROR:
        logger = log.error
    elif n_lines > N_LINES_WARNING:
        logger = log.warning
    elif n_lines > N_LINES_INFO:
        logger = log.info
    else:
        return

    logger(message)


def process_dir(dir_path=None):
    dir_path = dir_path or os.getcwd()
    for name_only in os.listdir(dir_path):
        dir_or_file_path = os.path.join(dir_path, name_only)
        if os.path.isdir(dir_or_file_path):
            process_dir(dir_or_file_path)
        else:
            process_file(dir_or_file_path)


if __name__ == '__main__':
    process_dir()
