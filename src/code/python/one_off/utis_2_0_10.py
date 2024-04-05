import os
import sys


def simple_replace(dir_path, before_after_pairs):
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if not file.endswith('.py'):
                continue
            if file in ['utis_2_0_10.py']:
                continue
            file_path = os.path.join(root, file)
            try:
                content = None
                with open(file_path, 'r') as f:
                    content = f.read()
                has_updated = False
                for before, after in before_after_pairs:
                    if before in content:
                        content = content.replace(before, after)
                        has_updated = True
                        print(f'{file}: "{before}" -> "{after}"')
                if has_updated:
                    with open(file_path, 'w') as f:
                        f.write(content)
                    print(f'🟢 Wrote {file}')
                    os.startfile(file_path)
            except BaseException:
                print(f'🔴 Error processing {file}')
    print("Fixed various utils_2_0_10 BUGS")


def main(dir_path):
    before_after_pairs = [
        ["hashx", "Hash"],
        ["TIME_FORMAT_", 'TimeFormat.'],
        [" SECONDS_IN", " TimeUtil.SECONDS_IN"],
    ]
    simple_replace(dir_path, before_after_pairs)


if __name__ == "__main__":
    dir_path = sys.argv[1]
    main(dir_path)
