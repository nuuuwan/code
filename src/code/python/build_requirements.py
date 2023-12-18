import os
from unittest import mock

import setuptools
from utils import File, Log

log = Log('build requirements')


def main():
    if not os.path.exists('setup.py'):
        return
    with mock.patch.object(setuptools, 'setup') as mock_setup:
        pass

        call_args = mock_setup.call_args
        if not call_args:
            return
        
        _, kwargs = call_args
        install_requires = kwargs.get('install_requires', [])
        file_path = 'requirements.txt'
        File(file_path).write_lines(
            ['# Autogenerate by build_requirements'] + install_requires
        )
        log.info(f'Wrote {len(install_requires)} dependencies to {file_path}')


if __name__ == '__main__':
    main()
