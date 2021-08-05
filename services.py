import os
import sys
from typing import List

import settings
from models import Module


def create_dir(path: str):
    try:
        print(f"Creating dir: {path}")
        os.mkdir(path)
    except FileExistsError:
        print(f"{path} already exists!")


# https://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename
def slugify(value):
    return "".join(i for i in value if i not in "\/:*?<>|").strip()


def write_file(title, ext, content):
    with open(f'{title}.{ext}', 'wb') as f:
        print(f"Create {title} {ext} file.")
        f.write(content)


def delete_residual(files, skip=False):
    if not skip:
        try:
            [os.remove(file) for file in files]
        except FileNotFoundError:
            print("Cannot delete files!")


def cd_module_dir(module: Module, path: str):
    os.chdir(path)
    module_path = os.path.join(path, module.title)
    create_dir(module_path)
    os.chdir(module_path)


def get_kwargs(kwargs):
    def iter_kwargs(args):
        for arg in args:
            if arg.startswith('--'):
                try:
                    key, val = arg.split('=', 1)
                    yield key, val
                except ValueError:
                    raise ValueError("Kwargs is incorrect!")

    return {key: val for key, val in iter_kwargs(kwargs)}


def get_optional(args):
    return [opt for opt in args if opt.startswith('-')]


def init_source_dir():
    work_dir = os.getcwd()
    source_dir = settings.SOURCE_DIR
    path = os.path.join(work_dir, source_dir)
    create_dir(path)
    return path


def filter_specific(modules: List[Module], kwargs):
    if '--specific' in kwargs:
        return filter(lambda x: x.title in kwargs['--specific'].split(','),
                      modules)
    return modules

