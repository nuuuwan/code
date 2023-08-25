import os

from utils import File, Log

log = Log('small_files')
VALID_EXT_LIST = ['.py', '.js']
def is_valid_path(dir_or_file_path: str) -> bool:
    for invalid_keyword in INVALID_KEYWORD_LIST:
        if invalid_keyword in dir_or_file_path:
            return False

    return True


def is_valid_file_ext(file_path: str) -> bool:
    ext = os.path.splitext(file_path)[1]
    return ext in VALID_EXT_LIST
        return None

    lines = File(file_path).read_lines()
    n_lines = len(lines)
    if n_lines <= 100:
        return None

    return n_lines


def get_long_file_info(dir_path):
    long_file_info_list = []
    for name_only in os.listdir(dir_path):
        dir_or_file_path = os.path.join(dir_path, name_only)
        if os.path.isdir(dir_or_file_path):
            long_file_info_list += get_long_file_info(dir_or_file_path)
        else:
            n_lines = get_n_lines(dir_or_file_path)
            if n_lines:
                long_file_info_list.append(
                    dict(file_path=dir_or_file_path, n_lines=n_lines)
                )
    return long_file_info_list


def main():
    root_path = os.getcwd()
    long_file_info_list = get_long_file_info(root_path)
    if not long_file_info_list:
        return 
    
    print('-' * 32)
    print('LONG FILES')
    print('-' * 32)
    sorted_long_file_info_list = sorted(
        long_file_info_list, key=lambda x: x['n_lines'], reverse=True
    )
    for long_file_info in sorted_long_file_info_list:
        print(
            long_file_info['n_lines'],
            long_file_info['file_path'].replace(root_path, '')[1:],
        )
    print('-' * 32)


if __name__ == '__main__':
    main()
