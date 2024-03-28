import os
import sys

from utils import File, Log

log = Log('build_inits')


def build_for_dir(dir_src, dir_code):
    high_module_name = (
        dir_code.replace(dir_src + '\\', '')
        .replace('/', '.')
        .replace('\\', '.')
    )
    if 'src' in high_module_name:
        return

    lines = ['# ' + high_module_name + ' (auto generate by build_inits.py)']

    modules_lines = []
    for file in os.listdir(dir_code):
        if not file.endswith('.py'):
            continue
        if file == '__init__.py':
            continue

        class_name = file.replace('.py', '')
        line = f'from {high_module_name}.{class_name} import {class_name}'
        modules_lines.append(line)
    if modules_lines:
        lines.append('')
        lines.extend(modules_lines)
        lines.append('')

    child_modules_lines = []
    for child_dir, __, __ in os.walk(dir_code):
        if child_dir == dir_code:
            continue

        if child_dir == '__pycache__':
            continue
        child_dir_base = (
            child_dir.replace(dir_code + '\\', '')
            .replace('\\', '.')
            .split('.')[0]
        )
        child_module_name = f'{high_module_name}.{child_dir_base}'
        class_names = []
        for file in os.listdir(child_dir):
            if not file.endswith('.py'):
                continue
            if file == '__init__.py':
                continue

            class_name = file.replace('.py', '')
            class_names.append(class_name)

        if class_names:
            class_names_str = ''.join(
                ['    ' + class_name + ',\n' for class_name in class_names]
            )
            line = f'from {child_module_name} import (\n{class_names_str})'
            child_modules_lines.append(line)
            child_modules_lines.append('')

    if child_modules_lines:
        lines.append('')
        lines.extend(child_modules_lines)
        lines.append('')

    init_py_path = os.path.join(dir_code, '__init__.py')
    File(init_py_path).write_lines(lines)
    log.debug(f'Wrote {init_py_path}')


def main(dir_root: str):
    dir_src = os.path.join(dir_root, 'src')
    assert os.path.exists(dir_src), f'{dir_src} does not exist'

    for dir_code, __, __ in os.walk(dir_src):
        if '__pycache__' in dir_code:
            continue
        build_for_dir(dir_src, dir_code)


if __name__ == "__main__":
    dir_root = sys.argv[1]
    main(dir_root)
