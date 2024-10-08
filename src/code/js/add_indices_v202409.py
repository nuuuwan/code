import os

from utils import File, Log

log = Log('add_indices_v202409')


def get_js_paths(dir_root: str) -> list[str]:
    js_paths = []
    for dir_path, _, file_names in os.walk(dir_root):
        for file_name in file_names:
            if not file_name.endswith('.js'):
                continue
            if file_name == 'index.js':
                index_path = os.path.join(dir_path, file_name)
                os.remove(index_path)
                continue
            if file_name[0].upper() != file_name[0]:
                continue    
            dir_path_only = os.sep.join(dir_path.split(os.sep)[2:])
            js_paths.append(os.path.join(dir_path_only, file_name).replace('\\','/'))
    js_paths.sort()
    return js_paths


def build_common_index(dir_root: str):
    js_paths = get_js_paths(dir_root)
    lines = ['// Auto-generated by add_indices_v202409.py', '']
    class_names = []
    for js_path in js_paths:
        class_name = os.path.basename(js_path)[:-3]
        lines.append(f'import {class_name} from "./{js_path}";')
        class_names.append(class_name)

    lines.extend(['', 'export {'])
    for class_name in class_names:
        lines.append(f'  {class_name},')
    lines.append('};')
    
    lines.append('')
    common_index_path = os.path.join(dir_root, 'index.js')
    File(common_index_path).write_lines(lines)


def get_child_dirs(dir_root: str) -> list[str]:
    child_dirs = []
    for file_or_dir in os.listdir(dir_root):
        if os.path.isdir(os.path.join(dir_root, file_or_dir)):
            child_dirs.append(file_or_dir)
    child_dirs.sort()
    return child_dirs


def main():
    dir_root = "./src"
    assert os.path.exists(dir_root)
    for child_dir in get_child_dirs(dir_root):
        build_common_index(os.path.join(dir_root, child_dir))


if __name__ == '__main__':
    main()