import os

VALID_EXT_LIST = ['.py', '.js']
INVALID_KEYWORD_LIST = [
    'node_modules',
    '.git',
    '.idea',
    'index.js',
    'setupTests.js',
]
N_LINES_NORMAL_MIN, N_LINES_NORMAL_MAX = 10, 100


def is_valid_path(dir_or_file_path: str) -> bool:
    for invalid_keyword in INVALID_KEYWORD_LIST:
        if invalid_keyword in dir_or_file_path:
            return False

    # Ignore All Caps Names
    file_name_only = os.path.basename(dir_or_file_path).split('.')[0]
    if file_name_only == file_name_only.upper():
        return False

    return True


def is_valid_file_ext(file_path: str) -> bool:
    ext = os.path.splitext(file_path)[1]
    return ext in VALID_EXT_LIST


def get_n_lines(file_path: str) -> int:
    content = None
    with open(file_path, mode='r', encoding="utf8") as file:
        content = file.read()
    lines = content.split('\n')
    return len(lines)


def get_emoji(n):
    if n >= 200:
        return '🔴'
    if n >= 150:
        return '🟠'
    if n >= 100:
        return '🟡'

    if n < 10:
        return '🔵'
    if n < 5:
        return '🟣'

    return '🟢'


def get_long_file_info(dir_path):
    long_file_info_list = []
    for name_only in os.listdir(dir_path):
        dir_or_file_path = os.path.join(dir_path, name_only)

        if not is_valid_path(dir_or_file_path):
            continue

        if os.path.isdir(dir_or_file_path):
            long_file_info_list.extend(get_long_file_info(dir_or_file_path))
            continue

        if not is_valid_file_ext(dir_or_file_path):
            continue

        n_lines = get_n_lines(dir_or_file_path)
        emoji = get_emoji(n_lines)
        long_file_info_list.append(
            dict(
                file_path=dir_or_file_path,
                n_lines=n_lines,
                emoji=emoji,
            )
        )
    return long_file_info_list


def main():
    root_path = os.getcwd()
    long_file_info_list = get_long_file_info(root_path)
    sorted_long_file_info_list = sorted(
        long_file_info_list, key=lambda x: x['n_lines'], 
    )

    total_n_lines = sum([x['n_lines'] for x in long_file_info_list])
    print(f'{total_n_lines:,}', 'lines in TOTAL')

    for long_file_info in sorted_long_file_info_list:
        if (
            N_LINES_NORMAL_MIN
            <= long_file_info['n_lines']
            < N_LINES_NORMAL_MAX
        ):
            continue
        print(
            long_file_info['emoji'],
            long_file_info['n_lines'],
            long_file_info['file_path'].replace(root_path, '')[1:],
        )


if __name__ == '__main__':
    main()
