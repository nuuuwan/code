import os

from utils import File

VALID_EXT_LIST = ['.py', '.js']
INVALID_KEYWORD_LIST = ['node_modules', '.git', '.idea']


def is_valid_path(dir_or_file_path: str) -> bool:
    for invalid_keyword in INVALID_KEYWORD_LIST:
        if invalid_keyword in dir_or_file_path:
            return False

    return True


def is_valid_file_ext(file_path: str) -> bool:
    ext = os.path.splitext(file_path)[1]
    return ext in VALID_EXT_LIST


def get_n_lines(file_path: str) -> int:
    lines = File(file_path).read_lines()
    return len(lines)


def get_long_file_info(dir_path):
    long_file_info_list = []
    for name_only in os.listdir(dir_path):
        dir_or_file_path = os.path.join(dir_path, name_only)
        if not is_valid_path(dir_or_file_path):
            continue

        if os.path.isdir(dir_or_file_path):
            long_file_info_list.extend(get_long_file_info(dir_or_file_path))
        else:
            if not is_valid_file_ext(dir_or_file_path):
                continue
            long_file_info_list.append(
                dict(
                    file_path=dir_or_file_path,
                    n_lines=get_n_lines(dir_or_file_path),
                )
            )
    return long_file_info_list


def main():
    root_path = os.getcwd()
    long_file_info_list = get_long_file_info(root_path)
    len(long_file_info_list)
    print(' ')
    print('-' * 32)
    sorted_long_file_info_list = sorted(
        long_file_info_list, key=lambda x: x['n_lines'], reverse=True
    )
    for long_file_info in sorted_long_file_info_list:
        if long_file_info['n_lines'] <= 100:
            continue
        print(
            long_file_info['n_lines'],
            long_file_info['file_path'].replace(root_path, '')[1:],
        )

    total_n_lines = sum([x['n_lines'] for x in long_file_info_list])
    print(f'{total_n_lines:,}', 'TOTAL')
    print('-' * 32)
    print(' ')


if __name__ == '__main__':
    main()
